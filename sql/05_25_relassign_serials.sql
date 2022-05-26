BEGIN;

-- before new batch of legacy files are added, the max serial number is 129.
/*
count | max |              max              
-------+-----+-------------------------------
    53 | 129 | 2022-05-17 09:12:33.854582-07
*/
SELECT count(*), max("Accession_Serial"), max("RCT")
FROM "PDB".entry
WHERE "RCT" < '2022-05-19';

/* summary of legacy files and new submission files prior to 2022/05/19
 count | min | max |              max              
-------+-----+-----+-------------------------------
    30 |  52 |  88 | 2019-10-30 11:16:50.028724-07  -- legacy
    23 |  16 | 129 | 2022-05-17 09:12:33.854582-07  -- new submissn
*/
SELECT count(*), min("Accession_Serial"), max("Accession_Serial"), max("RCT")
-- SELECT id, accession_code, "Accession_Serial", "Process_Status", "RCT", "mmCIF_File_Name" 
FROM "PDB".entry
WHERE "RCT" < '2022-05-19'
  AND NOT id ~ 'PDBDEV'
;

/* status of new submission after 2022/05/19
    id    | accession_code  | Accession_Serial | Process_Status |              RCT              |       mmCIF_File_Name       
----------+-----------------+------------------+----------------+-------------------------------+-----------------------------
 D_2-65VT |                 |              185 | success        | 2022-05-25 09:57:48.848092-07 | nsp7-11_combi-final-ihm.cif
 D_2-5W40 | PDBDEV_00000184 |              184 | success        | 2022-05-20 07:35:02.668669-07 | nsp7-8_combi-2.cif
*/
SELECT id, accession_code, "Accession_Serial", "Process_Status", "RCT", "mmCIF_File_Name" 
FROM "PDB".entry
WHERE "RCT" > '2022-05-19'
  AND NOT "mmCIF_File_Name" ~ 'PDBDEV'
;

-- ===============================================================
-- update database

-- update the legacy entries with new serial number derived from mmcif_file_name. 
UPDATE "PDB".entry e
SET "Accession_Serial" = t.serial
FROM
(
SELECT id, accession_code, "Accession_Serial", "Workflow_Status", "Process_Status", "RCT", "mmCIF_File_Name",  
  (regexp_replace("mmCIF_File_Name", '^PDBDEV_([0-9]*).cif', '\1', 'ig'))::int4 as new_serial,
  CASE
    WHEN accession_code IS NOT NULL THEN 'PDBDEV_'||to_char("Accession_Serial" - 54, 'FM00000000')
    ELSE NULL
  END AS new_accession_code
FROM "PDB".entry
WHERE "RCT" > '2022-05-19'
  AND "mmCIF_File_Name" ~ 'PDBDEV'
ORDER BY "mmCIF_File_Name" desc
) AS t
WHERE e.id = t.id
;

-- update the new entries with new serial number and accession_code if already assigned
UPDATE "PDB".entry e
SET "Accession_Serial" = t.new_serial,
  accession_code = t.new_accession_code
(
SELECT id, accession_code, "Accession_Serial", "Workflow_Status", "Process_Status", "RCT", "mmCIF_File_Name",
  "Accession_Serial" - 54 AS new_serial, 
  CASE
    WHEN accession_code IS NOT NULL THEN 'PDBDEV_'||to_char("Accession_Serial" - 54, 'FM00000000')
    ELSE NULL
  END AS new_accession_code
FROM "PDB".entry
WHERE "RCT" > '2022-05-19'
  AND NOT "mmCIF_File_Name" ~ 'PDBDEV'
)
    
COMMIT;







