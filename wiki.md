JSON schema semantics: 

1. $ref: Foreign keys
2. _primary_key if true indicates that the data item is a primary key 
3. Type: Indicates the type of data (string, integer, number)
4. Examples: Examples of the data item (shown while hovering on column name)
5. Description and rcsb_description: Description of the data item (shown while hovering on column name)
6. attribute_groups: Group together data items that form composite keys. The id and labels within the attribute group differentiate the multiple instances of the composite foreign keys. These are used along with $ref
7. enum and rcsb_enum_annotated: Controlled vocabulary of allowed values for a column 
8. required: List of mandatory data items in a table

Each table has a structure_id data item that points to the entry_id
