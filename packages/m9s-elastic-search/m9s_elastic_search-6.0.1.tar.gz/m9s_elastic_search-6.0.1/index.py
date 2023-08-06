# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import json

from pyes.exceptions import NotFoundException

from trytond.exceptions import UserError
from trytond.i18n import gettext
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool


class IndexBacklog(ModelSQL, ModelView):
    "Index Backlog"
    __name__ = "elasticsearch.index_backlog"

    record_model = fields.Char('Record Model', required=True, select=True)
    record_id = fields.Integer('Record ID', required=True, select=True)

    @classmethod
    def create_from_records(cls, records):
        """
        A convenience create method which can be passed multiple active
        records and they would all be added to the indexing backlog. A check
        is done to ensure that a record is not already in the backlog.

        :param record: List of active records to be indexed
        """
        vlist = []
        for record in records:
            if not cls.search([
                    ('record_model', '=', record.__name__),
                    ('record_id', '=', record.id),
            ], limit=1):
                vlist.append({
                    'record_model': record.__name__,
                    'record_id': record.id,
                })
        return cls.create(vlist)

    @staticmethod
    def _build_default_doc(record):
        """
        If a document does not have an `elastic_search_json` method, this
        method tries to build one in lieu.
        """
        return {
            'rec_name': record.rec_name,
        }

    @classmethod
    def update_index(cls, batch_size=100):
        """
        Update the remote elastic search index from the backlog and
        delete backlog entries once done.

        To be scalable, this operation limits itself to handling the oldest
        batch of records at a time. The batch_size can be optionally passed on
        to this function call. This should be small enough for subsequent
        transactions not to be blocked for a long time.

        That depends on your specific implementation and index size.
        """
        config = Pool().get('elasticsearch.configuration')(1)

        conn = config.get_es_connection()

        for item in cls.search_read(
                [], order=[('id', 'DESC')], limit=batch_size,
                fields_names=['record_model', 'record_id', 'id']):

            Model = Pool().get(item['record_model'])

            try:
                record, = Model.search([('id', '=', item['record_id'])])
            except ValueError:
                # Record may have been deleted
                try:
                    conn.delete(
                        config.index_name,                      # Index Name
                        config.make_type_name(Model.__name__),  # Document Type
                        item['record_id']
                    )
                except NotFoundException:
                    # This record was not there in elastic search too.
                    # Never mind!
                    pass
            else:
                if hasattr(record, 'elastic_search_json'):
                    # A model with the elastic_search_json method
                    data = record.elastic_search_json()
                else:
                    # A model without elastic_search_json
                    data = cls._build_default_doc(record)

                conn.index(
                    data,
                    config.index_name,                          # Index Name
                    config.make_type_name(record.__name__),     # Document Type
                    record.id,                                  # Record ID
                )
            finally:
                # Delete the item since it has been sent to the index
                cls.delete([cls(item['id'])])


class DocumentType(ModelSQL, ModelView):
    "ElasticSearch Document Type"
    __name__ = "elasticsearch.document.type"

    name = fields.Char('Name', required=True)
    model = fields.Many2One('ir.model', 'Model', required=True, select=True)
    mapping = fields.Text('Mapping', required=True)

    @staticmethod
    def default_mapping():
        return '{}'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        # TODO: add a unique constraint on model
        cls._buttons.update({
            'update_mapping': {},
            'reindex_all_records': {},
            'get_default_mapping': {},
        })

    @classmethod
    def validate(cls, document_types):
        "Validate the records"
        super().validate(document_types)
        for document_type in document_types:
            document_type.check_mapping()

    def check_mapping(self):
        """
        Check if it is possible to at least load the JSON
        as a check for its validity
        """
        try:
            json.loads(self.mapping)
        except:
            raise UserError(gettext('elastic_search.wrong_mapping'))

    @classmethod
    @ModelView.button
    def reindex_all_records(cls, document_types):
        """
        Reindex all of the records in this model

        :param document_types: Document Types
        """
        IndexBacklog = Pool().get('elasticsearch.index_backlog')

        for document_type in document_types:
            Model = Pool().get(document_type.model.model)
            records = Model.search([])

            # Performance speedups
            index_backlog_create = IndexBacklog.create
            model_name = Model.__name__

            vlist = []
            for record in records:
                vlist.append({
                    'record_model': model_name,
                    'record_id': record.id,
                })
            index_backlog_create(vlist)

    @classmethod
    @ModelView.button
    def get_default_mapping(cls, document_types):
        """
        Tries to get the default mapping from the model object
        """
        for document_type in document_types:
            Model = Pool().get(document_type.model.model)
            if hasattr(Model, 'es_mapping'):
                cls.write(
                    [document_type], {
                        'mapping': json.dumps(Model.es_mapping(), indent=4)
                    }
                )
            else:
                raise UserError(gettext(
                        'elastic_search.model_without_mapping',
                        Model.__name__))

    @classmethod
    @ModelView.button
    def update_mapping(cls, document_types):
        """
        Update the mapping on the server side
        """
        config = Pool().get('elasticsearch.configuration')(1)

        conn = config.get_es_connection()

        for document_type in document_types:
            conn.indices.put_mapping(
                config.make_type_name(document_type.model.model),   # Type
                json.loads(document_type.mapping),                  # Mapping
                [config.index_name],                                # Index
            )
