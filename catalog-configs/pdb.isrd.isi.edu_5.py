import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
from deriva.utils.catalog.components.deriva_model import DerivaCatalog
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args
from deriva.core.ermrest_config import tag as chaise_tags
import deriva.core.ermrest_model as em

groups = {
    'pdb-admin': 'https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee',
    'pdb-reader': 'https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee',
    'pdb-writer': 'https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a',
    'pdb-curator': 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6',
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'
}

bulk_upload = {
    'asset_mappings': [
        {
            'asset_type': 'table',
            'ext_pattern': '^.*[.](?P<file_ext>json|csv)$',
            'file_pattern': '^((?!/assets/).)*/records/(?P<schema>WWW?)/(?P<table>Page)[.]',
            'target_table': ['WWW', 'Page'],
            'default_columns': ['RID', 'RCB', 'RMB', 'RCT', 'RMT']
        },
        {
            'column_map': {
                'MD5': '{md5}',
                'URL': '{URI}',
                'Page': '{table_rid}',
                'Length': '{file_size}',
                'Filename': '{file_name}'
            },
            'dir_pattern': '^.*/(?P<schema>WWW)/(?P<table>Page)/(?P<key_column>.*)/',
            'ext_pattern': '^.*[.](?P<file_ext>.*)$',
            'file_pattern': '.*',
            'target_table': ['WWW', 'Page_Asset'],
            'checksum_types': ['md5'],
            'hatrac_options': {
                'versioned_uris': True
            },
            'hatrac_templates': {
                'hatrac_uri': '/hatrac/{schema}/{table}/{md5}.{file_name}'
            },
            'record_query_template': '/entity/{schema}:{table}_Asset/{table}={table_rid}/MD5={md5}/URL={URI_urlencoded}',
            'metadata_query_templates': [
                '/attribute/D:={schema}:{table}/RID={key_column}/table_rid:=D:RID'
            ]
        }
    ],
    'version_update_url': 'https://github.com/informatics-isi-edu/deriva-qt/releases',
    'version_compatibility': [['>=0.4.3', '<1.0.0']]
}

catalog_config = {
    'name': 'pdb',
    'groups': {
        'admin': groups['pdb-admin'],
        'reader': groups['pdb-reader'],
        'writer': groups['pdb-writer'],
        'curator': groups['pdb-curator']
    }
}

annotations = {chaise_tags.bulk_upload: bulk_upload, chaise_tags.catalog_config: catalog_config, }

acls = {
    'insert': [groups['pdb-curator'], groups['pdb-writer']],
    'delete': [groups['pdb-curator']],
    'write': [],
    'enumerate': ['*'],
    'select': [groups['pdb-writer'], groups['pdb-reader']],
    'owner': [groups['pdb-admin'], groups['isrd-staff']],
    'update': [groups['pdb-curator']],
    'create': []
}


def main(catalog, mode, replace=False):
    updater = CatalogUpdater(catalog)
    updater.update_catalog(mode, annotations, acls, replace=replace)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 5
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_catalog=True)
    catalog = DerivaCatalog(host, catalog_id=catalog_id, validate=False)
    main(catalog, mode, replace)

