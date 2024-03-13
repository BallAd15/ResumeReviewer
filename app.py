from flask import Flask, render_template, url_for, request, redirect
import openai
import fitz  # PyMuPDF
from docx import Document
import logging

logging.basicConfig(level=logging.ERROR)

openai.api_key = "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"

app = Flask(__name__) # Just referencing this file

# Create an index route - so that when we browse to the url, we don't immediately just 404
@app.route('/', methods=['POST', 'GET']) # Instead of GET by default, now we can also use POST and send data to our database
def index():
  if request.method == "POST":
    resume_file = request.files["resume"]
    filename = resume_file.filename
    file_format = filename.rsplit('.', 1)[-1].lower()  # Extract the file extension and convert to lowercase
    resume_text = extract_text(resume_file, file_format)
    #return render_template('feedback.html', feedback=resume_text)
    chatgpt_feedback = generateFeedback(resume_text)
    return chatgpt_feedback

  else:
    # Render the HTML form
    return render_template("index.html")

def extract_text(resume_file, file_format):
   if file_format == "pdf": 
      # Using PyMuPDF
      pdf_text = extract_text_from_pdf(resume_file)
      return pdf_text
   elif file_format == "doc" or file_format == "docx": 
      # Using python-docx
      doc_text = extract_text_from_doc(resume_file)
      return doc_text
   else:
      return "Unsupported file format. Please upload a PDF or DOC/DOCX file."

def extract_text_from_pdf(resume_file):
    pdf_text = ""
    try:
        with fitz.open(stream=resume_file.read(), filetype="pdf") as pdf_doc:
            for page in pdf_doc:
                pdf_text += page.get_text()
        return pdf_text
    except Exception as e:
        return f"Error occurred while processing PDF: {str(e)}"

def extract_text_from_doc(resume_file):
    doc_text = ""
    try:
        doc = Document(resume_file)
        for paragraph in doc.paragraphs:
            doc_text += paragraph.text + '\n'
        return doc_text
    except Exception as e:
        return f"Error occurred while processing DOC/DOCX: {str(e)}"

def generateFeedback(resume_text):
    prompt = f"This is a resume for a Software Development Engineer position. Please provide feedback on clarity, keyword optimization, and tailoring to the role. \n {resume_text}"
    try:
      response = openai.Completion.create(
          engine="gpt-3.5-turbo-instruct",  # Adjust engine as needed
          prompt=prompt,
          max_tokens=1024,  # Adjust maximum response length
          n=1,
          stop=None,
          temperature=0.7,  # Adjust temperature for creativity
      )
      chatgpt_feedback = response.choices[0].text.strip()
      return f"Resume uploaded successfully! Feedback from ChatGPT: {chatgpt_feedback}"
    except openai.APIError as e:
      # Handle potential errors during API interaction
      return f"An error occurred: {e}"
    
if __name__ == "__main__":
    app.run(debug=True) # debug=True so that if there are any errors, we can see them on the webpage
