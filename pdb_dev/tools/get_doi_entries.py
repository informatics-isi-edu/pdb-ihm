from deriva.core import ErmrestCatalog, HatracStore, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, tag, AttrDict
from deriva.core import urlquote, urlunquote, DEFAULT_SESSION_CONFIG
import json

# Break the requests into batches and aggregate data afterwards
# example of descending order: "RID::desc::"
def get_entities(catalog, schema_name, table_name, constraints=None, keys=["RID"], attr_list=None, sort=["RID"], limit=None, batch_size=5000):
    payload = []
    if not limit:
        limit = 10000000
    after = []
    while True:
        page_size = limit if limit < batch_size else batch_size
        if attr_list:
            url = "/attributegroup/M:=%s:%s" % (urlquote(schema_name), urlquote(table_name))
        else:
            url = "/entity/M:=%s:%s" % (urlquote(schema_name), urlquote(table_name))
        if constraints: url = "%s/%s" % (url, constraints)
        if attr_list:
            url = "%s/%s;%s" % (url, ",".join([ urlquote(v) for v in keys ]), attr_list)
        if sort: url = "%s@sort(%s)" % (url, ",".join( [ urlquote(v) for v in sort ] ))
        if after: url = "%s@after(%s)" % (url, ",".join( [ urlquote(v) for v in after ]))
        url = "%s?limit=%d" % (url, page_size)
        #print("get_entities: url = %s" % (url))
        rows = catalog.get(url).json()
        payload.extend(rows)
        n = len(rows)
        if len(rows) == 0 or n < batch_size:
            break
        else:
            after = [ rows[-1][k] for k in sort ]
            limit = limit - n
    return(payload)


# released entries
# change the name assignment in attr_list before ":=" symbol
def get_released_entries(catalog):
    constraints="Workflow_Status=REL/LA:=(RID)=(PDB:Entry_Latest_Archive:Entry)/$M/S:=left(id)=(PDB:struct:entry_id)/$M/C:=left(id)=(PDB:citation:structure_id)/C:RID::null::;C:id=1/$M/A:=left(id)=(PDB:audit_author:structure_id)/$M"
    attr_list="entry.id:=M:id,entry.Accession_Code:=M:Accession_Code,entry.Workflow_Status:=M:Workflow_Status,entry.Deposit_Date:=M:Deposit_Date,entry.Release_Date:=M:Release_Date,Entry_Latest_Archive.Submission_Time:=LA:Submission_Time,struct.title:=S:title,citation.pdbx_database_id_DOI:=C:pdbx_database_id_DOI,audit_author.name:=array(A:name)"
    payload = get_entities(catalog, "PDB", "entry", constraints, keys=["RID", "id"], attr_list=attr_list)
    print(json.dumps(payload, indent=4))
    return payload


# hold entries
# change the name assignment in attr_list before ":=" symbol
def get_hold_entries(catalog):
    constraints="Workflow_Status=HOLD/S:=left(id)=(PDB:struct:entry_id)/$M/A:=left(id)=(PDB:audit_author:structure_id)/$M"
    attr_list="entry.id:=M:id,entry.Accession_Code:=M:Accession_Code,entry.Workflow_Status:=M:Workflow_Status,entry.Deposit_Date:=M:Deposit_Date,struct.title:=S:title,audit_author.name:=array(A:name)"
    payload = get_entities(catalog, "PDB", "entry", constraints, keys=["RID", "id"], attr_list=attr_list)
    print(json.dumps(payload, indent=4))
    return payload


# =====================================================================
def main(server_name, catalog_id, credentials, args):
    catalog = ErmrestCatalog("https", args.host, args.catalog_id, credentials)
    catalog.dcctx["cid"] = "cli/wwpdb"

    if args.workflow_status == "REL":
        rel_payload = get_released_entries(catalog)
    elif args.workflow_status == "HOLD":
        hold_payload = get_hold_entries(catalog)
        
# =====================================================================
# python upload_entry_remedy_files.py --host <host> --catalog-id <id> --workflow-status <workflow-status>
# Defaults: --host data.pdb-dev.org --catalog-id 1 --workflow-status REL
if __name__ == "__main__":
    cli = BaseCLI("pdbdev", None, 1)
    cli.remove_options(['--host', '--config-file'])
    cli.parser.add_argument('--host', metavar='<host>', help="Fully qualified deriva hostname (default=data.pdb-dev.org)", default="data.pdb-dev.org")
    cli.parser.add_argument('--catalog-id', metavar='<id>', help="Deriva catalog ID (default=1)", default="1")
    cli.parser.add_argument('--workflow-status', metavar='<workflow-status>', help="Workflow status (default=REL)", default="REL")    
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials, args)
