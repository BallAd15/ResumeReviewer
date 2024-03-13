<h1 id="resume-reviewer">Resume Reviewer</h1>
<p>This application allows you to upload your resume in the pdf/doc format. The application evaluates it and provides feedback on the same.</p>
<h2 id="setup">Setup</h2>
<p>Clone the repository</p>
<blockquote>
<p>git clone <a href="https://github.com/BallAd15/ResumeReviewer">https://github.com/BallAd15/ResumeReviewer</a></p>
</blockquote>
<p>Fetch an API Key, and store in a .env file</p>
<blockquote>
<p><a href="https://ai.google.dev/">https://ai.google.dev/</a></p>
</blockquote>
<p>Install dependencies</p>
<blockquote>
<p>pip install -r requirements.txt</p>
</blockquote>
<p>Build the app</p>
<blockquote>
<p>python app.py</p>
</blockquote>
<h2 id="application">Application</h2>
<h3 id="1-application-framework">1. Application Framework</h3>
<p>Flask was used as the backend framework, and HTML/CSS was used for the frontend.
The functionality to upload the file was created here</p>
<h3 id="2--data-extraction">2.  Data Extraction</h3>
<p>The data from the documents uploaded was extracted using the following methods:</p>
<ul>
<li><strong>.pdf : PyMuPDF</strong><ul>
<li>PyMuPDF is a Python library that provide functionalities for reading, manipulating, and extracting data from PDF documents.</li>
</ul>
</li>
<li><strong>.doc/.docx : python-docx</strong><ul>
<li>python-docx is a Python library for creating and manipulating Microsoft Word (.docx) files. It provides a high-level interface for working with Word documents.</li>
</ul>
</li>
</ul>
<h3 id="3-generate-feedback">3. Generate Feedback</h3>
<p>The extracted text was fed to the Google Gemini API, (GenAI) to receive a feedback.</p>
<ul>
<li>The Google Gemini API (GenAI) provides powerful natural language processing (NLP) capabilities that can significantly enhance the resume review process.</li>
<li>These include Semantic Understanding, Keyword Extraction, Sentiment Analysis, Clarity Assessment</li>
</ul>
<h3 id="4-formatting-the-response">4. Formatting the Response</h3>
<p>The response received from GenAI isn&#39;t in a format which can be displayed easily on a webpage. Hence various parsing techniques were used, so it&#39;s easier for the flask template engine, Jinja to render the page</p>
