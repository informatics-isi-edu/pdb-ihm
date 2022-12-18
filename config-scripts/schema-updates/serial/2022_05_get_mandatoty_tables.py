import sys
import json
import traceback
from deriva.core.ermrest_model import tag as chaise_tags
from deriva.core import get_credential, DerivaServer, BaseCLI, urlquote
from deriva.core.ermrest_model import Column, builtin_types, Table, Key, ForeignKey
from deriva.core.utils.core_utils import tag as annotation_tags
import utils
from utils import ApplicationClient

manadatory_tables = []
checked_tables = {}

def get_tables(model):
    schema = model.schemas['PDB']
    for table_name in schema.tables:
        table = schema.tables[table_name]
        annotations = table.annotations
        if annotation_tags['display'] in annotations.keys():
            display = annotations[annotation_tags['display']]
            if 'markdown_name' in display.keys():
                markdown_name = display['markdown_name']
                if markdown_name.endswith('^*^'):
                    manadatory_tables.append(table_name)

def check_mandatory(catalog):
    url = '/entity/PDB:entry/Workflow_Status=REL'
    resp = catalog.get(url)
    resp.raise_for_status()
    rows = resp.json()
    for row in rows:
        rel_tables = []
        checked_tables[row['RID']] = rel_tables
        for table_name in manadatory_tables:
            if table_name != 'entry':
                url = '/entity/PDB:entry/RID={}/PDB:{}'.format(row['RID'], table_name)
                resp = catalog.get(url)
                resp.raise_for_status()
                mandatory_rows = resp.json()
                if len(mandatory_rows) == 0:
                    rel_tables.append(table_name) 
    
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    get_tables(model)
    print('Mandatory tables')
    print(json.dumps(manadatory_tables, indent=4))                    
    print(len(manadatory_tables))
    
    check_mandatory(catalog)
    
    print('Checked tables')
    print(json.dumps(checked_tables, indent=4))                    
    print(len(checked_tables))
    
if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)

