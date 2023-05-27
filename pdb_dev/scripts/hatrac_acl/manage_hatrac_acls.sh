#!/bin/bash

su -c "psql -q -d hatrac" - hatrac <<EOF
UPDATE hatrac.name n
set "read" = owner, owner = NULL, "subtree-owner" = NULL
WHERE NOT n.name ~ '^(/|/dev)$'
  AND id != 1
  AND "read" IS NULL
  AND "owner" IS NOT NULL;

UPDATE hatrac.version n
SET "read" = owner, owner = NULL
WHERE "read" IS NULL
  AND "owner" IS NOT NULL;

EOF


