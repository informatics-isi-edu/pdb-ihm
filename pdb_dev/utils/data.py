import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType

"""
add rows to a table
"""
def add_rows_to_vocab_table(catalog, table_name, rows):
    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    table = schema.__getattr__(table_name)
    table.insert(rows, defaults=['ID', 'URI'])
    print('Added rows to the vocabulary table {}'.format(table_name))

    

