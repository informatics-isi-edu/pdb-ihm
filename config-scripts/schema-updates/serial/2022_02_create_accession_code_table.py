import sys
import json
import traceback
from deriva.core.ermrest_model import tag as chaise_tags
from deriva.core import get_credential, DerivaServer, BaseCLI, urlquote
from deriva.core.ermrest_model import Column, builtin_types, Table, Key, ForeignKey
import utils
from utils import ApplicationClient

pdb_admin = "https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee"
isrd_staff = "https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b"
pdb_curator = "https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"

acls = {
      "delete": [
        pdb_admin,
        isrd_staff,
        pdb_curator
      ],
        "insert": [
            pdb_admin,
            pdb_curator,
            isrd_staff
        ],
        "select": [
            '*'
        ],
        "update": [
            pdb_admin,
            pdb_curator,
            isrd_staff
        ],
      "enumerate": ['*']
}

def define_tdoc_Accession_Code():
    table_name='Accession_Code'
    comment='Generates a new accession serial value with a reference to the entry table.'

    column_defs = [
         Column.define(
            'Accession_Serial',
            builtin_types.serial4,
            nullok=False,
            comment='The latest accession serial value.'
        ),
        Column.define(
            'Accession_Code',
            builtin_types.text,
            nullok=False,
            comment='The corresponding accession code value.'
        ),
       Column.define(
            'Entry',
            builtin_types.text,
            nullok=False,
            comment='A foreign key to the RID of the entry.'
        ),
        Column.define(
            "Owner",
            builtin_types.text,
            comment='Group that can update the record.',                        
            nullok=True
        )
    ]
    
    key_defs = [
        Key.define(["Accession_Serial"], constraint_names=[["PDB", "Accession_Code_Accession_Serial_primary_key"]] ),
        Key.define(["Accession_Code"], constraint_names=[["PDB", "Accession_Code_Accession_Code_primary_key"]] ),
        Key.define(["Entry"], constraint_names=[["PDB", "Accession_Code_Entry_primary_key"]] )
    ]

    fkey_defs = [
        ForeignKey.define(["Entry"], "PDB", "entry", ["RID"],
                          constraint_names=[ ["PDB", "Accession_Code_Entry_fkey"] ],
                          on_update="CASCADE",
                          on_delete="CASCADE"
        ),
        ForeignKey.define(["RCB"], "public", "ERMrest_Client", ["ID"],
                          constraint_names=[["PDB", '{}_RCB_fkey'.format(table_name)]],
                          on_update="NO ACTION",
                          on_delete="NO ACTION"   
        ),
        ForeignKey.define(["RMB"], "public", "ERMrest_Client", ["ID"],
                          constraint_names=[["PDB", '{}_RMB_fkey'.format(table_name)]],
                          on_update="NO ACTION",
                          on_delete="NO ACTION"   
        ),
        ForeignKey.define(["Owner"], "public", "Catalog_Group", ["ID"],
                          constraint_names=[["PDB", '{}_Owner_fkey'.format(table_name)]],
                          on_update="NO ACTION",
                          on_delete="NO ACTION"   
        )
    ]
    table_def = Table.define(
        table_name,
        column_defs,
        key_defs=key_defs,
        fkey_defs=fkey_defs,
        acls=acls,
        comment=comment,
        provide_system=True
    )
    return table_def
    
def setNextAccessionSerial(rid, user):
    try:
        row = {'Entry': rid}
        url = '/entity/PDB:Accession_Code?defaults=Accession_Serial'
        resp = self.catalog.post(
            url,
            json=[row]
        )
        resp.raise_for_status()
        
        if len(resp.json()) == 1:
            row = resp.json()[0]
            self.logger.debug('SUCCEEDED created in the table %s the entry:\n %s.' % ('Accession_Code', json.dumps(row, indent=4))) 
        return
    except:
        et, ev, tb = sys.exc_info()
        self.logger.error('got exception "%s"' % str(ev))
        self.logger.error('%s' % ''.join(traceback.format_exception(et, ev, tb)))
        self.export_error_message = 'ERROR setNextAccessionSerial: "%s"' % str(ev)
        subject = 'PDB-Dev {} {}: {} ({})'.format(rid, 'SUBMIT', Process_Status_Terms['ERROR_GENERATING_ACCESSION_CODE'], user)
        self.sendMail(subject, 'RID: %s\n%s\n' % (rid, ''.join(traceback.format_exception(et, ev, tb))))
        return
    
def updateAccessionSerial(rid, user, value):
    try:
        url = '/entity/PDB:Accession_Code/Entry={}'.format(urlquote(rid))
        self.logger.debug('Query URL: "%s"' % url) 
        resp = self.catalog.get(url)
        resp.raise_for_status()
        rows = resp.json()
        if len(rows) > 0:
            row = resp.json()[0]
            row['Accession_Serial'] = value
            self.updateAttributes('PDB',
                                  'Accession_Code',
                                  row['RID'],
                                  ["Accession_Serial"],
                                  row,
                                  user)
            self.logger.debug('SUCCEEDED updated in the table %s the entry:\n %s.' % ('Accession_Code', json.dumps(row, indent=4))) 
        else:
            row = {'Entry': rid, 'Accession_Serial': value}
            url = '/entity/PDB:Accession_Code'
            resp = self.catalog.post(
                url,
                json=[row]
            )
            resp.raise_for_status()
            
            if len(resp.json()) == 1:
                row = resp.json()[0]
                self.logger.debug('SUCCEEDED created in the table %s the entry:\n %s.' % ('Accession_Code', json.dumps(row, indent=4))) 
        return
    except:
        et, ev, tb = sys.exc_info()
        self.logger.error('got exception "%s"' % str(ev))
        self.logger.error('%s' % ''.join(traceback.format_exception(et, ev, tb)))
        self.export_error_message = 'ERROR updateAccessionSerial: "%s"' % str(ev)
        subject = 'PDB-Dev {} {}: {} ({})'.format(rid, 'SUBMIT', Process_Status_Terms['ERROR_GENERATING_ACCESSION_CODE'], user)
        self.sendMail(subject, 'RID: %s\n%s\n' % (rid, ''.join(traceback.format_exception(et, ev, tb))))
        return
    
