import os
import json
from pypers.core.interfaces import db

class IndexConfig:

    def __init__(self, pipeline_type, collection_name):
        self.config = db.get_indexer_config() \
                        .get_config('solr.index')

        self.type = pipeline_type
        self.collection = collection_name

    def save_to_disk(self, path):
        with open(path, 'w') as f:
            f.wrtie(json.dumps(self.config))

    def get_collection_config(self):
        # type default
        dflt_config = self.config.get(self.type, {}) \
                                 .get('_default_', {}) \
                                 .get('index', {})

        # collection specific
        coll_config = self.config.get(self.type, {}) \
                                 .get(self.collection, {}) \
                                 .get('index', {})

        # merge by overriding dflt by coll
        dflt_config.update(coll_config)

        return dflt_config

    def get_solr_url(self):
        return os.environ.get('SLRW_URL')

    def get_solr_timeout(self):
        return os.environ.get('SLRW_TIMEOUT', 20)

    def get_batch_size(self):
        return os.environ.get('SLRW_BATCH_SIZE', 100)


