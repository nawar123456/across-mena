import pdfplumber
import pandas as pd

pdf_path = "pdfcommercialnames.pdf"
csv_path = "output.csv"  # Save as CSV for better Arabic support

data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            lines = text.split("\n")  # Split text into lines
            for line in lines:
                data.append([line])  # Store as list (1 column per row)

# Convert extracted data into a DataFrame
df = pd.DataFrame(data, columns=["Arabic Text"])

# Save as CSV with UTF-8 encoding
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print(f"✅ Arabic text extracted successfully and saved as {csv_path}")
