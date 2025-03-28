#!/usr/bin/env python3
import unicodedata
import csv
import argparse
import sys

def remove_accents(text):
    """
    Remove accents from input text while preserving capitalization.
    
    Args:
        text (str): Input text with accented characters
        
    Returns:
        str: Text with accents removed, capitalization preserved
    """
    # Normalize the text to decompose accented characters
    # NFKD decomposition will separate base characters from diacritical marks
    normalized_text = unicodedata.normalize('NFKD', text)
    
    # Remove all diacritical marks (combining characters)
    # This regex matches all non-spacing marks (category "Mn" in Unicode)
    result = ''.join([c for c in normalized_text if not unicodedata.combining(c)])
    
    return result

def process_csv(input_file, output_file):
    """
    Process a CSV file by removing accents from all text fields.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
    """
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
             open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            
            for row in reader:
                # Process each field in the row
                processed_row = [remove_accents(field) for field in row]
                writer.writerow(processed_row)
                
        print(f"Successfully processed {input_file} and saved results to {output_file}")
    except Exception as e:
        print(f"Error processing CSV file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove accents from text while preserving capitalization')
    parser.add_argument('-i', '--input', help='Input CSV file')
    parser.add_argument('-o', '--output', help='Output CSV file')
    parser.add_argument('--examples', action='store_true', help='Show examples')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    # Process CSV if input and output files are provided
    if args.input and args.output:
        process_csv(args.input, args.output)
    
    # Show examples if requested or if no other options are specified
    if args.examples or (not args.input and not args.output and not args.interactive):
        sample_texts = [
            "Café", 
            "naïve",
            "Résumé",
            "Façade",
            "GRÖSSE",
            "Niño",
            "Åland",
            "Søren Kierkegård"
        ]
        
        print("Original | Without Accents")
        print("-" * 30)
        
        for text in sample_texts:
            print(f"{text} | {remove_accents(text)}")
    
    # Run interactive mode if requested
    if args.interactive or (not args.input and not args.output and not args.examples):
        print("\nEnter text to remove accents (or press Ctrl+C to exit):")
        try:
            while True:
                user_input = input("> ")
                if not user_input:
                    continue
                print(remove_accents(user_input))
        except KeyboardInterrupt:
            print("\nExiting...") 