from flask import Flask, render_template, url_for, request, redirect
import google.generativeai as genai
import fitz  # PyMuPDF
from docx import Document
import logging
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

logging.basicConfig(level=logging.ERROR)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__) # Just referencing this file

# Create an index route - so that when we browse to the url, we don't immediately just 404
@app.route('/', methods=['POST', 'GET']) # Instead of GET by default, now we can also use POST and send data to our database
def index():
  if request.method == "POST":
    resume_file = request.files["resume"]
    filename = resume_file.filename
    file_format = filename.rsplit('.', 1)[-1].lower()  # Extract the file extension and convert to lowercase
    resume_text = extract_text(resume_file, file_format)
    gemini_feedback = generateFeedback(resume_text)

    formatted_feedback = format_response(gemini_feedback)

    return render_template('feedback.html', feedback=formatted_feedback)

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
    # Set up the model
    generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
    
    convo = model.start_chat()

    convo.send_message(prompt)

    feedback = convo.last.text
    return feedback

def format_response(input_text):
    feedback_dict = {}
    current_category = None

    lines = input_text.split("\n")
    for line in lines:
            if line == '':
                    pass
            elif line.startswith("**"):
                    feedback_dict[line[2:-2]] = []
                    current_category = line[2:-2]
            else:
                    feedback_dict[current_category].append(line[1:].replace("*",""))    
    return feedback_dict
    
if __name__ == "__main__":
    app.run(debug=True) # debug=True so that if there are any errors, we can see them on the webpage
