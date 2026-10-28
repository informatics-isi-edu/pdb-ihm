#!/usr/bin/env python3
"""
Script to replace four-symbol PDB IDs with extended PDB IDs in IHMCIF files.

Replaces PDB IDs in:
- data_ block
- _entry.id field
- _struct.entry_id field
- _pdbx_database_status.entry_id field
- Any field ending with .entry_id
- Any loop with entry_id field
- Any loop with _struc. or _pdbx. prefix containing entry_id

Does NOT replace in _database_2 loop.

Usage:
    python3 replace_pdb_ids.py -i input.cif -o output.cif [-d diff_file]

    If -d is not specified, diff is written to stdout.
"""

import argparse
import gzip
import os
import re
import sys
from pathlib import Path
from collections import namedtuple


PDBComparison = namedtuple('PDBComparison', [
    'line_num', 'field_name', 'original_string', 'output_string', 'changed'
])


def convert_pdb_id(pdb_id):
    """
    Convert a 4-character PDB ID to extended format.

    Example: 8ZZ1 -> pdb_00008zz1
    """
    if not pdb_id or len(pdb_id) != 4:
        return pdb_id

    # Convert to lowercase and zero-pad to 8 characters
    pdb_lower = pdb_id.lower()
    pdb_padded = pdb_lower.zfill(8)
    return f"pdb_{pdb_padded}"


def is_pdb_id(value):
    """Check if a value is a 4-character PDB ID (must start with a digit and have at least one letter)."""
    if not value:
        return False
    value = value.strip()
    # Remove quotes if present
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    elif value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    # PDB IDs are 4 characters, must start with a digit, have at least one letter, rest alphanumeric
    return (len(value) == 4 and
            value[0].isdigit() and
            value.isalnum() and
            any(c.isalpha() for c in value))


def is_pdb_id_simple(value):
    """Check if a value is a 4-character PDB ID (alphanumeric) - simpler version for replacement."""
    if not value:
        return False
    value = value.strip()
    # PDB IDs are 4 characters, alphanumeric
    return len(value) == 4 and value.isalnum()


