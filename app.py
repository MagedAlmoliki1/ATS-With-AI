import base64
import time
import streamlit as st
import os
import io
import pdf2image
import groq
from groq import Groq
import fitz  # PyMuPDF
from PIL import Image


client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],
)


import fitz  # PyMuPDF
from PIL import Image
import io
import os



import fitz  # PyMuPDF
import fitz  # PyMuPDF

import textdistance as td





import re

def clean_text(input_text):
    # Remove URLs (websites)
    cleaned_text = re.sub(r'http[s]?://\S+|www\.\S+', '', input_text)
    
    # Remove email addresses
    cleaned_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', '', cleaned_text)
    
    
    # Remove any non-alphanumeric characters (noise), keeping spaces and letters
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', cleaned_text)
    
    # Optional: remove extra spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    return cleaned_text
def match(resume, job_des):
    resume=clean_text(resume)
    job_des=clean_text(job_des)


    
    j = td.jaccard.similarity(resume, job_des)
    s = td.sorensen_dice.similarity(resume, job_des)
    c = td.cosine.similarity(resume, job_des)
    o = td.overlap.normalized_similarity(resume, job_des)
    total = (j + s + c + o) / 4
    # total = (s+o)/2
    return total * 100

def extract_text_from_pdf(file_path):
    """
    Extract text from a multi-page PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the file.
    """
    try:
        # Open the PDF file
        doc = fitz.open(file_path)
        all_text = ""

        # Loop through each page to extract text
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)  # Load the current page
            text = page.get_text()  # Extract text from the page
            # Append the text to the result with a separator for each page
            all_text += f"\n--- Page {page_num + 1} ---\n{text}"  

        # Close the PDF file
        doc.close()

        return all_text  # Return the extracted text
    except Exception as e:
        # Handle errors and return an error message
        return f"An error occurred: {e}"





client = Groq()
from groq import Groq

client = Groq()

from groq import Groq

def analyze_resume_with_groq(resume_analysis_prompt):
    """
   
    """
    client = Groq()

    # استدعاء Groq API مع البرمبت المعدل
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a helpful ATS."
            },
            {
                "role": "user",
                "content": resume_analysis_prompt,
            }
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )

    return chat_completion.choices[0].message.content





    



def save_uploaded_file(uploaded_file, folder_name):
    """
    Save the uploaded file to a specified folder.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)  # Create the folder if it doesn't exist

    file_path = os.path.join(folder_name, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path

    

## Streamlit App

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )



st.set_page_config(page_title="ATS Resume EXpert")
icon("📄")

st.header("ATS Tracking System",divider="rainbow", anchor=False)


input_job=st.text_area("Job Description: ",key="input",value='Job Description\n')

uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    # Save the uploaded PDF file
    pdf_path = save_uploaded_file(uploaded_file, "cv_pdf")
    st.info(f"PDF file saved in folder: '{'cv_pfd/'+pdf_path}'.")
    print(pdf_path)
    input_resume=extract_text_from_pdf(pdf_path)
    print(input_resume)

    

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improvise my Skills")
submit3 = st.button("Percentage(%) Match")

input_prompt1 = f"""
You are a professional and experienced ATS (Applicant Tracking System) with a deep understanding of resume analysis and job description alignment. Your task is to extract and analyze detailed information from the provided resume content. Focus exclusively on the provided text without adding external content. The output should include both structured data extraction and a detailed alignment analysis.

**Task 1: Extract Structured Data**
Extract the following fields from the resume:
- "resume_data": The summary content of the resume.
- "entities": Named entities mentioned in the resume (e.g., names, organizations, titles, etc.).
- "extracted_keywords": Key terms and skills explicitly mentioned in the resume.
- "keyterms": Unique and essential terms related to the job field.
- "name": The candidate's full name as found in the resume.
- "experience": A list of experiences, roles, and responsibilities.
- "emails": Any email addresses mentioned in the resume.
- "phones": Any phone numbers mentioned in the resume.
- "years": Specific years mentioned (e.g., for job roles or education).
- "skills": A list of skills explicitly mentioned in the resume.
- "bi_grams": Common two-word phrases found in the resume.
- "tri_grams": Common three-word phrases found in the resume.
- "pos_frequencies": Frequency of parts of speech (e.g., nouns, verbs, etc.).

