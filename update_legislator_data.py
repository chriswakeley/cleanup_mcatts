#!/usr/bin/env python3
import pandas as pd
import unicodedata
import sys
import argparse

# --- Function from remove_accents.py ---
def remove_accents(text):
    """
    Remove accents from input text while preserving capitalization.

    Args:
        text (str): Input text with accented characters

    Returns:
        str: Text with accents removed, capitalization preserved
    """
    if not isinstance(text, str): # Handle non-string data gracefully
        return text
    try:
        # Normalize the text to decompose accented characters (NFKD)
        normalized_text = unicodedata.normalize('NFKD', text)
        # Remove all diacritical marks (combining characters)
        result = ''.join([c for c in normalized_text if not unicodedata.combining(c)])
        return result
    except Exception as e:
        print(f"Warning: Could not remove accents from '{text}': {e}", file=sys.stderr)
        return text # Return original text on error

# --- Main processing function combining all steps ---
def process_legislator_pipeline(mcatts_file, legislators_file, output_file):
    """
    Performs the legislator data processing pipeline:
    1. Update mcatts data using legislator data.
    2. Remove accents from all text fields in the updated data.
    3. Remove the 'statenm' column.
    
    Args:
        mcatts_file (str): Path to the initial mcatts_caucus CSV file.
        legislators_file (str): Path to the legislators CSV file (should already have accents removed).
        output_file (str): Path to save the final processed CSV file.
    """
    try:
        # === Step 1: Update legislator data (from update_legislator_data.py) ===
        print(f"Step 1: Loading {mcatts_file}...")
        mcatts_df = pd.read_csv(mcatts_file)

        print(f"Step 1: Loading {legislators_file}...")
        # Assume legislators file already has accents removed as per original script names
        legislators_df = pd.read_csv(legislators_file)

        # Create a copy to modify
        mcatts_updated = mcatts_df.copy()

        # Track non-matching entries
        non_matches = []

        print("Step 1: Updating mc.name and state using legislator data...")
        # Optimize lookup by setting index on legislators_df
        legislators_df.set_index(['icpsr', 'congress'], inplace=True)

        for index, row in mcatts_updated.iterrows():
            lookup_key = (row['id'], row['cong'])
            try:
                # Use .loc for efficient index-based lookup
                match = legislators_df.loc[lookup_key]
                # If match is found (no KeyError), update the row
                # Handle potential multiple matches (shouldn't happen with id/cong key)
                # by taking the first one if it's a DataFrame, or directly if it's a Series
                if isinstance(match, pd.DataFrame):
                    match_data = match.iloc[0]
                else: # It's a Series
                    match_data = match

                mcatts_updated.at[index, 'mc.name'] = match_data['bioname']
                mcatts_updated.at[index, 'state'] = match_data['state_abbrev']
                # Ensure statenm is also copied over if present, for Step 3 consistency
                if 'statenm' in match_data:
                     mcatts_updated.at[index, 'statenm'] = match_data['statenm']

            except KeyError:
                # Add to non-matches list if lookup fails
                non_matches.append((row['id'], row['cong'], row['mc.name']))

        # Print non-matching entries
        if non_matches:
            print("\nStep 1: The following entries in mcatts_caucus had no match in legislators:")
            print("ID, Congress, Name")
            print("-" * 40)
            for entry in non_matches:
                print(f"{entry[0]}, {entry[1]}, {entry[2]}")
            print(f"Total non-matches: {len(non_matches)}")
        else:
            print("Step 1: All entries were successfully matched or updated.")
        
        # The result of Step 1 is the mcatts_updated DataFrame
        df_step1_output = mcatts_updated
        print("Step 1: Update complete.")

        # === Step 2: Remove accents (from remove_accents.py) ===
        print("\nStep 2: Removing accents from all text fields...")
        # Apply remove_accents function element-wise to the entire DataFrame
        # It will only affect string elements due to the check inside remove_accents
        df_step2_output = df_step1_output.applymap(remove_accents)
        print("Step 2: Accent removal complete.")

        # === Step 3: Remove statenm column (from remove_statenm_column.py) ===
        print("\nStep 3: Removing 'statenm' column...")
        df_step3_output = df_step2_output.copy() # Work on a copy

        if 'statenm' not in df_step3_output.columns:
            print("Step 3: Warning: 'statenm' column not found. Skipping removal.")
        else:
            # Remove the statenm column
            df_step3_output = df_step3_output.drop(columns=['statenm'])
            print("Step 3: 'statenm' column removed.")

        # === Final Step: Save the result ===
        print(f"\nSaving final processed data to {output_file}...")
        df_step3_output.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Successfully saved final output to {output_file}")

    except FileNotFoundError as e:
        print(f"Error: Input file not found - {e}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
         print(f"Error: Missing expected column in input file - {e}. Please check CSV headers.", file=sys.stderr)
         sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}", file=sys.stderr)
        sys.exit(1)

# --- Command-line argument parsing ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process legislator data: Update names/states, remove accents, and remove statenm column.'
    )
    parser.add_argument(
        '--mcatts',
        required=True,
        help='Path to the initial mcatts_caucus CSV file (e.g., mcatts_caucus_103_116.csv)'
    )
    parser.add_argument(
        '--legislators',
        required=True,
        help='Path to the legislators CSV file (e.g., legislators-no-accents.csv)'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Path to save the final processed CSV output file.'
    )

    args = parser.parse_args()

    # Run the combined processing pipeline
    process_legislator_pipeline(args.mcatts, args.legislators, args.output)