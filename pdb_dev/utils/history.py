#!/usr/bin/python

import json
import sys
from datetime import datetime, timezone
from deriva.core import DerivaServer, get_credential, urlquote
from .shared import DCCTX, PDBDEV_CLI

host = 'data.pdb-dev.org'
credentials = get_credential(host)
server = DerivaServer('https', host, credentials)
catalog_id = '1'
schema_name = 'PDB'
table_name = 'entry'
key_cols = ['RID']
key_vals = ['2-TK8P']

# -- ==============================================================================================
def get_record_history(server, cid, sname, tname, kvals, kcols=['RID'], snap=None):
    parts = {
        'cid': urlquote(cid),
        'sname': urlquote(sname),
        'tname': urlquote(tname),
        'filter': ','.join([
            '%s=%s' % (urlquote(kcol), urlquote(kval))
            for kcol, kval in zip(kcols, kvals)
        ]),
    }

    if snap is None:
        # determinate starting (latest) snapshot
        r = server.get('/ermrest/catalog/%(cid)s' % parts)
        snap = r.json()['snaptime']
    parts['snap'] = snap

    path = '/ermrest/catalog/%(cid)s@%(snap)s/entity/%(sname)s:%(tname)s/%(filter)s'

    rows_found = []
    snap2rows = {}
    while True:
        url = path % parts
        sys.stderr.write('%s\n' % url)
        l = server.get(url).json()
        if len(l) > 1:
            raise ValueError('got more than one row for %r' % url)
        if len(l) == 0:
            sys.stderr.write('ERROR: %s: No record found \n' % (url))
            break
        row = l[0]
        snap2rows[parts['snap']] = row
        rows_found.append(row)
        rmt = datetime.fromisoformat(row['RMT'])
        # find snap ID prior to row version birth time
        parts['snap'] = urlb32_encode(datetime_epoch_us(rmt) - 1)
        
    return snap2rows

# -- --------------------------------------------------------------------------------------
def datetime_epoch_us(dt):
    """Return microseconds-since-epoch integer for given timezone-qualified datetime"""
    return int(dt.timestamp()) * 1000000 + dt.microsecond

# -- --------------------------------------------------------------------------------------
# Take the iso format string (same as RMT) and return the version number
#
def iso_to_snap(iso_datetime):
    rmt = datetime.fromisoformat(iso_datetime)
    return urlb32_encode(datetime_epoch_us(rmt))

# -- --------------------------------------------------------------------------------------
def urlb32_encode(i):
    """Encode integer as per ERMrest's base-32 snapshot encoding"""
    if i > 2**63-1:
        raise ValueError(i)
    elif i < -2**63:
        raise ValueError(i)

    # pad 64 bit to 65 bits for 13 5-bit digits
    raw = i << 1
    encoded_rev = []
    for d in range(1,14):
        if d > 2 and ((d-1) % 4) == 0:
            encoded_rev.append('-')
        code = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'[raw % 32]
        encoded_rev.append(code)
        raw = raw // 32

    while encoded_rev and encoded_rev[-1] in {'0', '-'}:
        del encoded_rev[-1]
        
    if not encoded_rev:
        encoded_rev = ['0']

    encoded = reversed(encoded_rev)

    return ''.join(encoded)

# -- ==============================================================================================
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer("https", server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx["cid"] = DCCTX["cli/history"]

    if args.iso2snap:
        if not args.iso_datetime:        
            args.iso_datetime = datetime.now(timezone.utc).isoformat()
        print("snap = %s" % (iso_to_snap(args.iso_datetime)))
        return 0
            
    snap2rows = get_record_history(server, catalog_id, args.schema, args.table, [args.rid], ["RID"])
    curr_time = "live"
    for snap, row in snap2rows.items():
        print("snapshot: %s\n time: %s <- %s\n chaise: %s\n records: %s\n" % (
            snap, curr_time, row["RMT"],
            "https://%s/chaise/record/#%s@%s/%s:%s/RID=%s" % (server_name,catalog_id,snap,args.schema,args.table,args.rid),
            json.dumps(row, indent=2)))
        curr_time = row["RMT"]
    return 0

# -- ==============================================================================================
# to run the script:
# to get history:
#   python -m pdb_dev.utils.history --host data.pdb-dev.org --catalog-id 1 --rid 2-TK8P
# to get snapshot version:
#   python -m pdb_dev.utils.history --iso2snap --iso-datetime <RMT>
#
if __name__ == '__main__':
    cli = PDBDEV_CLI(DCCTX["acl"], None, 1)
    cli.parser.add_argument('--schema', metavar='<schema>', help="Schama name (default=PDB)", default="PDB", required=False)
    cli.parser.add_argument('--table', metavar='<table>', help="Table name (default=entry)", default="entry", required=False)
    cli.parser.add_argument('--iso2snap', help="Return snapshot value based on iso datetime", action='store_true', required=False)
    cli.parser.add_argument('--iso-datetime', metavar='<iso_datetime>', help="ISO datetime format (default=current time)", default=None, required=False)
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    
    sys.exit(main(args.host, args.catalog_id, credentials, args))
