
# ATS Resume Expert 📝

ATS Resume Expert is a Streamlit-based application designed to analyze resumes against job descriptions using advanced language models. The app helps users identify strengths, improvement areas, and alignment percentage between resumes and job descriptions.

---

## Features
- **PDF to Image Conversion**: Converts PDF resumes into images for processing.
- **Resume Analysis**: Analyzes the resume based on the job description and provides feedback.
- **Skill Improvement Suggestions**: Suggests specific areas for skill development.
- **Match Percentage**: Calculates and displays the percentage match between resume and job description.

---

## Installation Guide

Follow these steps to set up and run the project locally:

### 1. Clone the Repository
```bash
git clone <repository_url>
cd <repository_name>
```

### 2. Create a Virtual Environment
Create an isolated environment for the project:
```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
- On Linux/macOS:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

### 4. Install Dependencies
Install all the required Python packages:
```bash
pip install -r requirements.txt
```

---

## Dependencies

The application requires the following Python libraries:

- `streamlit`: For creating the web interface.
- `python-dotenv`: For managing environment variables securely.
- `pdf2image`: For converting PDF pages into images.
- `base64`: For encoding images.
- `os`: For handling file operations.
- `io`: For handling input/output streams.
- `Pillow`: For working with image data.
- `groq`: For leveraging the Groq API for AI-driven analysis.
- `PyMuPDF (fitz)`: For working with PDF files.

Ensure these dependencies are included in the `requirements.txt` file.

---

## Configuration

### 1. Set Up Environment Variables
Create a `.streamlit/secrets.toml` file in the project root and add your **Groq API Key**:
```toml
[secrets]
GROQ_API_KEY = "<your_api_key>"
```

---

## Running the Application

Once everything is set up, run the application using Streamlit:
```bash
streamlit run app.py
```

---

## Usage

1. Open the application in your web browser.
2. Select a model from the dropdown list.
3. Input the job role and job description.
4. Upload your resume (in PDF format).
5. Click the desired action button:
   - **Tell Me About the Resume**: Get a detailed analysis.
   - **How Can I Improve My Skills**: Receive skill enhancement suggestions.
   - **Percentage Match**: View the percentage alignment between resume and job description.

---

## Directory Structure

```
├── app.py                   # Main application file
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── .streamlit/
│   └── secrets.toml         # Contains API keys and secrets
└── cv_img/                  # Folder for storing converted images
```

---

## Contributions

Contributions are welcome! Feel free to fork the repository, make improvements, and create pull requests.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Author

Created by **[MagedAlmoliki1]**.
