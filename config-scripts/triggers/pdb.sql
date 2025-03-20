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
$function$

DROP TRIGGER IF EXISTS entry_trigger_before_insert ON "PDB"."entry";
CREATE TRIGGER entry_trigger_before_insert
BEFORE INSERT ON "PDB"."entry"
FOR EACH ROW EXECUTE PROCEDURE "PDB".entry_trigger_before_insert();

-- before update
CREATE OR REPLACE FUNCTION "PDB".entry_trigger_before_update() RETURNS trigger LANGUAGE plpgsql
AS $function$
BEGIN

  IF NEW."Image_File_Name" IS NULL THEN
    NEW."Image_File_Name" := 'missing_image.png';
    NEW."Image_File_Bytes" := 35406;
    NEW."Image_File_URL" := '/hatrac/dev/pdb/public/images/missing_image.png:UTV3DLUONOXGI7D73RFIQMG6XU';
    NEW."Image_File_MD5" := '27994cb72f6d4780d9b09a85b9b5ac50';
  END IF;
  
  IF NEW."Submitter_Flag" IS NULL OR  NEW."Submitter_Flag" = 'false'
  THEN
    NEW."Submitter_Flag_Date" := NULL;
  END IF;

  IF ( (OLD."mmCIF_File_MD5" IS NULL) AND (NEW."mmCIF_File_MD5" IS NOT NULL) ) OR
     ( (OLD."mmCIF_File_MD5" IS NOT NULL) AND (NEW."mmCIF_File_MD5" IS NULL) ) OR
     ( OLD."mmCIF_File_MD5" != NEW."mmCIF_File_MD5" )
  THEN
    NEW."Record_Status_Detail" := NULL;
    IF NEW."Manual_Processing" = 'false'
    THEN
      IF OLD."Workflow_Status" = 'ERROR'
      THEN
      	 NEW."Process_Status" := 'Reprocess (trigger backend process after Error)';
      ELSE
      	 NEW."Process_Status" := 'New (trigger backend process)';
      END IF;

      IF OLD."Workflow_Status" != 'ERROR' AND OLD."mmCIF_File_MD5" IS NOT NULL AND NEW."mmCIF_File_MD5" IS NOT NULL AND OLD."mmCIF_File_MD5" != NEW."mmCIF_File_MD5"
      THEN
        NEW."Process_Status" := 'Resume (trigger backend process)';
      END IF;
    END IF;
    RETURN NEW;
  END IF;
  
  IF NEW."Process_Status" like 'In progress:%'
  THEN
    NEW."Record_Status_Detail" := NULL;
    RETURN NEW;
  END IF;

  IF OLD."Workflow_Status" != NEW."Workflow_Status"
  THEN
    IF NEW."Workflow_Status" != 'ERROR'
    THEN
      NEW."Record_Status_Detail" := NULL;
    END IF;
    IF NEW."Workflow_Status" IN ('DEPO', 'SUBMIT', 'SUBMISSION COMPLETE', 'RELEASE READY')
    THEN
      IF NEW."Manual_Processing" = 'false'
      THEN
        IF OLD."Workflow_Status" = 'ERROR'
	THEN
          NEW."Process_Status" := 'Reprocess (trigger backend process after Error)';
      	ELSE
          NEW."Process_Status" := 'Resume (trigger backend process)';
      	END IF;
      END IF;
    END IF;
  END IF;
  RETURN NEW;

END;
$function$

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
$function$

DROP TRIGGER IF EXISTS entry_related_file_trigger_before_update ON "PDB"."Entry_Related_File";
CREATE TRIGGER entry_related_file_trigger_before_update
BEFORE UPDATE ON "PDB"."Entry_Related_File"
FOR EACH ROW EXECUTE PROCEDURE "PDB".entry_related_file_trigger_before_update()

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
$function$

DROP TRIGGER IF EXISTS accession_code_trigger_before_update ON "PDB"."Accession_Code";
CREATE TRIGGER accession_code_trigger_before_update
BEFORE UPDATE ON "PDB"."Accession_Code"
FOR EACH ROW EXECUTE PROCEDURE "PDB".accession_code_trigger_before_update()


COMMIT;
