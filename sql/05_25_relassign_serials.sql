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
-- SELECT count(*), min("Accession_Serial"), max("Accession_Serial"), max("RCT")
SELECT id, accession_code, "Workflow_Status", "Accession_Serial", "Process_Status", "RCT", "mmCIF_File_Name" 
FROM "PDB".entry
WHERE "RCT" < '2022-05-19'
  AND NOT id ~ 'PDBDEV'
ORDER BY "Accession_Serial" DESC
;

/* status of new submission after 2022/05/19
    id    | accession_code  | Accession_Serial | Process_Status |              RCT              |       mmCIF_File_Name       
----------+-----------------+------------------+----------------+-------------------------------+-----------------------------
 D_2-65VT |                 |              185 | success        | 2022-05-25 09:57:48.848092-07 | nsp7-11_combi-final-ihm.cif
 D_2-5W40 | PDBDEV_00000184 |              184 | success        | 2022-05-20 07:35:02.668669-07 | nsp7-8_combi-2.cif
*/
SELECT id, accession_code, "Accession_Serial", "Process_Status", "RCT", "mmCIF_File_Name" 
FROM "PDB".entry
WHERE NOT "mmCIF_File_Name" ~ 'PDBDEV'
ORDER BY "RCT" 
;

-- All id in the form of PDBDEV_xxxx has consistent filename
SELECT id, accession_code, "Accession_Serial", "Process_Status", "RCT", "mmCIF_File_Name" 
FROM "PDB".entry
WHERE id ~ 'PDBDEV' 
   AND "mmCIF_File_Name" ~ 'PDBDEV'
ORDER BY "RCT" 
;

-- duplicate entries (based on accession_code and filename)
/*
  -- different MD5

      id        | accession_code  | Accession_Serial | Process_Status |              RCT              |          mmCIF_File_Name           |          mmCIF_File_MD5          
-----------------+-----------------+------------------+----------------+-------------------------------+------------------------------------+----------------------------------
 D_1-N1DE        | PDBDEV_00000016 |               16 | success        | 2021-06-15 08:44:21.225609-07 | input.cif                          | 9984c98d243ceb6ecdff951d443297f9
 D_1-NM8T        | PDBDEV_00000089 |               89 | success        | 2021-07-26 03:39:32.66875-07  | aSyn_Fig4AB_Fig3ABC_states_CYS.cif | 42a25ea81f87633224fe531ea55c34c9
 D_1-P1ZE        | PDBDEV_00000092 |               92 | success        | 2021-08-13 02:48:12.672465-07 | COX_AIFM1_2.cif                    | 97515fa0dcbe70eedc1532e9c234b54d
 D_1-RK9P        | PDBDEV_00000098 |               98 | success        | 2021-12-15 13:17:06.446564-08 | centroids_python-ihm.cif           | 677b3c221464d38719ec121d00919f1c
 D_1-S916        | PDBDEV_00000099 |               99 | success        | 2022-03-15 01:43:30.550314-07 | cluster_2.cif                      | 03feaa4cb80b2210c4a755bb09ffd2f1
 PDBDEV_00000016 |                 |               81 | New            | 2019-10-30 11:16:02.470876-07 | PDBDEV_00000016.cif                | 9187d19ec0cfc34fa19ed81259c10f14
 D_1-Z1Y8        |                 |              177 | success        | 2022-05-19 14:11:31.899145-07 | PDBDEV_00000092.cif                | 5b57179ccbc5752c3318803720bb53db
*/
SELECT id, accession_code, "Accession_Serial", "Process_Status", "RCT", "mmCIF_File_Name", "mmCIF_File_MD5"
FROM "PDB".entry
WHERE accession_code IN ('PDBDEV_00000016','PDBDEV_00000089','PDBDEV_00000092','PDBDEV_00000098','PDBDEV_00000099')
   OR "mmCIF_File_Name" IN ('PDBDEV_00000016.cif','PDBDEV_00000089.cif','PDBDEV_00000092.cif','PDBDEV_00000098.cif','PDBDEV_00000099.cif')
