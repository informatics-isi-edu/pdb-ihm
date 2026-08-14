#!/bin/bash

su -c "psql -q -d hatrac" - hatrac <<EOF
-- remove ownership of user-id and give read/write access based on uid
UPDATE hatrac.name n
SET "create" = ARRAY['https://auth.globus.org/'||(regexp_split_to_array(name, '/'))[ cardinality(regexp_split_to_array(name, '/')) ]],
  "subtree-create" = ARRAY['https://auth.globus.org/'||(regexp_split_to_array(name, '/'))[ cardinality(regexp_split_to_array(name, '/')) ]],
  "subtree-update" = ARRAY['https://auth.globus.org/'||(regexp_split_to_array(name, '/'))[ cardinality(regexp_split_to_array(name, '/')) ]],
  "subtree-read" = ARRAY['https://auth.globus.org/'||(regexp_split_to_array(name, '/'))[ cardinality(regexp_split_to_array(name, '/')) ]],
  "read" = "owner",
  "owner" = NULL,
  "subtree-owner" = NULL
WHERE ( name ~ '^(/dev)?/pdb/submitted/uid/[^/]+$'
     OR name ~ '/dev/pdb/user/[^/]+$')
  AND "owner" IS NOT NULL AND "owner"::text != '{}'
;  

-- remove ownership of user-id and give read access based on uid
UPDATE hatrac.name n
SET "subtree-read" = ARRAY['https://auth.globus.org/'||(regexp_split_to_array(name, '/'))[ cardinality(regexp_split_to_array(name, '/')) ]],
    "read" = "owner",
    "owner" = NULL,
    "subtree-owner" = NULL
WHERE name ~ '^(/dev)?/pdb/generated/uid/[^/]+$'
  AND "owner" IS NOT NULL AND "owner"::text != '{}'
;  

-- remove ownership of object and namespaces. For namespace, read access is for provenance. It doesn't do anything.
UPDATE hatrac.name n
set "read" = owner, owner = NULL, "subtree-owner" = NULL
WHERE ( n.name ~ '^(/|/dev)?/pdb/(submitted|generated)/uid/[^/]+/.*'
     OR n.name ~ '^(/|/dev)?/pdb/(entry|entry_files|entry_mmCIF/image/mmCIF)/.*')
  AND "read" IS NULL
  AND "owner" IS NOT NULL AND "owner"::text != '{}';

-- remove ownership of all versions so they can't be deleted.
UPDATE hatrac.version n
SET "read" = owner, owner = NULL
WHERE "read" IS NULL
  AND "owner" IS NOT NULL AND "owner"::text != '{}';

EOF


