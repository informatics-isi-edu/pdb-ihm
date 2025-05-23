# Annotation organizations

## Annotation file types
There are 3 types of scripts:

1. catalog-level and catalog-wide annotations containing:
- catalog-level annotations (e.g. chaise-config, column-defaults, bulk-upload)

- Annotations that apply to all schemas in the catalog. These annotations include: generated, immutable, deletable, required at
all model elements in the catalog

2. tag-specific scripts
Inidividual python file contains annotations of specific tags applied to all model elements in the catalog. Examples: asset.py

3. schema-specific scripts
The rest of the annotations that are not tag-specific are groupped based on schemas.


## Files content
### Catalog-level scripts
- catalog_annotation.py: catalog-level and catalog-wide annotations
- bulk_upload.py: bulk-upload specific annotations e.g. configurations for client tool used for uploading files in bulk. Note: bulk-upload is called from catalog_annotation.py as is a catalog annotation

### Tag-specific scripts
- assets.py: asset annotations
- export.py: export annotations
- citation.py: citation annotations (This is not being used in the project at the moment)

### Schema-specific scripts
- Vocab.py: focuses on vocab schema
- public.py: focusse on public schema
- PDB*.py: focuses on PDB schema. The contents are split due to the size.
  - PDB.py: contains annotations for entry table and deriva tables (e.g. non-cif, non-ihm)
  - PDB_ihm.py: contains annotations for table with `ihm` prefix
  - PDB_base.py: contains annotations for cif-related tables
  
## Run annotitions
```
python -m pdb_dev.config.annotation.apply_all_annotations --host data-dev.pdb-ihm.org --catalog-id 99
```