def initializeAccessionCode(catalog):
    try:
        url = '/entity/PDB:entry'
        resp = catalog.get(url)
        resp.raise_for_status()
        rows = resp.json()
        url = '/entity/PDB:Accession_Code'
        for row in rows:
            accession_code_row = {'Entry': row['RID'], 
                                  'Accession_Serial': row['Accession_Serial'], 
                                  'Accession_Code': row['accession_code'] if row['accession_code'] != None else 'PDBDEV_' + ('00000000' + str(row['Accession_Serial']))[-8:]}
            resp = catalog.post(
                url,
                json=[accession_code_row]
            )
            resp.raise_for_status()
        print('SUCCEEDED initializing the table Accession_Code')
        url = '/aggregate/PDB:entry/max:=max(Accession_Serial)'
        resp = catalog.get(url)
        resp.raise_for_status()
        rows = resp.json()
        offset = rows[0]['max']
        print('Execute:\nselect setval(\'"PDB"."Accession_Code_Accession_Serial_seq"\', {});'.format(offset))
        return
    except:
        et, ev, tb = sys.exc_info()
        print('got exception "%s"' % str(ev))
        print('%s' % ''.join(traceback.format_exception(et, ev, tb)))
        return
    
def updateEntryAccessionCode(catalog):
    try:
        url = '/entity/PDB:entry'
        resp = catalog.get(url)
        resp.raise_for_status()
        rows = resp.json()
        url = '/entity/PDB:Accession_Code'
        entry_accession_code_rows = []
        for row in rows:
            if row['accession_code'] != None:
                continue
            
            url = '/attribute/PDB:Accession_Code/Entry={}/Accession_Code'.format(urlquote(row['RID']))
            resp = catalog.get(url)
            resp.raise_for_status()
            accession_code_rows = resp.json()
            if len(accession_code_rows) != 1:
                print('len(accession_code_row) != 1')
            accession_code_row = accession_code_rows[0]
            entry_accession_code_row = {'RID': row['RID'], 'accession_code': accession_code_row['Accession_Code']}
            entry_accession_code_rows.append(entry_accession_code_row)
        columns = ['accession_code']
        columns = ','.join([urlquote(col) for col in columns])
        url = '/attributegroup/PDB:entry/RID;{}'.format(columns)
        resp = catalog.put(
            url,
            json=entry_accession_code_rows
        )
        resp.raise_for_status()
        print('SUCCEEDED updated the table accession_code in the entry table')
        return
    except:
        et, ev, tb = sys.exc_info()
        print('got exception "%s"' % str(ev))
        print('%s' % ''.join(traceback.format_exception(et, ev, tb)))
        return
    
def getNextAccessionSerial(rid, user):
    try:
        accession_serial_value = None
        row = {'Name': 'Dummy'}
        url = '/entity/PDB:Accession_Serial?defaults=Value'
        resp = self.catalog.post(
            url,
            json=[row]
        )
        resp.raise_for_status()
        
        self.logger.debug('SUCCEEDED created in the table "%s" the entry "%s".' % (url, json.dumps(row, indent=4))) 
        if len(resp.json()) == 1:
            row = resp.json()[0]
            accession_serial_rid = row['RID']
            accession_serial_value = row['Value']
            url = '/entity/PDB:Accession_Serial/RID={}'.format(urlquote(accession_serial_rid))
            resp = self.catalog.delete(
                url
            )
            resp.raise_for_status()
            self.logger.debug('SUCCEEDED deleted the rows for the URL "%s".' % (url)) 
        return accession_serial_value
    except:
        et, ev, tb = sys.exc_info()
        self.logger.error('got exception "%s"' % str(ev))
        self.logger.error('%s' % ''.join(traceback.format_exception(et, ev, tb)))
        self.export_error_message = 'ERROR getNextAccessionSerial: "%s"' % str(ev)
        subject = 'PDB-Dev {} {}: {} ({})'.format(rid, 'SUBMIT', Process_Status_Terms['ERROR_GENERATING_ACCESSION_CODE'], user)
        self.sendMail(subject, 'RID: %s\n%s\n' % (rid, ''.join(traceback.format_exception(et, ev, tb))))
        return None
    
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    """
    Create the Accession_Code table
    """
    
    utils.drop_table(catalog, 'PDB', 'Accession_Code')
    model = catalog.getCatalogModel()
    utils.create_table_if_not_exist(model, 'PDB', define_tdoc_Accession_Code())
    initializeAccessionCode(catalog)

    utils.drop_fkey_if_exist(model, 'PDB', 'entry', 'entry_accession_code_fkey')
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'entry', 'entry_accession_code_fkey',
                                            ForeignKey.define(['accession_code'], 'PDB', 'Accession_Code', ['Accession_Code'],
                                              constraint_names=[ ['PDB', 'entry_accession_code_fkey'] ],
                                              on_update='CASCADE',
                                              on_delete='SET NULL')
                                           )
    updateEntryAccessionCode(catalog)
    
    utils.drop_column_if_exist(model, 'PDB', 'entry', 'Accession_Serial')



if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)
    
