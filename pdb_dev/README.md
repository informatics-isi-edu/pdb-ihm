# Generating Backend Configuration Files

The PDB backend application is using a configuration file [pdb_conf.json](https://github.com/informatics-isi-edu/protein-database/blob/master/scripts/pdb_processing/config/pdb_conf.json). 
It is referring files which most of them can be found at [PDB Configuration Files](https://github.com/informatics-isi-edu/protein-database/blob/master/scripts/pdb_processing/config).
Some of those files need to be generated using tools that are included in the Python [pdb_dev](https://github.com/informatics-isi-edu/protein-database/tree/master/pdb_dev) package.
Their sources can be viewed at [backend configuration tools](https://github.com/informatics-isi-edu/protein-database/tree/master/pdb_dev/config/app).

### Operational Mode

The following commands need to executed in order to generate the PDB backend configuration files:

1. Generating the introspection of **`entry`** table from the catalog **`1`**
```
    python -m pdb_dev.config.app.get_catalog_model data.pdb-dev.org 1 display PDB:entry > catalog_1_display_entry.json
```
The output is the **`catalog_1_display_entry.json`** file.  

2. Generating the tables dependencies
```
python -m pdb_dev.config.app.get_tables_dependencies data.pdb-dev.org PDB tables_groups.json
```
While loading the data, the Foreign Keys establish an order in which the tables will be loaded. The output **`tables_groups.json`** file has as keys a group number, 
and the tables from the group **`n`** need to be loaded after the tables in the groups **`m`** where **`m < n`**. That is because it has foreign keys referring columns 
from the tables in the **`m`** groups.

3. Generating the constraints introspection (keys, foreign keys) of the catalog **`1`**
```
python -m pdb_dev.config.app.get_catalog_model data.pdb-dev.org 1 display:constraints PDB > catalog_1_display_PDB_constraints.json
```
The **`catalog_1_display_PDB_constraints.json`** file contains for each table the columns that are **`keys`**, **`foreign keys`** or **`referenced_by`**.

4. Generating the optional foreign keys to the **`RID`** column
```
python -m pdb_dev.config.app.get_optional_fk 1 catalog_1_display_PDB_constraints.json optional_fk.json
```
The tool uses as input the **`catalog_1_display_PDB_constraints.json`** file generated at step **`3`**. The output **`optional_fk.json`** file contains the foreign key names together with foreign keys and references by columns.

5. Generating the **`ermrest`** tables from the original [json-full-db-ihm_dev_full-col-ihm_dev_full.json](https://github.com/informatics-isi-edu/protein-database/blob/master/config-scripts/initial/json-may-27-2021/json_schema/json-full-db-ihm_dev_full-col-ihm_dev_full.json) file in a format closer to the **`ermrest`** introspection
```
python -m pdb_dev.config.app.get_ermrest_table_defs json-full-db-ihm_dev_full-col-ihm_dev_full.json ermrest_table_defs.json
```
The **`ermrest_table_defs.json`** file contains the `ermrest` tables and columns that will be exported in the `system generated mmCIF` file.

6. Generating the columns that has the **`.`** as a default value
```
python -m pdb_dev.config.app.get_mmcif_defaults data.pdb-dev.org 1 PDB > mmCIF_defaults.json
```
In case those columns don't have a value set by the user, the default value **`.`** will be used.

7. Generating the combo1 columns referring the **`RID`** column
```
python -m pdb_dev.config.app.get_columns_end_with_rid data.pdb-dev.org 1
```
The output is the **`combo1_columns.json`** file.

8. Generating the vocabulary ucode column
```
python -m pdb_dev.config.app.get_ucode_all data.pdb-dev.org 1
```
The script needs to have the [testGetUcode.py](https://github.com/informatics-isi-edu/protein-database/blob/master/scripts/dictionary-api/testGetUcode.py), 
[ihm-extension.dic](https://github.com/informatics-isi-edu/protein-database/blob/master/scripts/make-json/py-rcsb_db/CACHE/dictionaries/ihm-extension.dic) and 
[mmcif_v5.342_ihm_v1.17.dic](https://github.com/informatics-isi-edu/protein-database/blob/master/scripts/make-json/py-rcsb_db/CACHE/dictionaries/mmcif_v5.342_ihm_v1.17.dic) files.
The output **`vocab_ucode.json`** contains the vocabulary columns whose values will be converted to upper case.

