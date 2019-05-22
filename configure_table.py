import deriva.core.ermrest_model as em
from collections import namedtuple
from deriva.core import ErmrestCatalog, get_credential, DerivaServer
from deriva.utils.catalog.manage.configure_catalog import DerivaCatalogConfigure, DerivaTableConfigure
import deriva.utils.catalog.components.model_elements as model_elements
from deriva.core.ermrest_config import tag as chaise_tags

hostname = 'pdb.isrd.isi.edu'
catalog_number = 4
credential = get_credential(hostname)
catalog_ermrest = ErmrestCatalog('https', hostname, catalog_number, credentials=credential)
model = catalog_ermrest.getCatalogModel()
schema_name = 'PDB'

schema = model.schemas[schema_name]
catalog = model_elements.DerivaCatalog(catalog_ermrest)

tname_list = ['ihm_cross_link_list','ihm_cross_link_restraint','ihm_entity_poly_segment']


for tname in tname_list:
    table = DerivaTableConfigure(catalog, schema_name, tname)
    table.configure_table_defaults()

exit()
# adjust column order after configure_table_defaults
for tname in tname_list:
    tab = model.schemas[schema_name].tables[tname]
    vc = tab.annotations['tag:isrd.isi.edu,2016:visible-columns']
    if '*' in vc.keys():
        updated_vc = [vc['*'][0]]+vc['*'][6:]+vc['*'][1:6]
        tab.annotations.update({
            chaise_tags.visible_columns: {'*': updated_vc}
        })
        tab.apply(catalog_ermrest)