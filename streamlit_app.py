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

    if file_name.endswith(".pdf"):
        try:
            import fitz
            document = fitz.open(stream=file_bytes, filetype="pdf")
            text = "\n".join(page.get_text() for page in document)
            document.close()
            return text
        except Exception:
            return ""

    elif file_name.endswith(".docx"):
        try:
            from docx import Document
            document = Document(io.BytesIO(file_bytes))
            text = "\n".join(paragraph.text for paragraph in document.paragraphs)
            return text
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
        "marketing", "research", "management"
    ]

    found_skills = [skill for skill in skills if skill in text_lower]

    # Sections
    education_words = [
        "education", "qualification", "degree",
        "bachelor", "master", "school", "college"
    ]

    experience_words = [
        "experience", "work experience",
        "employment", "internship", "worked"
    ]

    project_words = [
        "project", "projects"
    ]

    certification_words = [
        "certification", "certificate", "certifications"
    ]

    summary_words = [
        "summary", "objective", "profile"
    ]

    education_found = any(word in text_lower for word in education_words)
    experience_found = any(word in text_lower for word in experience_words)
    projects_found = any(word in text_lower for word in project_words)
    certifications_found = any(word in text_lower for word in certification_words)
    summary_found = any(word in text_lower for word in summary_words)

    # ---------- SCORING ----------

    education_score = 15 if education_found else 0

    skill_score = min(len(found_skills) * 3, 25)

    experience_score = 20 if experience_found else 0

    project_score = 15 if projects_found else 0

    certification_score = 10 if certifications_found else 0

    keyword_score = min(len(found_skills) * 1.5, 15)

    score = round(
        education_score
        + skill_score
        + experience_score
        + project_score
        + certification_score
        + keyword_score
    )

    # Bonus for professional summary
    if summary_found:
        score = min(score + 5, 100)

    return {
        "score": score,
        "skills": found_skills,
        "education": education_found,
        "experience": experience_found,
        "projects": projects_found,
        "certifications": certifications_found,
        "summary": summary_found
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

    with st.spinner("🔍 Analyzing your resume..."):
        text = extract_text(resume)

    if not text.strip():

        st.error(
            "❌ I couldn't read the text from this file. "
            "Please upload a text-based PDF or DOCX file."
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

        st.write("### 🛠️ Skills Detected")

        if result["skills"]:
            st.write(", ".join(result["skills"]))
        else:
            st.write("No common skills detected.")

        st.write("### 💡 Suggestions")

        suggestions = []

        if not result["education"]:
            suggestions.append("Add a clear Education section.")

        if len(result["skills"]) < 5:
            suggestions.append("Add more relevant skills.")

        if not result["experience"]:
            suggestions.append("Add work experience or internship details.")

        if not result["projects"]:
            suggestions.append("Add academic or personal projects.")

        if not result["certifications"]:
            suggestions.append("Add relevant certifications if you have them.")

        if not result["summary"]:
            suggestions.append("Add a professional summary or career objective.")

        if suggestions:
            for suggestion in suggestions:
                st.write("• " + suggestion)
        else:
            st.write("🎉 Your resume contains all the major sections!")

else:
    st.info("Please upload a PDF or DOCX resume to begin.")
