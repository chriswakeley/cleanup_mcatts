#!/usr/bin/env python3
import pandas as pd
import sys
import argparse

def remove_statenm_column(input_file, output_file):
    """
    Remove the statenm column from a CSV file.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to save the output CSV file
    """
    try:
        # Load the CSV file
        print(f"Loading {input_file}...")
        df = pd.read_csv(input_file)
        
        # Check if statenm column exists
        if 'statenm' not in df.columns:
            print("Warning: 'statenm' column not found in the input file.")
            return
        
        # Remove the statenm column
        print("Removing 'statenm' column...")
        df = df.drop(columns=['statenm'])
        
        # Save the modified dataframe to a new CSV file
        df.to_csv(output_file, index=False)
        print(f"Modified data saved to {output_file}")
        
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove statenm column from CSV file')
    parser.add_argument('-i', '--input', required=True, 
                        help='Path to input CSV file (e.g., updated_mcatts_no-accents.csv)')
    parser.add_argument('-o', '--output', 
                        help='Path to output CSV file (if not specified, will add "_no_statenm" suffix)')
    
    args = parser.parse_args()
    
    # If output file not specified, create one based on input filename
    if not args.output:
        input_name = args.input.rsplit('.', 1)[0]  # Remove extension
        args.output = f"{input_name}_no_statenm.csv"
    
    remove_statenm_column(args.input, args.output) 