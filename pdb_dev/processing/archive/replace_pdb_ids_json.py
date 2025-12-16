#!/usr/bin/env python3
"""
Script to replace four-letter PDB IDs with extended PDB IDs in JSON files.

Replaces PDB IDs in:
- Main dictionary keys (4-letter PDB IDs starting with a digit and containing at least one letter)
- File paths in sub-level keys (values containing filenames)

Usage:
    python3 replace_pdb_ids_json.py -i input.json.gz -o output.json.gz
"""

import argparse
import gzip
import json
import re
import sys
from pathlib import Path


def is_pdb_id(value):
    """
    Check if a value is a 4-letter PDB ID starting with a digit and containing at least one letter.
    
    Examples: 8ZZ1, 8ZZ8, 1ABC (valid)
              ABCD, 1234 (invalid - must start with digit and have at least one letter)
    """
    if not value or not isinstance(value, str):
        return False
    
    value = value.strip()
    # Must be exactly 4 characters, start with a digit, be alphanumeric, and contain at least one letter
    return (len(value) == 4 and
            value[0].isdigit() and
            value.isalnum() and
            any(c.isalpha() for c in value))


def convert_pdb_id(pdb_id):
    """
    Convert a 4-character PDB ID to extended format.
    
    Example: 8ZZ1 -> pdb_00008zz1
            8ZZ8 -> pdb_00008zz8
    """
    if not pdb_id or len(pdb_id) != 4:
        return pdb_id
    
    # Convert to lowercase and zero-pad to 8 characters
    pdb_lower = pdb_id.lower()
    pdb_padded = pdb_lower.zfill(8)
    return f"pdb_{pdb_padded}"


def replace_pdb_id_in_path(path, old_pdb_id, new_pdb_id):
    """
    Replace PDB ID in a file path.
    
    Replaces both uppercase and lowercase versions of the PDB ID.
    """
    if not isinstance(path, str):
        return path
    
    # Replace lowercase version
    path = path.replace(old_pdb_id.lower(), new_pdb_id)
    # Replace uppercase version
    path = path.replace(old_pdb_id.upper(), new_pdb_id)
    # Replace original case if different
    if old_pdb_id != old_pdb_id.lower() and old_pdb_id != old_pdb_id.upper():
        path = path.replace(old_pdb_id, new_pdb_id)
    
    return path


def process_json_data(data):
    """
    Process JSON data to replace PDB IDs in keys and values.
    
    Returns a new dictionary with replaced PDB IDs.
    """
    if not isinstance(data, dict):
        return data
    
    new_data = {}
    
    for key, value in data.items():
        # Check if the key is a PDB ID
        if is_pdb_id(key):
            # Convert the key
            new_key = convert_pdb_id(key)
            
            # Process the value recursively
            new_value = process_value(value, key, new_key)
            
            new_data[new_key] = new_value
        else:
            # Key is not a PDB ID, but value might contain PDB IDs in paths
            new_value = process_value(value, None, None)
            new_data[key] = new_value
    
    return new_data


def process_value(value, old_pdb_id, new_pdb_id):
    """
    Process a value recursively, replacing PDB IDs in file paths.
    
    Args:
        value: The value to process (can be dict, list, str, etc.)
        old_pdb_id: The original PDB ID to replace (if processing a PDB ID entry)
        new_pdb_id: The new extended PDB ID (if processing a PDB ID entry)
    """
    if isinstance(value, dict):
        return {k: process_value(v, old_pdb_id, new_pdb_id) for k, v in value.items()}
    elif isinstance(value, list):
        return [process_value(item, old_pdb_id, new_pdb_id) for item in value]
    elif isinstance(value, str):
        # Only replace PDB IDs in strings that contain .gz (file paths)
        if '.gz' not in value:
            return value
        
        # If we have a PDB ID context, replace it in the string
        if old_pdb_id and new_pdb_id:
            return replace_pdb_id_in_path(value, old_pdb_id, new_pdb_id)
        else:
            # Check if the string contains a PDB ID pattern and replace it
            # Look for 4-character patterns that match PDB ID format in file paths
            def replace_pdb_in_string(s):
                # Pattern to match 4-character PDB IDs in paths (lowercase, alphanumeric)
                # This will match patterns like /8zz1/ or 8zz1.cif.gz
                pattern = r'\b([0-9][a-z0-9]{3})\b'
                def replacer(match):
                    potential_pdb = match.group(1)
                    if is_pdb_id(potential_pdb):
                        return convert_pdb_id(potential_pdb)
                    return potential_pdb
                return re.sub(pattern, replacer, s, flags=re.IGNORECASE)
            
            return replace_pdb_in_string(value)
    else:
        return value


def process_json_file(input_path, output_path):
    """
    Process a gzipped JSON file and replace PDB IDs.
    """
    # Read input file
    try:
        with gzip.open(input_path, 'rt', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        raise
    
    # Process the data
    new_data = process_json_data(data)
    
    # Write output file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with gzip.open(output_path, 'wt', encoding='utf-8') as f:
            json.dump(new_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        raise


def main():
    """Main function to process JSON files with command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Replace four-letter PDB IDs with extended PDB IDs in JSON files.'
    )
    parser.add_argument('-i', '--input', required=True, help='Input JSON.gz file')
    parser.add_argument('-o', '--output', required=True, help='Output JSON.gz file')

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Process the file
    try:
        process_json_file(input_path, output_path)
        print(f"Successfully processed {input_path} -> {output_path}")
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

