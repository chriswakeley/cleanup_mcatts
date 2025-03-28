#!/usr/bin/env python3
import pandas as pd
import sys

def update_legislator_data(mcatts_file, legislators_file, output_file):
    """
    Update mcatts_caucus data with matching entries from legislators-no-accents data.
    
    Args:
        mcatts_file (str): Path to mcatts_caucus CSV file
        legislators_file (str): Path to legislators-no-accents CSV file
        output_file (str): Path to save the updated CSV file
    """
    try:
        # Load the CSV files
        print(f"Loading {mcatts_file}...")
        mcatts_df = pd.read_csv(mcatts_file)
        
        print(f"Loading {legislators_file}...")
        legislators_df = pd.read_csv(legislators_file)
        
        # Make a copy of the original data for comparison
        mcatts_updated = mcatts_df.copy()
        
        # Track non-matching entries
        non_matches = []
        
        # Iterate through each row in the mcatts dataframe
        print("Processing entries...")
        for index, row in mcatts_df.iterrows():
            # Find the matching entry in legislators dataframe
            match = legislators_df[(legislators_df['id'] == row['id']) & 
                                   (legislators_df['congress'] == row['cong'])]
            
            if not match.empty:
                # Update the name, state, and statenm columns
                mcatts_updated.at[index, 'mc.name'] = match.iloc[0]['name']
                mcatts_updated.at[index, 'state'] = match.iloc[0]['state']
                mcatts_updated.at[index, 'statenm'] = match.iloc[0]['state']
            else:
                # Add to non-matches list
                non_matches.append((row['id'], row['cong'], row['mc.name']))
        
        # Print non-matching entries
        if non_matches:
            print("\nThe following entries in mcatts_caucus had no match in legislators-no-accents:")
            print("ID, Congress, Name")
            print("-" * 40)
            for entry in non_matches:
                print(f"{entry[0]}, {entry[1]}, {entry[2]}")
            print(f"Total non-matches: {len(non_matches)}")
        else:
            print("All entries were successfully matched.")
        
        # Save the updated dataframe to a new CSV file
        mcatts_updated.to_csv(output_file, index=False)
        print(f"\nUpdated data saved to {output_file}")
        
    except Exception as e:
        print(f"Error processing files: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Update legislator data by matching entries between two CSV files')
    parser.add_argument('--mcatts', required=True, help='Path to mcatts_caucus_103_116.csv file')
    parser.add_argument('--legislators', required=True, help='Path to legislators-no-accents.csv file')
    parser.add_argument('--output', required=True, help='Path to save the updated CSV file')
    
    args = parser.parse_args()
    
    update_legislator_data(args.mcatts, args.legislators, args.output) 