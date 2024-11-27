import base64
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

def convert_pdf_to_images(pdf_path, output_dir='cv_img'):
    """
    Converts each page of a PDF to an image and returns the paths of the saved images.

    Args:
    - pdf_path (str): Path to the PDF file.
    - output_dir (str): Directory where the images will be saved.

    Returns:
    - List of image paths (str).
    """
    image_paths = []  # List to store the paths of saved images

    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)

        # Check if the output directory exists, create it if not
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Loop through each page of the PDF
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)

            # Convert the page to a pixmap (image) at 300 dpi resolution
            pix = page.get_pixmap(dpi=300)  # 300 dpi resolution

            # Convert the pixmap to image data (in ppm format)
            img_data = pix.tobytes("ppm")
            img = Image.open(io.BytesIO(img_data))  # Load into PIL Image

            # Save the image as a JPG file
            image_path = os.path.join(output_dir, f"page_{page_num + 1}.jpg")
            img.save(image_path, "JPEG")

            # Add the image path to the list
            image_paths.append(image_path)

        # Return the list of image paths
        return image_paths

    except Exception as e:
        print(f"Error occurred: {e}")
        return 1



client = Groq()
def evaluate_resume(pdf_content, prompt):
    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    # Encode the input image
    base64_image = encode_image(pdf_content)

    # Initialize the Groq client
    client = Groq()

    # Create the chat completion request
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
    model="llama-3.2-11b-vision-preview",
    )
    
    # Return the result
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


role = st.text_input("**What's the Job Role?**",value='Machine Learning Engineer')

input_text=st.text_area("Job Description: ",key="input",value='Job Description\n')

uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    # Save the uploaded PDF file
    pdf_path = save_uploaded_file(uploaded_file, "cv_pdf")
    st.info(f"PDF file saved in folder: '{'cv_pfd/'+pdf_path}'.")
    

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improvise my Skills")
submit3 = st.button("Percentage(%) Match")

input_prompt1 = """
 You are a professional and experienced ATS(Application Tracking System) with a deep understanding of {role} fields. Analyze the provided resume and job description (JD). Provide a detailed analysis (200-300 words) of how the resume aligns with the JD, highlighting key areas of strength, relevant experiences, and qualifications. Discuss any notable achievements or skills that are particularly well-matched to the job requirements.
                    
                    Here is the resume content : the  image
                    Here is the job description : {input_text}
                    Your Response Should have the following structure
                    Example:
                    
                    Note: Only Mention and Analyze the content of the provided resume text. Make sure Nothing additional is added outside the provided text 
                    
                    Resume Analysis and Alignment with Job Description:

                    Overview: 
                    The resume presents a strong background in software engineering, with a particular emphasis on full-stack development and cloud technologies.
                    
                    Strengths:
                    - Technical Proficiency: Proficient in key programming languages such as Python, JavaScript, and Java, aligning well with the job's technical requirements.
                    - Project Experience: Showcases several projects that demonstrate the ability to design, develop, and deploy scalable software solutions, mirroring the JD's emphasis on hands-on experience.
                    
                    Relevant Experiences: (Highlight only the things that are present in the resume.)
                    - Lead Developer Role: Led a team in developing a SaaS application using microservices architecture, directly relevant to the job's focus on leadership and microservices.
                    - Cloud Solutions Architect: Experience in designing cloud infrastructure on AWS, aligning with the JD's requirement for cloud computing skills.
                    

"""

input_prompt2 = """
You are a professional and experienced ATS(Application Tracking System) with a deep understanding of {role} fields. Based on the analysis of the resume and the job description, suggest specific improvements and additions to the candidate's skill set (200-300 words). Identify areas where the candidate falls short and recommend actionable steps or resources for acquiring or enhancing the necessary skills. Highlight the importance of these skills in the context of the targeted job role.
                    
                    Here is the resume content : the image.
                    Here is the job description : {input_text}
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
                   
"""
input_prompt3 = """
You are a professional and experienced ATS(Application Tracking System) focused exclusively on the {role} field. Your task is to evaluate the resume strictly based on the provided job description and resume content. It is critical to only identify and list the keywords and phrases that have a direct match between the resume and the JD. Highlight any crucial keywords or skills required for the job that are absent in the resume. Based on your analysis, provide a percentage match.

                    Important: Your analysis must strictly adhere to the content provided below. Do not infer or add any keywords, skills, or technologies not explicitly mentioned in these texts. Re-evaluate the texts to ensure accuracy. Recheck before you provide your response

                    Resume Content: the image.
                    Job Description: {input_text}
                    
                    Never provide anything which is neither present in resume content nor job description.
                    
                    Output should strictly follow this structure:

                    Percentage Match: [Provide percentage]

                    Matched Keywords:
                    - Skills: [List only the matched skills found in both the job description and resume content. recheck before you provide your response]
                    - Technologies: [List only the matched technologies found in both the job description and resume. Recheck before you provide your response]
                    - Methodologies: [List only the matched methodologies found in both the job description and resume. Recheck before you provide your response]

                    Missing Keywords:
                    - [List the skills or technologies crucial for the role found in the job description but not in the resume. Recheck before you provide your response]

                    Final Thoughts:
                    - [Provide a brief assessment focusing on the alignment, matched keywords, missing elements, and percentage match. Reinforce the instruction to only mention elements present in the provided texts. Recheck before you provide your response]




"""

if submit1:
    # Tell Me About the Resume
    if uploaded_file is not None:
        pdf_contens=convert_pdf_to_images(pdf_path)
        response=evaluate_resume(pdf_contens[0],input_prompt1)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
if submit2:
    # How Can I Improvise my Skills
    if uploaded_file is not None:
        pdf_contens=convert_pdf_to_images(pdf_path)
        response=evaluate_resume(pdf_contens[0],input_prompt2)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
if submit3:    
    # Percentage(%) Match
    if uploaded_file is not None:
        pdf_contens=convert_pdf_to_images(pdf_path)
        response=evaluate_resume(pdf_contens[0],input_prompt3)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
