import streamlit as st
import re
import io

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# ---------- TEXT EXTRACTION ----------

def extract_text(uploaded_file):
    file_name = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()

    # PDF
    if file_name.endswith(".pdf"):
        try:
            import fitz

            document = fitz.open(stream=file_bytes, filetype="pdf")

            # First try normal text extraction
            text = "\n".join(page.get_text() for page in document).strip()

            # If PDF has little/no text, try OCR
            if len(re.sub(r"\s+", "", text)) < 80:
                try:
                    import pytesseract
                    from PIL import Image

                    ocr_text = []

                    for page in document:
                        pix = page.get_pixmap(
                            matrix=fitz.Matrix(2, 2),
                            alpha=False
                        )

                        img = Image.frombytes(
                            "RGB",
                            [pix.width, pix.height],
                            pix.samples
                        )

                        page_text = pytesseract.image_to_string(img)

                        if page_text.strip():
                            ocr_text.append(page_text)

                    text = "\n".join(ocr_text).strip()

                except Exception:
                    pass

            document.close()
            return text

        except Exception:
            return ""

    # DOCX
    elif file_name.endswith(".docx"):
        try:
            from docx import Document

            document = Document(io.BytesIO(file_bytes))

            paragraphs = [
                paragraph.text.strip()
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]

            return "\n".join(paragraphs)

        except Exception:
            return ""

    return ""


# ---------- ANALYSIS ----------

def analyze_resume(text):
    text_lower = text.lower()

    # Skills
    skills = [
        "python", "java", "javascript", "html", "css",
        "sql", "excel", "powerpoint", "word",
        "communication", "leadership", "teamwork",
        "problem solving", "data analysis", "machine learning",
        "artificial intelligence", "project management",
        "marketing", "research", "management",
        "c++", "c#", "php", "react", "node.js",
        "git", "github", "aws", "docker", "tableau"
    ]

    found_skills = [
        skill for skill in skills
        if re.search(r"\b" + re.escape(skill) + r"\b", text_lower)
    ]

    # Sections
    education_words = [
        "education", "qualification", "degree",
        "bachelor", "master", "school", "college",
        "university", "b.tech", "bba", "mba"
    ]

    experience_words = [
        "experience", "work experience",
        "employment", "internship", "worked",
        "professional experience"
    ]

    project_words = [
        "project", "projects"
    ]

    certification_words = [
        "certification", "certificate",
        "certifications", "certified"
    ]

    summary_words = [
        "summary", "objective", "profile",
        "career objective", "professional summary"
    ]

    contact_words = [
        "email", "phone", "mobile", "linkedin"
    ]

    education_found = any(word in text_lower for word in education_words)
    experience_found = any(word in text_lower for word in experience_words)
    projects_found = any(word in text_lower for word in project_words)
    certifications_found = any(word in text_lower for word in certification_words)
    summary_found = any(word in text_lower for word in summary_words)

    email_found = bool(
        re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text_lower)
    )

    phone_found = bool(
        re.search(r"\b\d{10}\b", text_lower)
    )

    linkedin_found = "linkedin" in text_lower

    contact_score = 0

    if email_found:
        contact_score += 2

    if phone_found:
        contact_score += 2

    if linkedin_found:
        contact_score += 1

    # ---------- SCORING ----------

    education_score = 15 if education_found else 0

    # More skills = higher score, but capped
    skill_score = min(len(found_skills) * 2.5, 20)

    experience_score = 20 if experience_found else 0

    project_score = 15 if projects_found else 0

    certification_score = 10 if certifications_found else 0

    summary_score = 5 if summary_found else 0

    # Content quality based on text length
    word_count = len(text_lower.split())

    if word_count >= 500:
        content_score = 10
    elif word_count >= 300:
        content_score = 7
    elif word_count >= 150:
        content_score = 4
    else:
        content_score = 1

    score = round(
        education_score
        + skill_score
        + experience_score
        + project_score
        + certification_score
        + summary_score
        + contact_score
        + content_score
    )

    score = min(score, 100)

    return {
        "score": score,
        "skills": found_skills,
        "education": education_found,
        "experience": experience_found,
        "projects": projects_found,
        "certifications": certifications_found,
        "summary": summary_found,
        "email": email_found,
        "phone": phone_found,
        "linkedin": linkedin_found,
        "word_count": word_count
    }


# ---------- UI ----------

st.title("🤖 AI Resume Analyzer")

st.write(
    "Upload your resume and get an automated analysis "
    "based on skills, education, experience, projects and certifications."
)

st.divider()

resume = st.file_uploader(
    "📄 Upload your Resume",
    type=["pdf", "docx"]
)

if resume is not None:

    st.success("Resume uploaded successfully! ✅")

    with st.spinner("🔍 Reading and analyzing your resume..."):
        text = extract_text(resume)

    if not text.strip():

        st.error(
            "❌ I couldn't read the text from this file. "
            "Please try another PDF or DOCX file."
        )

    else:

        result = analyze_resume(text)

        st.subheader("📊 Resume Analysis")

        st.metric(
            "Resume Score",
            f"{result['score']}/100"
        )

        st.divider()

        st.write("### 🔍 Analysis")

        if result["education"]:
            st.write("✅ Education section detected")
        else:
            st.write("❌ Education section missing")

        if result["experience"]:
            st.write("✅ Experience section detected")
        else:
            st.write("⚠️ Experience section missing")

        if result["projects"]:
            st.write("✅ Projects section detected")
        else:
            st.write("⚠️ Projects section missing")

        if result["certifications"]:
            st.write("✅ Certifications detected")
        else:
            st.write("⚠️ Certifications not detected")

        if result["summary"]:
            st.write("✅ Professional summary/objective detected")
        else:
            st.write("⚠️ Professional summary/objective missing")

        st.write("### 📞 Contact Information")

        if result["email"]:
            st.write("✅ Email detected")
        else:
            st.write("⚠️ Email not detected")

        if result["phone"]:
            st.write("✅ Phone number detected")
        else:
            st.write("⚠️ Phone number not detected")

        if result["linkedin"]:
            st.write("✅ LinkedIn detected")
        else:
            st.write("⚠️ LinkedIn not detected")

        st.write("### 🛠️ Skills Detected")

        if result["skills"]:
            st.write(", ".join(result["skills"]))
        else:
            st.write("No common skills detected.")

        st.write("### 📄 Resume Content")

        st.write(
            f"Approximately **{result['word_count']} words** detected."
        )

        st.write("### 💡 Suggestions")

        suggestions = []

        if not result["education"]:
            suggestions.append("Add a clear Education section.")

        if len(result["skills"]) < 5:
            suggestions.append("Add more relevant skills.")

        if not result["experience"]:
            suggestions.append(
                "Add work experience or internship details if applicable."
            )

        if not result["projects"]:
            suggestions.append("Add academic or personal projects.")

        if not result["certifications"]:
            suggestions.append(
                "Add relevant certifications if you have them."
            )

        if not result["summary"]:
            suggestions.append(
                "Add a professional summary or career objective."
            )

        if not result["email"]:
            suggestions.append("Add a professional email address.")

        if not result["phone"]:
            suggestions.append("Add a contact phone number.")

        if suggestions:
            for suggestion in suggestions:
                st.write("• " + suggestion)
        else:
            st.write(
                "🎉 Your resume contains the major sections!"
            )

else:
    st.info("Please upload a PDF or DOCX resume to begin.")
