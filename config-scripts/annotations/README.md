# PDB Annotations

This directory contains the annotations configuration files for PDB. The files are:

```
Makefile : a file to generate the JSON annotation file from the CPP annotation file
add_pdb_annotations.py : a script to extend the pattern annotations file with the rest of the annotations
annotation_config.cpp : a file with all the annotations of catalog 99 as of today 30-JUN-2020
annotation_patterns.json : a file that contains just the pattern annotations
annotations_known_attributes.json : a files that contains the names of the known annotations.
```

## Dump the latest definitions of the annotations from a catalog

Execute:

```
deriva-annotation-dump --config-file annotations_known_attributes.json <catalog_number> > catalog_<catalog_number>_annotation.json

```

The script will dump all the current annotations of the catalog `<catalog_number>` into the `catalog_<catalog_number>_annotation.json` file.

## Extend the pattern annotations file with the rest of the annotations from the catalog

Execute:

```
python3 add_pdb_annotations.py annotation_patterns.json catalog_<catalog_number>_annotation.json annotation_config.cpp
```

The script generates the `annotation_config.cpp` file with all the annotations from the catalog `<catalog_number>`.

## Update the annotations

Update the annotations from the `annotation_config.cpp` file. You can use macro statements like:

```
#ifdef dev    
                "url_pattern": "/hatrac/resources/protocol/{{$moment.year}}/{{{File_MD5}}}"
#else
                "url_pattern": "/hatrac/resources/protocol/2018/{{{File_MD5}}}"
#endif

```

or adding also comments like:

```
#if defined(dev) or defined(hatrac)
                "url_pattern": "/hatrac/resources/protocol/{{$moment.year}}/{{{File_MD5}}}"
#else		  
                "url_pattern": "/hatrac/resources/protocol/2018/{{{File_MD5}}}"
#endif

```

## Generate the updated JSON file with the annotations

Execute for development:

```
make dev_annotation_config.json
```

or for production:

```
make production_annotation_config.json
```

The `make` command will generate the `dev_annotation_config.json` or `production_annotation_config.json` file.

## Update the annotations in the database

Execute for the entire catalog:

```
deriva-annotation-config --host pdb.isrd.isi.edu --config-file dev_annotation_config.json <catalog_number>

```

or for just a schema:

```
deriva-annotation-config --host pdb.isrd.isi.edu --config-file dev_annotation_config.json -s <schema_name> <catalog_number>

```

or just for a table:

```
deriva-annotation-config --host pdb.isrd.isi.edu --config-file dev_annotation_config.json -s <schema_name> -t <table_name> <catalog_number>

```

## Applying the annotations

Execute the following script:

```
./apply_annotations.sh <host> <catalog>
```

### Examples

For dev:

```
./apply_annotations.sh dev-aws.pdb-dev.org 99
```

For staging:

```
./apply_annotations.sh dev-aws.pdb-dev.org 50
```

For production:

```
./apply_annotations.sh data.pdb-dev.org 1
```
