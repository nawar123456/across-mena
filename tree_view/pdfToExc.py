import pdfplumber
import pandas as pd

pdf_path = "pdfcommercialnames.pdf"
excel_path = "output.xlsx"

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

# Save to Excel with proper encoding
df.to_excel(excel_path, index=False)

print(f"✅ Arabic text extracted successfully and saved as {excel_path}")