ORDER BY accession_code, "Accession_Serial"
;

-- ===============================================================
-- update database
-- Need to drop unique constraint first
ALTER TABLE "PDB".entry DROP CONSTRAINT "entry_Accession_Serial_primary_key";

-- 30 and 89 are missing!
-- update the legacy entries with new serial number derived from mmcif_file_name. 
UPDATE "PDB".entry e
SET "Accession_Serial" = t.new_serial
FROM
(
SELECT id, accession_code, "Accession_Serial", "Workflow_Status", "Process_Status", "RCT", "mmCIF_File_Name",  
  (regexp_replace("mmCIF_File_Name", '^PDBDEV_([0-9]*).cif', '\1', 'ig'))::int4 as new_serial,
  CASE
    WHEN accession_code IS NOT NULL THEN 'PDBDEV_'||to_char("Accession_Serial" - 54, 'FM00000000')
    ELSE NULL
  END AS new_accession_code
FROM "PDB".entry
WHERE "mmCIF_File_Name" ~ 'PDBDEV'
ORDER BY "mmCIF_File_Name" desc
) AS t
WHERE e.id = t.id
;

-- update the new entries with new serial number and accession_code if already assigned
UPDATE "PDB".entry e
SET "Accession_Serial" = t.new_serial,
  accession_code = t.new_accession_code
FROM
(
SELECT id, accession_code, "Accession_Serial", "Workflow_Status", "Process_Status", "RCT", "mmCIF_File_Name",
  "Accession_Serial" - 65 AS new_serial, 
  CASE
    WHEN accession_code IS NOT NULL THEN 'PDBDEV_'||to_char("Accession_Serial" - 65, 'FM00000000')
    ELSE NULL
  END AS new_accession_code
FROM "PDB".entry
WHERE "RCT" > '2022-05-19' AND "RCT" < '2022-05-26'
  AND NOT "mmCIF_File_Name" ~ 'PDBDEV'
) AS t
WHERE e.id = t.id
;

-- latest entry
UPDATE "PDB".entry e
SET "Accession_Serial" = 121
WHERE "RID" = '2-6C4M'
;
-- ===============================================================
-- clean up duplicates
-- delete 1-Z1Y8 (e.g. "PDBDEV_0000092.cif"), D_1-N1DE (with accession_number = "PDBDEV_0000016") 
SELECT e."RID", structure_id, f."RID", f."File_Format", f."File_Name"
FROM "PDB"."Entry_Related_File" f join "PDB".entry e ON (f.structure_id = e.id)
WHERE e."RID" IN ('1-N1DE','1-N4AY','1-NA4Y','1-NF8W','1-NK7M','1-NQPA','1-NR0J','1-P7V0','1-PBTC','1-RJSW','1-RP1A','1-SE3G','1-Z1Y8')
;

DELETE FROM "PDB"."Entry_Related_File" f
  USING "PDB".entry e 
WHERE f.structure_id = e.id AND e."RID" IN ('1-N1DE','1-N4AY','1-NA4Y','1-NF8W','1-NK7M','1-NQPA','1-NR0J','1-P7V0','1-PBTC','1-RJSW','1-RP1A','1-SE3G','1-Z1Y8')
;

DELETE FROM "PDB"."Entry_Error_File" f
  USING "PDB".entry e 
WHERE f."Entry_RID" = e."RID" AND e."RID" IN ('1-N1DE','1-N4AY','1-NA4Y','1-NF8W','1-NK7M','1-NQPA','1-NR0J','1-P7V0','1-PBTC','1-RJSW','1-RP1A','1-SE3G','1-Z1Y8')
;

-- ('D_1-Z1Y8', 'D_1-N1DE');

DELETE FROM "PDB".entry 
WHERE "RID" IN ('1-N1DE','1-N4AY','1-NA4Y','1-NF8W','1-NK7M','1-NQPA','1-NR0J','1-P7V0','1-PBTC','1-RJSW','1-RP1A','1-SE3G','1-Z1Y8');

