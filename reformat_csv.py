import csv

def reformat_csv(input_file, output_file):
    with open(input_file, encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)

        for row in reader:
            # Wrap every cell in quotes and add empty columns for ,,, style
            row_with_padding = row + ["", "", ""]  # Add 3 empty columns
            writer.writerow(row_with_padding)

    print(f"✅ Saved: {output_file}")

# 👇 Change the filenames as needed
reformat_csv('syrian_tarrif test9 txt.txt', 'ttxt.csv')