def read_file_lines(filepath):
    """Read file lines with encoding fallback."""
    
    if not filepath.exists():
        print(f"Error: Input file '{filepath.name}' does not exist", file=sys.stderr)        
        raise Exception(f"Error: Input file '{filepath.name}' does not exist")

    if filepath.name.endswith(".gz"):
        # Try UTF-8 first, fall back to latin-1 if needed
        try:
            with gzip.open(filepath, 'rt', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            # Fall back to latin-1 which can decode any byte
            with gzip.open(filepath, 'rt', encoding='latin-1') as f:
                lines = f.readlines()
    elif filepath.name.endswith(".cif"):
        # Try UTF-8 first, fall back to latin-1 if needed
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            # Fall back to latin-1 which can decode any byte
            with open(filepath, 'r', encoding='latin-1') as f:
                lines = f.readlines()
    else:
        raise Exception(f"ERROR: unknown file extension: {filepath.name}")

    return lines


def extract_field_name(line):
    """Extract the field name from a CIF line."""
    if line.startswith('_'):
        match = re.match(r'^(_[^\s]+)', line)
        if match:
            return match.group(1)
    elif line.startswith('data_'):
        return "data_ block"
    return ""


def find_pdb_ids_in_line(line, line_num):
    """
    Find all PDB IDs in a line and return their positions and context.
    Returns list of (start_pos, end_pos, pdb_id, context)
    """
    pdb_ids = []

    # Skip lines that are ONLY field names (no value after the field name)
    if line.startswith('_'):
        # Check if this is a field name with a value (has whitespace after field name)
        if not re.search(r'^_[^\s]+\s+', line):
            # This is a field name only (no value), skip it
            return pdb_ids
        # If it has a value, extract the value part and only search there
        field_match = re.match(r'^(_[^\s]+)\s+(.*)$', line)
        if field_match:
            field_name = field_match.group(1)
            value_part = field_match.group(2)
            # Only search in the value part, not the field name
            search_text = value_part
            field_name_offset = len(field_name) + 1  # +1 for the space
        else:
            search_text = line
            field_name_offset = 0
    else:
        search_text = line
        field_name_offset = 0

    # Pattern to match 4-character PDB IDs (must start with a digit)
    pattern = r'(?:^|[^A-Z0-9])([0-9][A-Z0-9]{3})(?=[^A-Z0-9]|$)'

    for match in re.finditer(pattern, search_text, re.IGNORECASE):
        pdb_id = match.group(1)
        if is_pdb_id(pdb_id):
            # Adjust position if we're searching only in the value part
            start_pos = match.start(1) + field_name_offset
            end_pos = match.end(1) + field_name_offset

            # Extract context
            context = ""
            if line.startswith('_'):
                field_match = re.match(r'^(_[^\s]+)', line)
                if field_match:
                    context = field_match.group(1)
            elif line.startswith('data_'):
                context = "data_ block"
            else:
                context_start = max(0, start_pos - 30)
                context_end = min(len(line), end_pos + 30)
                context = line[context_start:context_end].strip()

            pdb_ids.append((start_pos, end_pos, pdb_id, context))

    return pdb_ids


def create_pdb_comparison(input_filepath, output_filepath, diff_output):
    """
    Create a detailed comparison showing all PDB ID occurrences.
    Writes to diff_output (file handle or stdout).
    """
    input_path = Path(input_filepath)
    output_path = Path(output_filepath)
    
    input_lines = read_file_lines(input_path)
    output_lines = read_file_lines(output_path)

    comparisons = []
    seen_lines = set()
    in_atom_site_loop = False

    max_lines = max(len(input_lines), len(output_lines))

    for line_num in range(1, max_lines + 1):
        input_line = input_lines[line_num - 1] if line_num <= len(input_lines) else ""
        output_line = output_lines[line_num - 1] if line_num <= len(output_lines) else ""

        # Check if we're entering an _atom_site loop
        if input_line.strip() == 'loop_':
            in_atom_site_loop = False
            for next_line_num in range(line_num, min(line_num + 50, len(input_lines))):
                next_line = input_lines[next_line_num].strip()
                if next_line.startswith('_atom_site.'):
                    in_atom_site_loop = True
                    break
                elif next_line and not next_line.startswith('_'):
                    break

        # Check if current line is an _atom_site field header
        if input_line.startswith('_atom_site.'):
            in_atom_site_loop = True

        # Check if we're in an _atom_site loop and should skip
        if in_atom_site_loop:
            if input_line.strip() == 'loop_':
                continue
            elif input_line.startswith('_') and not input_line.startswith('_atom_site.'):
                in_atom_site_loop = False
            elif input_line.strip() == '' or input_line.startswith('#'):
                for next_line_num in range(line_num, min(line_num + 10, len(input_lines))):
                    next_line = input_lines[next_line_num].strip()
                    if next_line and not next_line.startswith('#'):
                        if not next_line.startswith('_atom_site.') and not (next_line.startswith('ATOM ') or next_line.startswith('HETATM ')):
                            in_atom_site_loop = False
                        break
                if in_atom_site_loop:
                    continue
            else:
                continue

        # Skip lines containing ATOM or HETATM
        if re.search(r'\bATOM\b', input_line, re.IGNORECASE) or re.search(r'\bHETATM\b', input_line, re.IGNORECASE):
            continue

        # Find all PDB IDs in input line
        input_pdb_ids = find_pdb_ids_in_line(input_line, line_num)

        if not input_pdb_ids:
            continue

        # Find PDB IDs in corresponding output line
        output_pdb_ids = find_pdb_ids_in_line(output_line, line_num) if output_line else []

        # Extract field name from input line
        field_name = extract_field_name(input_line)
        if not field_name and input_line.strip():
            if input_line.strip().startswith('data_'):
                field_name = "data_ block"
            else:
                line_preview = input_line.strip()[:40]
                if len(input_line.strip()) > 40:
                    field_name = f"{line_preview}..."
                else:
                    field_name = line_preview

        # For each PDB ID in input, try to find corresponding one in output
        for in_start, in_end, in_pdb_id, in_context in input_pdb_ids:
            matched = False
            out_pdb_id = None

            for out_start, out_end, out_pdb_id_candidate, out_context in output_pdb_ids:
                pos_match = abs(in_start - out_start) < 10
                context_match = (in_context and out_context and
                                in_context[:20] == out_context[:20])

                if pos_match or context_match:
                    out_pdb_id = out_pdb_id_candidate
                    matched = True
                    break

            # If no match found, check if this is a known transformation
            if not matched:
                extended_pattern = rf'pdb_0+{in_pdb_id.lower()}'
                if re.search(extended_pattern, output_line, re.IGNORECASE):
                    out_pdb_id = re.search(extended_pattern, output_line, re.IGNORECASE).group(0)
                    matched = True

            # Determine if changed
            if matched:
                changed = (in_pdb_id.upper() != out_pdb_id.upper())
            else:
                original_string = input_line.rstrip('\n')
                output_string = output_line.rstrip('\n') if output_line else ""
                if original_string == output_string:
                    changed = False
                else:
                    changed = True
                out_pdb_id = None

            # Create comparison entry
            original_string = input_line.rstrip('\n')
            output_string = output_line.rstrip('\n') if output_line else ""

            # If lines are identical, mark as unchanged
            if original_string == output_string:
                changed = False

            # Create a unique key based on line number and content
            comparison_key = (line_num, original_string, output_string)

            # Only add if we haven't seen this exact line comparison
            if comparison_key not in seen_lines:
                seen_lines.add(comparison_key)
                comparisons.append(PDBComparison(
                    line_num=line_num,
                    field_name=field_name or "unknown",
                    original_string=original_string,
                    output_string=output_string,
                    changed=changed
                ))

    # Write comparison report
    diff_output.write(f"PDB ID Comparison Report\n")
    diff_output.write(f"{'=' * 80}\n")
    diff_output.write(f"Input file:  {input_filepath}\n")
    diff_output.write(f"Output file: {output_filepath}\n")
    diff_output.write(f"{'=' * 80}\n\n")

    if not comparisons:
        diff_output.write("No PDB IDs found in input file.\n")
        return

    # Group by changed/unchanged
    changed_comps = [c for c in comparisons if c.changed]
    unchanged_comps = [c for c in comparisons if not c.changed]

    diff_output.write(f"Summary:\n")
    diff_output.write(f"  Total PDB ID occurrences: {len(comparisons)}\n")
    diff_output.write(f"  Changed: {len(changed_comps)}\n")
    diff_output.write(f"  Unchanged: {len(unchanged_comps)}\n")
    diff_output.write(f"\n{'=' * 80}\n\n")

    # Show changed entries first
    if changed_comps:
        diff_output.write("CHANGED ENTRIES:\n")
        diff_output.write(f"{'=' * 80}\n\n")
        for comp in changed_comps:
            diff_output.write(f"Line {comp.line_num}: {comp.field_name}\n")
            diff_output.write(f"  Original:\n")
            diff_output.write(f"    {comp.original_string}\n")
            diff_output.write(f"  Output:\n")
            diff_output.write(f"    {comp.output_string}\n")
            diff_output.write(f"\n")

    # Show unchanged entries
    if unchanged_comps:
        diff_output.write(f"\n{'=' * 80}\n")
        diff_output.write("UNCHANGED ENTRIES:\n")
        diff_output.write(f"{'=' * 80}\n\n")
        for comp in unchanged_comps:
            line_prefix = f"Line {comp.line_num}: "
            diff_output.write(f"{line_prefix}{comp.original_string}\n")
            diff_output.write(f"\n")


def process_cif_file(input_filepath, output_filepath):
    """Process a single CIF file and replace PDB IDs."""

    input_path = Path(input_filepath)
    output_path = Path(output_filepath)
    
    lines = read_file_lines(input_path)

    output_lines = []
    in_loop = False
    loop_headers = []
    entry_id_column = None
    in_database_2_loop = False
    current_pdb_id = None

    i = 0
    while i < len(lines):
        line = lines[i]
        original_line = line

        # Check for data_ block
        if line.startswith('data_'):
            # Extract PDB ID from data_ block
            match = re.match(r'^data_([A-Z0-9]{4})$', line.strip(), re.IGNORECASE)
            if match:
                pdb_id = match.group(1)
                current_pdb_id = pdb_id
                extended_id = convert_pdb_id(pdb_id)
                line = f"data_{extended_id}\n"

        # Check for _entry.id field
        elif re.match(r'^_entry\.id\s+', line):
            match = re.match(r'^_entry\.id\s+([A-Z0-9]{4})\s*$', line.strip(), re.IGNORECASE)
            if match:
                pdb_id = match.group(1)
                extended_id = convert_pdb_id(pdb_id)
                # Preserve whitespace from original line
                whitespace = re.match(r'^(_entry\.id\s+)', line).group(1)
                line = f"{whitespace}{extended_id}\n"

        # Check for _struct.entry_id field
        elif re.match(r'^_struct\.entry_id\s+', line):
            match = re.match(r'^_struct\.entry_id\s+([A-Z0-9]{4})\s*$', line.strip(), re.IGNORECASE)
            if match:
                pdb_id = match.group(1)
                extended_id = convert_pdb_id(pdb_id)
                # Preserve whitespace
                whitespace = re.match(r'^(_struct\.entry_id\s+)', line).group(1)
                line = f"{whitespace}{extended_id}\n"

        # Check for _pdbx_database_status.entry_id field
        elif re.match(r'^_pdbx_database_status\.entry_id\s+', line):
            match = re.match(r'^_pdbx_database_status\.entry_id\s+([A-Z0-9]{4})\s*$', line.strip(), re.IGNORECASE)
            if match:
                pdb_id = match.group(1)
                extended_id = convert_pdb_id(pdb_id)
                # Preserve whitespace
                whitespace = re.match(r'^(_pdbx_database_status\.entry_id\s+)', line).group(1)
                line = f"{whitespace}{extended_id}\n"

        # Check for any other field ending with .entry_id (like _ihm_entry_collection_mapping.entry_id)
        elif re.match(r'^_[^\.]+\.entry_id\s+', line):
            match = re.match(r'^(_[^\.]+\.entry_id\s+)([A-Z0-9]{4})\s*$', line.strip(), re.IGNORECASE)
            if match:
                field_part = match.group(1)
                pdb_id = match.group(2)
                extended_id = convert_pdb_id(pdb_id)
                # Preserve whitespace from original line
                whitespace_match = re.match(r'^(_[^\.]+\.entry_id\s+)', line)
                if whitespace_match:
                    whitespace = whitespace_match.group(1)
                    line = f"{whitespace}{extended_id}\n"
                else:
                    line = f"{field_part}{extended_id}\n"

        # Check for loop start
        elif line.strip() == 'loop_':
            in_loop = True
            loop_headers = []
            entry_id_column = None
            in_database_2_loop = False

        # Check for loop headers (lines starting with _)
        elif in_loop and line.startswith('_'):
            loop_headers.append(line.strip())

            # Check if this is a _database_2 loop
            if '_database_2.' in line:
                in_database_2_loop = True

            # Check if this is an entry_id field
            if '.entry_id' in line:
                entry_id_column = len(loop_headers) - 1

            # Check if this is a _struc. or _pdbx. loop with entry_id
            if (line.startswith('_struc.') or line.startswith('_pdbx.')) and '.entry_id' in line:
                entry_id_column = len(loop_headers) - 1

        # Check for loop data (non-header, non-comment lines after headers)
        elif in_loop and loop_headers and not line.startswith('#') and line.strip():
            # Check if we're in a loop that should be processed
            if not in_database_2_loop and entry_id_column is not None:
                # Parse CIF line - handle both tab and space separated, with quoted strings
                original_line_stripped = line.rstrip('\n')

                # Use regex to split while preserving quoted strings
                parts = []
                current = ''
                in_quotes = False
                quote_char = None

                for char in original_line_stripped:
                    if char in ('"', "'") and not in_quotes:
                        in_quotes = True
                        quote_char = char
                        current += char
                    elif char == quote_char and in_quotes:
                        in_quotes = False
                        current += char
                        parts.append(current)
                        current = ''
                        quote_char = None
                    elif char in ('\t', ' ') and not in_quotes:
                        if current:
                            parts.append(current)
                            current = ''
                    else:
                        current += char

                if current:
                    parts.append(current)

                # Process entry_id column if it exists
                if entry_id_column < len(parts):
                    value = parts[entry_id_column].strip()
                    # Remove quotes if present
                    unquoted_value = value
                    if value.startswith('"') and value.endswith('"'):
                        unquoted_value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        unquoted_value = value[1:-1]

                    if is_pdb_id_simple(unquoted_value):
                        extended_id = convert_pdb_id(unquoted_value)
                        # Reconstruct the value with original quoting
                        if value.startswith('"') and value.endswith('"'):
                            parts[entry_id_column] = f'"{extended_id}"'
                        elif value.startswith("'") and value.endswith("'"):
                            parts[entry_id_column] = f"'{extended_id}'"
                        else:
                            parts[entry_id_column] = extended_id

                        # Reconstruct line - try to preserve original format
                        if '\t' in original_line_stripped:
                            line = '\t'.join(parts) + '\n'
                        else:
                            line = ' '.join(parts) + '\n'

        # Check for loop end (empty line or comment after data)
        elif in_loop and loop_headers:
            if line.strip() == '' or line.startswith('#'):
                # Check if next non-empty line is not a loop header
                j = i + 1
                while j < len(lines) and lines[j].strip() == '':
                    j += 1
                if j >= len(lines) or (not lines[j].startswith('_') and lines[j].strip() != 'loop_'):
                    in_loop = False
                    loop_headers = []
                    entry_id_column = None
                    in_database_2_loop = False

        output_lines.append(line)
        i += 1

    # Write output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if output_path.name.endswith(".gz"):
        try:
            with gzip.open(output_path, 'wt', encoding='utf-8') as f:
                f.writelines(output_lines)
        except UnicodeEncodeError:
            # Fall back to latin-1 if UTF-8 encoding fails
            with gzip.open(output_path, 'wt', encoding='latin-1') as f:
                f.writelines(output_lines)
    else:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.writelines(output_lines)
        except UnicodeEncodeError:
            # Fall back to latin-1 if UTF-8 encoding fails
            with open(output_path, 'w', encoding='latin-1') as f:
                f.writelines(output_lines)


def main():
    """Main function to process CIF files with command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Replace four-symbol PDB IDs with extended PDB IDs in IHMCIF files.'
    )
    parser.add_argument('-i', '--input', required=True, help='Input CIF file')
    parser.add_argument('-o', '--output', required=True, help='Output CIF file')
    parser.add_argument('-d', '--diff', help='Diff output file (default: stdout)')

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    # Process the file
    try:
        process_cif_file(args.input, args.output)
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate diff if requested
    if args.diff:
        try:
            with open(args.diff, 'w', encoding='utf-8') as diff_file:
                create_pdb_comparison(args.input, args.output, diff_file)
        except Exception as e:
            print(f"Error creating diff: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Write diff to stdout
        create_pdb_comparison(args.input, args.output, sys.stdout)


if __name__ == '__main__':
    main()