**Task 2: Resume Analysis and Alignment with Job Description**
Provide a detailed analysis of how the resume aligns with the job description, following the structure below:

1. **Overview**: Summarize the resume's general focus and areas of expertise.
2. **Strengths**: Highlight key skills, experiences, or achievements that strongly align with the job description.
3. **Relevant Experiences**: Analyze specific roles or accomplishments mentioned in the resume and discuss their relevance to the job description.
4. **Alignment Gaps**: Identify any potential gaps or areas where the resume could better match the job description.

Here is the resume content: {input_resume}
Here is the job description: {input_job}

"""


input_prompt2 = """
You are a professional and experienced ATS(Application Tracking System) with a deep understanding of fields. Based on the analysis of the resume and the job description, suggest specific improvements and additions to the candidate's skill set (200-300 words). Identify areas where the candidate falls short and recommend actionable steps or resources for acquiring or enhancing the necessary skills. Highlight the importance of these skills in the context of the targeted job role.
                    

                    Your Response Should have the following structure
                    Example:
                    
                    Note: Only Mention and Analyze the content of the provided resume text. Make sure Nothing additional is added outside the provided text 
                    
                    Skills Improvement and Addition Suggestions:

                    To further align your resume with the job requirements and the evolving trends in software engineering, consider the following improvements:

                    Expand Knowledge in Emerging Technologies:
                    - Dive into Machine Learning and Big Data Analytics; consider online courses or projects that demonstrate practical application.
                    - Familiarize yourself with Blockchain Technology, given its growing impact on secure and decentralized systems.
                    
                    Enhance Cloud Computing Skills:
                    - Gain deeper expertise in cloud services beyond AWS, such as Microsoft Azure or Google Cloud Platform, to showcase versatility.
                    - Strengthen Soft Skills:
                    Leadership and project management skills are highly valued; consider leading more projects or taking courses in Agile and Scrum methodologies.
                    Here is the resume content : {input_resume}
                    Here is the job description : {input_job}.
                   
"""
input_prompt3 = """
You are a professional and experienced ATS(Application Tracking System) focused exclusively on the {role} field. Your task is to evaluate the resume strictly based on the provided job description and resume content. It is critical to only identify and list the keywords and phrases that have a direct match between the resume and the JD. Highlight any crucial keywords or skills required for the job that are absent in the resume. Based on your analysis, provide a percentage match.

                    Important: Your analysis must strictly adhere to the content provided below. Do not infer or add any keywords, skills, or technologies not explicitly mentioned in these texts. Re-evaluate the texts to ensure accuracy. Recheck before you provide your response

                    Resume Content: {input_resume}.
                    Job Description: {input_job}
                    
                    Never provide anything which is neither present in resume content nor job description.
                    
                    Output should strictly follow this structure:

                    Percentage Match: [Provide percentage]

                    Matched Keywords:
                    - Skills: [List only the matched skills found in both the job description and resume content. recheck before you provide your response]
                    - Technologies: [List only the matched technologies found in both the job description and resume. Recheck before you provide your response]
                    - Methodologies: [List only the matched methodologies found in both the job description and resume. Recheck before you provide your response]

                    Missing Keywords:
                    - [List the skills or technologies crucial for the role found in the job description but not in the resume. Recheck before you provide your response]

                   




"""

if submit1:
    print(input_prompt1)
    # Tell Me About the Resume
    if uploaded_file is not None:
        response=analyze_resume_with_groq(input_prompt1)
        st.subheader("The Repsonse is")
        st.write(response)
        print(response)
    else:
        st.write("Please uplaod the resume")
if submit2:
    # How Can I Improvise my Skills
    if uploaded_file is not None:
        response=analyze_resume_with_groq(input_prompt2)
        st.subheader("The Repsonse is")
        st.write(response)
        print(response)
    else:
        st.write("Please uplaod the resume")
if submit3:    
    # Percentage(%) Match
    if uploaded_file is not None:
        

        response=analyze_resume_with_groq(input_prompt1)
        st.subheader("The Repsonse is")
        match=match(response,input_job)
        # Show loading spinner
        with st.spinner("Calculating match..."):
                time.sleep(2)  # Simulate processing time
                match_percentage = match
        st.success(f"The match percentage is: {match_percentage:.2f}%")
    else:
        st.write("Please uplaod the resume")
