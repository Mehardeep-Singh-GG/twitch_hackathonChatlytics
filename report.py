import google.generativeai as genai
# Specify the file path
file_path = 'stream_data.txt'

# Open the file and read its contents into a string
with open(file_path, 'r', encoding='utf-8') as file:
    text_data = file.read()

# Display the contents as a string
print(text_data)
file_path = 'summary.txt.txt'

# Open the file and read its contents into a string
with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()

# Display the contents as a string

genai.configure(api_key="AIzaSyAGt_AHHj4dyhAJTN7h1BiBE8b92_wUVA8")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(f"create an indetail report of this to judge how a persons stream went {data}{text_data} aalso give a grate to it out of 10")
gg = response.text()

from fpdf import FPDF

# Create a PDF class instance
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Set font
pdf.set_font("Arial", size=12)
# Add string to the PDF
for line in gg.split('\n'):
    pdf.cell(200, 10, txt=line, ln=True)

# Save the PDF to a file
pdf.output("report.pdf")

print("PDF created successfully!")

