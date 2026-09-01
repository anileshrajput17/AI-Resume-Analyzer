import streamlit as st

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("🤖 AI Resume Analyzer")
st.write("Upload your resume and get a quick AI-powered analysis.")

st.divider()

resume = st.file_uploader(
    "📄 Upload your Resume",
    type=["pdf", "docx"]
)

if resume is not None:
    st.success("Resume uploaded successfully! ✅")

    st.subheader("📊 Resume Analysis")

    score = 75

    st.metric("Resume Score", f"{score}/100")

    st.write("### 🔍 Analysis")

    st.write("✅ Education section detected")
    st.write("✅ Skills section detected")
    st.write("⚠️ Experience section needs improvement")
    st.write("⚠️ Add more relevant projects")

    st.write("### 💡 Suggestions")

    st.write("• Add more relevant skills")
    st.write("• Include projects and certifications")
    st.write("• Improve your professional summary")

else:
    st.info("Please upload a PDF or DOCX resume to begin.")
