import streamlit as st

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Recruitment System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("📂 Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Resume Screening",
        "Candidate Ranking",
        "Recruiter Dashboard",
        "Explainable AI",
        "About"
    ]
)

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------

if page == "Home":

    st.title("🤖 Explainable AI-Powered Recruitment Decision Support System")

    st.markdown("---")

    st.write("""
Welcome to the AI Recruitment Decision Support System.

This system uses Artificial Intelligence,
Natural Language Processing,
Sentence-BERT,
Machine Learning
and Explainable AI
to assist recruiters in selecting the most suitable candidates.
""")

    st.markdown("## 🎯 Features")

    col1, col2 = st.columns(2)

    with col1:

        st.success("Resume Upload")

        st.success("Job Description Upload")

        st.success("Semantic Resume Matching")

        st.success("Candidate Ranking")

    with col2:

        st.success("Explainable AI")

        st.success("Recruiter Dashboard")

        st.success("Candidate Feedback")

        st.success("Download Reports")

# ---------------------------------------------------
# RESUME SCREENING
# ---------------------------------------------------

elif page == "Resume Screening":

    st.title("📄 Resume Screening")

    st.write("Upload resumes and job description.")

    resumes = st.file_uploader(
        "Upload Candidate Resume(s)",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    job_description = st.file_uploader(
        "Upload Job Description",
        type=["pdf", "docx"]
    )

    analyze = st.button("🚀 Analyze Candidates")

    if analyze:

        if resumes is None or len(resumes) == 0:

            st.error("Please upload at least one resume.")

        elif job_description is None:

            st.error("Please upload a Job Description.")

        else:

            st.success("Files uploaded successfully.")

            st.info("Semantic analysis will be added in the next version.")

# ---------------------------------------------------
# Candidate Ranking
# ---------------------------------------------------

elif page == "Candidate Ranking":

    st.title("🏆 Candidate Ranking")

    st.info("Ranking module coming soon.")

# ---------------------------------------------------
# Recruiter Dashboard
# ---------------------------------------------------

elif page == "Recruiter Dashboard":

    st.title("📊 Recruiter Dashboard")

    st.info("Dashboard module coming soon.")

# ---------------------------------------------------
# Explainable AI
# ---------------------------------------------------

elif page == "Explainable AI":

    st.title("🧠 Explainable AI")

    st.info("SHAP explanations will be added here.")

# ---------------------------------------------------
# About
# ---------------------------------------------------

elif page == "About":

    st.title("About the Project")

    st.write("""
Project Title:

Explainable AI-Powered Recruitment Decision Support System

Developed By:

Gauri Sinha

Patna University

Technology Used

• Python

• Streamlit

• Sentence-BERT

• Machine Learning

• SHAP

• Explainable AI
""")
