# Summary

A Python script that processes and cleans MCATTS legislator data by updating names and states, removing accents from text fields, and cleaning up unnecessary columns.

This utility script performs several data cleaning operations on legislator data files:

1. Updates legislator names and state information using a reference dataset
2. Removes accent marks from all text fields while preserving capitalization
3. Removes unnecessary columns (specifically 'statenm')

To run this script:

Save the code above as a Python file (e.g., update_legislator_data.py).

Make sure you have pandas installed (pip install pandas).

Run it from your terminal, providing the required file paths:

python update_legislator_data.py --mcatts ./mcatts_caucus_103_116.csv --legislators ./HSall_members.csv --output ./final_output.csv

HSall_members.csv is sourced from https://voteview.com/data