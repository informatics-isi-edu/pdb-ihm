BEGIN;

-- before insert
CREATE OR REPLACE FUNCTION "PDB".entry_trigger_before_insert() RETURNS trigger LANGUAGE plpgsql 
AS $function$
DECLARE
  accession_serial_last_value integer;
BEGIN
  NEW.id := 'D_' || NEW."RID";
  IF NEW."Submitter_Flag" IS NULL OR  NEW."Submitter_Flag" = 'false' THEN
     NEW."Submitter_Flag_Date" := NULL;
  END IF;

  IF NEW."Image_File_Name" IS NULL THEN
     NEW."Image_File_Name" := 'missing_image.png';
     NEW."Image_File_Bytes" := 35406;
     NEW."Image_File_URL" := '/hatrac/pdb/public/images/missing_image.png:SFJRT3MNZVDH55UY33CYR7FCD4';
     NEW."Image_File_MD5" := '27994cb72f6d4780d9b09a85b9b5ac50';
  END IF;
  RETURN NEW;
END; 
$function$;

DROP TRIGGER IF EXISTS entry_trigger_before_insert ON "PDB"."entry";
CREATE TRIGGER entry_trigger_before_insert
BEFORE INSERT ON "PDB"."entry"
FOR EACH ROW EXECUTE PROCEDURE "PDB".entry_trigger_before_insert();

-- ---------------------------------------------------------------------------
-- before update
CREATE OR REPLACE FUNCTION "PDB".entry_trigger_before_update() RETURNS trigger LANGUAGE plpgsql
AS $function$
DECLARE
  reset_process_status boolean;
BEGIN
  reset_process_status := false;
  
  IF NEW."Image_File_Name" IS NULL THEN
     NEW."Image_File_Name" := 'missing_image.png';
     NEW."Image_File_Bytes" := 35406;
     NEW."Image_File_URL" := '/hatrac/dev/pdb/public/images/missing_image.png:UTV3DLUONOXGI7D73RFIQMG6XU';
     NEW."Image_File_MD5" := '27994cb72f6d4780d9b09a85b9b5ac50';
  END IF;
  
  IF NEW."Submitter_Flag" IS NULL OR  NEW."Submitter_Flag" IS FALSE
  THEN
    NEW."Submitter_Flag_Date" := NULL;
  END IF;


  -- The mmcif file content has changed (note: assuming that md5 is not null), trigger processing workflow
  -- If submitter forgets to reset Workflow_Status, reset to DEPO.
  -- If curators forgets to reset, ignore (let them fix it themselves)
  IF coalesce(OLD."mmCIF_File_MD5", '') != coalesce(NEW."mmCIF_File_MD5", '')
  THEN
    NEW."Last_mmCIF_File_MD5" := OLD."mmCIF_File_MD5";
    IF NEW."Manual_Processing" IS FALSE AND New."Workflow_Status" = 'ERROR'
       AND OLD."Process_Status" in ('Error: generating mmCIF file', 'Error: processing uploaded mmCIF file')
    THEN
       NEW."Workflow_Status" = 'DEPO';
       reset_process_status := TRUE;
    END IF;
  END IF; -- file_md5

  -- if workflow status has changed
  IF reset_process_status
     OR ( OLD."Workflow_Status" != NEW."Workflow_Status"
       AND NEW."Workflow_Status" IN ('DEPO', 'SUBMIT', 'SUBMISSION COMPLETE', 'RELEASE READY')
       AND NEW."Manual_Processing" IS FALSE
     )
  THEN
     NEW."Record_Status_Detail" := NULL;
     IF OLD."Workflow_Status" = 'ERROR' THEN
        NEW."Process_Status" := 'Reprocess (trigger backend process after Error)';
     ELSE
        NEW."Process_Status" := 'Resume (trigger backend process)';
     END IF;
  END IF;
  RETURN NEW;

END;
$function$;

DROP TRIGGER IF EXISTS entry_trigger_before_update ON "PDB"."entry";
CREATE TRIGGER entry_trigger_before_update
BEFORE UPDATE ON "PDB"."entry"
FOR EACH ROW EXECUTE PROCEDURE "PDB".entry_trigger_before_update();

-- ==================================================================================

CREATE OR REPLACE FUNCTION "PDB".entry_related_file_trigger_before_update() RETURNS trigger LANGUAGE plpgsql
AS $function$
BEGIN
  IF ((OLD."File_MD5" IS NULL) AND (NEW."File_MD5" IS NOT NULL)) OR ((OLD."File_MD5" IS NOT NULL) AND (NEW."File_MD5" IS  NULL)) OR (OLD."File_MD5" != NEW."File_MD5")
  THEN
    IF OLD."Restraint_Workflow_Status" = 'ERROR'
    THEN
      NEW."Restraint_Process_Status" := 'Reprocess (trigger backend process after Error)';
    ELSE
      NEW."Restraint_Process_Status" := 'New (trigger backend process)';
    END IF;
   
    NEW."Record_Status_Detail" := NULL;

    IF OLD."Restraint_Workflow_Status" != 'ERROR' AND OLD."File_MD5" IS NOT NULL AND NEW."File_MD5" IS NOT NULL AND OLD."File_MD5" != NEW."File_MD5"
    THEN
      NEW."Restraint_Process_Status" := 'Resume (trigger backend process)';
    END IF;
    RETURN NEW;
  END IF;
  
  IF NEW."Restraint_Process_Status" like 'In progress:%'
  THEN
    NEW."Record_Status_Detail" := NULL;
  RETURN NEW;
  END IF;

  IF OLD."Restraint_Workflow_Status" != NEW."Restraint_Workflow_Status"
  THEN
    IF NEW."Restraint_Workflow_Status" != 'ERROR'
    THEN
      NEW."Record_Status_Detail" := NULL;
    END IF;
    
    IF NEW."Restraint_Workflow_Status" IN ('DEPO', 'SUBMIT')
    THEN
      IF OLD."Restraint_Workflow_Status" = 'ERROR'
      THEN
        NEW."Restraint_Process_Status" := 'Reprocess (trigger backend process after Error)';
      ELSE
        NEW."Restraint_Process_Status" := 'Resume (trigger backend process)';
      END IF;
    END IF;
  END IF;

  RETURN NEW;
END;
$function$;

DROP TRIGGER IF EXISTS entry_related_file_trigger_before_update ON "PDB"."Entry_Related_File";
CREATE TRIGGER entry_related_file_trigger_before_update
BEFORE UPDATE ON "PDB"."Entry_Related_File"
FOR EACH ROW EXECUTE PROCEDURE "PDB".entry_related_file_trigger_before_update();

-- ==================================================================================
CREATE OR REPLACE FUNCTION "PDB".accession_code_trigger_before_update() RETURNS trigger LANGUAGE plpgsql
AS $function$
BEGIN
  IF OLD."Entry" IS NOT NULL AND OLD."Entry" != NEW."Entry" THEN
    RAISE EXCEPTION 'Entry value is not allowed to be updated';
    RETURN OLD;
  END IF;
  RETURN NEW;
END;
$function$;

DROP TRIGGER IF EXISTS accession_code_trigger_before_update ON "PDB"."Accession_Code";
CREATE TRIGGER accession_code_trigger_before_update
BEFORE UPDATE ON "PDB"."Accession_Code"
FOR EACH ROW EXECUTE PROCEDURE "PDB".accession_code_trigger_before_update();


COMMIT;
