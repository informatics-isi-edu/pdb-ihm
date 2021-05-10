# Fix the following simple key inssues
# 1. entry: rename entry_id_unique_key to entry_id_primary_key 
# 2. struct: add struct_primary_key: [entry_id]
# 3. pdbx_entry_detail:
#  3.1. delete structure_id column and its fkey to entry table
#  3.2. create pdbx_entry_details_primary_key: [entry_id]