-- should have 0 entries
SELECT id, accession_code, "Accession_Serial", "Workflow_Status", "Process_Status", e."RCT", "mmCIF_File_Name", c."Email" AS "RCB", c2."Email" AS "RMB"
FROM "PDB".entry e JOIN public."ERMrest_Client" c ON (e."RCB" = c."ID")
 JOIN public."ERMrest_Client" c2 ON (e."RMB" = c2."ID")
WHERE e."RID" IN ('1-N1DE','1-N4AY','1-NA4Y','1-NF8W','1-NK7M','1-NQPA','1-NR0J','1-P7V0','1-PBTC','1-RJSW','1-RP1A','1-SE3G','1-Z1Y8')
ORDER BY e."RCT"
;

-- reassign the user submitted files
SELECT id, accession_code, "Accession_Serial", "Process_Status", "RCT", "mmCIF_File_Name", t.min_serial
FROM "PDB".entry
LEFT JOIN LATERAL (
  SELECT min("Accession_Serial") AS min_serial, max("Accession_Serial") AS max_serial
  FROM "PDB".entry
  WHERE "RCT" < '2022-05-19' AND NOT id ~ 'PDBDEV' AND NOT "RID" IN ('1-N1DE','1-N4AY','1-NA4Y','1-NF8W','1-NK7M','1-NQPA','1-NR0J','1-P7V0','1-PBTC','1-RJSW','1-RP1A','1-SE3G','1-Z1Y8')
    AND accession_code IS NULL 
) AS t ON TRUE
WHERE "RCT" < '2022-05-19' AND NOT id ~ 'PDBDEV'  AND NOT "RID" IN ('1-N1DE','1-N4AY','1-NA4Y','1-NF8W','1-NK7M','1-NQPA','1-NR0J','1-P7V0','1-PBTC','1-RJSW','1-RP1A','1-SE3G','1-Z1Y8')
   AND accession_code IS NULL
ORDER BY "Accession_Serial" DESC
;

DO $$
  declare
    row record;
    min_serial int4;
  BEGIN
    min_serial := 113;
    FOR row IN
      SELECT "RID", id, "Accession_Serial", "Process_Status", "RCT", "mmCIF_File_Name"
      FROM "PDB".entry
      WHERE "RCT" < '2022-05-19' AND NOT id ~ 'PDBDEV' AND NOT "RID" IN ('1-N1DE','1-N4AY','1-NA4Y','1-NF8W','1-NK7M','1-NQPA','1-NR0J','1-P7V0','1-PBTC','1-RJSW','1-RP1A','1-SE3G','1-Z1Y8') AND accession_code IS NULL
      ORDER BY "RCT"
    LOOP
      RAISE NOTICE 'row:(%, %, %, %)', row."RID", row."Accession_Serial", min_serial, row."RCT";
      UPDATE "PDB".entry SET "Accession_Serial" = min_serial WHERE "RID" = row."RID";
      min_serial := min_serial + 1;
    END LOOP;
  END;
$$;

-- -------------------final check
SELECT id, accession_code, "Accession_Serial", "Process_Status", "RCT", "mmCIF_File_Name" 
FROM "PDB".entry
WHERE NOT "mmCIF_File_Name" ~ 'PDBDEV'
ORDER BY "RCT" 
;

SELECT id, accession_code, "Accession_Serial", "Process_Status", "RCT", "mmCIF_File_Name" 
FROM "PDB".entry
WHERE "mmCIF_File_Name" ~ 'PDBDEV'
ORDER BY "Accession_Serial" 
;

-- ====================================================================
-- set serial column counter
SELECT setval('"PDB"."entry_Accession_Serial_seq"', max("Accession_Serial"))
FROM "PDB".entry;

ALTER TABLE "PDB".entry ADD CONSTRAINT "entry_Accession_Serial_primary_key" UNIQUE("Accession_Serial");

SELECT _ermrest.model_change_event();

COMMIT;







