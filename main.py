import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Recruitment System",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "resumes" not in st.session_state:
    st.session_state.resumes = []

if "job_description" not in st.session_state:
    st.session_state.job_description = None

if "analysis_completed" not in st.session_state:
    st.session_state.analysis_completed = False


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main application background */
    .stApp {
        background-color: #F6F8FB;
    }

    /* Remove unnecessary top spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #0B132B 0%,
            #111C3A 55%,
            #172554 100%
        );
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    [data-testid="stSidebar"] * {
        color: #F8FAFC;
    }

    [data-testid="stSidebar"] .stRadio label {
        padding: 0.65rem 0.75rem;
        border-radius: 10px;
        margin-bottom: 0.25rem;
        transition: 0.2s ease-in-out;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(255, 255, 255, 0.08);
    }

    /* Hide default Streamlit menu/footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent;
    }

    /* Typography */
    h1, h2, h3 {
        color: #0F172A;
        font-family: Arial, Helvetica, sans-serif;
    }

    p, li, label {
        font-family: Arial, Helvetica, sans-serif;
    }

    /* Brand */
    .brand-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: 0.2px;
        margin-bottom: 0.15rem;
    }

    .brand-subtitle {
        font-size: 0.78rem;
        color: #B8C4E0;
        line-height: 1.4;
        margin-bottom: 1.7rem;
    }

    /* Top header */
    .top-header {
        background: #FFFFFF;
        border: 1px solid #E5EAF2;
        border-radius: 18px;
        padding: 1.7rem 2rem;
        box-shadow: 0 6px 22px rgba(15, 23, 42, 0.05);
        margin-bottom: 1.4rem;
    }

    .top-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 750;
        color: #0F172A;
    }

    .top-header p {
        color: #64748B;
        margin-top: 0.55rem;
        margin-bottom: 0;
        font-size: 1rem;
        line-height: 1.65;
        max-width: 900px;
    }

    /* Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E5EAF2;
        border-radius: 16px;
        padding: 1.3rem 1.4rem;
        min-height: 135px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
    }

    .metric-label {
        color: #64748B;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.7px;
    }

    .metric-value {
        color: #0F172A;
        font-size: 2rem;
        font-weight: 750;
        margin-top: 0.35rem;
    }

    .metric-description {
        color: #94A3B8;
        font-size: 0.82rem;
        margin-top: 0.25rem;
    }

    /* Section card */
    .section-card {
        background: #FFFFFF;
        border: 1px solid #E5EAF2;
        border-radius: 18px;
        padding: 1.6rem;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
        margin-bottom: 1rem;
    }

    .section-title {
        color: #0F172A;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .section-description {
        color: #64748B;
        font-size: 0.9rem;
        line-height: 1.55;
        margin-bottom: 1rem;
    }

    /* Workflow */
    .workflow-step {
        background: #FFFFFF;
        border: 1px solid #E5EAF2;
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
        min-height: 120px;
    }

    .workflow-number {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #172554;
        color: #FFFFFF;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin-bottom: 0.55rem;
    }

    .workflow-title {
        color: #0F172A;
        font-size: 0.92rem;
        font-weight: 700;
    }

    .workflow-text {
        color: #64748B;
        font-size: 0.78rem;
        margin-top: 0.3rem;
        line-height: 1.4;
    }

    /* Feature cards */
    .feature-card {
        background: #FFFFFF;
        border: 1px solid #E5EAF2;
        border-radius: 14px;
        padding: 1.1rem;
        min-height: 145px;
    }

    .feature-heading {
        color: #0F172A;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.45rem;
    }

    .feature-text {
        color: #64748B;
        font-size: 0.82rem;
        line-height: 1.5;
    }

    /* Status */
    .status-ready {
        display: inline-block;
        background: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 650;
    }

    .status-pending {
        display: inline-block;
        background: #FFF7ED;
        color: #C2410C;
        border: 1px solid #FED7AA;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 650;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #172554, #1E3A8A);
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 1rem;
        font-weight: 650;
        transition: all 0.2s ease-in-out;
    }

    .stButton > button:hover {
        color: #FFFFFF;
        border: none;
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(30, 58, 138, 0.2);
    }

    /* Download buttons */
    .stDownloadButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 0.65rem 1rem;
        font-weight: 600;
    }

    /* File upload */
    [data-testid="stFileUploader"] {
        background: #F8FAFC;
        border-radius: 14px;
        padding: 0.35rem;
    }

    /* Divider */
    .soft-divider {
        height: 1px;
        background: #E5EAF2;
        margin: 1.3rem 0;
    }

    /* Technology footer */
    .technology-footer {
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.12);
        color: #C5D0EA;
        font-size: 0.72rem;
        line-height: 1.7;
    }

    .version-text {
        color: #94A3B8;
        font-size: 0.68rem;
        margin-top: 0.65rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-title">AI Recruitment System</div>
        <div class="brand-subtitle">
            Explainable decision support for structured,
            transparent and intelligent candidate evaluation.
        </div>
        """,
        unsafe_allow_html=True
    )

    selected_page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Recruitment",
            "Analysis",
            "Reports",
            "Settings"
        ],
        label_visibility="collapsed"
    )

    st.markdown(
        """
        <div class="technology-footer">
            <strong>Core Technologies</strong><br>
            Python<br>
            Streamlit<br>
            Artificial Intelligence<br>
            Sentence-BERT<br>
            SHAP

            <div class="version-text">
                Research Prototype · Version 1.0
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DASHBOARD PAGE
# =========================================================

if selected_page == "Dashboard":

    st.markdown(
        """
        <div class="top-header">
            <h1>AI Recruitment Decision Support System</h1>
            <p>
                Evaluate multiple candidates against a job description using
                semantic matching, structured scoring and explainable
                artificial intelligence.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    resumes_count = len(st.session_state.resumes)

    job_status = (
        "Uploaded"
        if st.session_state.job_description is not None
        else "Not uploaded"
    )

    analysis_status = (
        "Completed"
        if st.session_state.analysis_completed
        else "Pending"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Candidate Resumes</div>
                <div class="metric-value">{resumes_count}</div>
                <div class="metric-description">
                    Files currently available for screening
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Job Description</div>
                <div class="metric-value"
                     style="font-size:1.35rem; margin-top:0.8rem;">
                    {job_status}
                </div>
                <div class="metric-description">
                    Active role criteria for evaluation
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">AI Model</div>
                <div class="metric-value"
                     style="font-size:1.35rem; margin-top:0.8rem;">
                    Ready
                </div>
                <div class="metric-description">
                    Semantic analysis environment
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Analysis Status</div>
                <div class="metric-value"
                     style="font-size:1.35rem; margin-top:0.8rem;">
                    {analysis_status}
                </div>
                <div class="metric-description">
                    Latest recruitment evaluation cycle
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.markdown("### Recruitment Workflow")

    step1, step2, step3, step4 = st.columns(4)

    with step1:
        st.markdown(
            """
            <div class="workflow-step">
                <div class="workflow-number">1</div>
                <div class="workflow-title">Upload Resumes</div>
                <div class="workflow-text">
                    Add multiple candidate resumes in PDF or DOCX format.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with step2:
        st.markdown(
            """
            <div class="workflow-step">
                <div class="workflow-number">2</div>
                <div class="workflow-title">Add Job Description</div>
                <div class="workflow-text">
                    Provide the role requirements and evaluation context.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with step3:
        st.markdown(
            """
            <div class="workflow-step">
                <div class="workflow-number">3</div>
                <div class="workflow-title">Run AI Analysis</div>
                <div class="workflow-text">
                    Perform semantic matching and weighted candidate scoring.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with step4:
        st.markdown(
            """
            <div class="workflow-step">
                <div class="workflow-number">4</div>
                <div class="workflow-title">Review Results</div>
                <div class="workflow-text">
                    Examine rankings, explanations and downloadable reports.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.markdown("### System Capabilities")

    feature1, feature2, feature3, feature4 = st.columns(4)

    with feature1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-heading">
                    Semantic Resume Matching
                </div>
                <div class="feature-text">
                    Sentence-BERT supports contextual comparison between
                    candidate information and role requirements.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with feature2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-heading">
                    Structured Evaluation
                </div>
                <div class="feature-text">
                    Candidates can be assessed across skills, experience,
                    education, projects and other role criteria.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with feature3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-heading">
                    Candidate Ranking
                </div>
                <div class="feature-text">
                    Multiple applicants are organized according to their
                    calculated suitability for the selected role.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with feature4:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-heading">
                    Explainable Decisions
                </div>
                <div class="feature-text">
                    SHAP-based explanations help clarify how evaluation
                    factors influence candidate outcomes.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# RECRUITMENT PAGE
# =========================================================

elif selected_page == "Recruitment":

    st.markdown(
        """
        <div class="top-header">
            <h1>Recruitment Workspace</h1>
            <p>
                Upload candidate resumes and one job description before
                initiating the evaluation process.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    upload_col1, upload_col2 = st.columns(2)

    with upload_col1:

        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Candidate Resumes</div>
                <div class="section-description">
                    Upload one or more resumes in PDF or DOCX format.
                    Multiple candidates can be analyzed in a single cycle.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        uploaded_resumes = st.file_uploader(
            "Upload candidate resumes",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            key="resume_uploader",
            label_visibility="collapsed"
        )

        if uploaded_resumes:
            st.session_state.resumes = uploaded_resumes
            st.success(
                f"{len(uploaded_resumes)} resume(s) uploaded successfully."
            )

            with st.expander("View uploaded resume files"):
                for index, resume in enumerate(
                    uploaded_resumes,
                    start=1
                ):
                    st.write(f"{index}. {resume.name}")

    with upload_col2:

        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Job Description</div>
                <div class="section-description">
                    Upload the job description that will be used as the
                    evaluation reference for all candidate resumes.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        uploaded_job_description = st.file_uploader(
            "Upload job description",
            type=["pdf", "docx"],
            accept_multiple_files=False,
            key="job_uploader",
            label_visibility="collapsed"
        )

        if uploaded_job_description is not None:
            st.session_state.job_description = uploaded_job_description
            st.success(
                "Job description uploaded successfully."
            )

            st.write(
                f"Selected file: "
                f"`{uploaded_job_description.name}`"
            )

    st.markdown(
        '<div class="soft-divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown("### Upload Readiness")

    status_col1, status_col2, status_col3 = st.columns(3)

    with status_col1:
        if st.session_state.resumes:
            st.markdown(
                '<span class="status-ready">'
                'Resumes ready</span>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<span class="status-pending">'
                'Resumes required</span>',
                unsafe_allow_html=True
            )

    with status_col2:
        if st.session_state.job_description is not None:
            st.markdown(
                '<span class="status-ready">'
                'Job description ready</span>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<span class="status-pending">'
                'Job description required</span>',
                unsafe_allow_html=True
            )

    with status_col3:
        if (
            st.session_state.resumes
            and st.session_state.job_description is not None
        ):
            st.markdown(
                '<span class="status-ready">'
                'Ready for analysis</span>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<span class="status-pending">'
                'Upload process incomplete</span>',
                unsafe_allow_html=True
            )

    st.write("")

    analyze_button = st.button(
        "Run Candidate Analysis",
        use_container_width=True
    )

    if analyze_button:

        if not st.session_state.resumes:
            st.error(
                "Please upload at least one candidate resume."
            )

        elif st.session_state.job_description is None:
            st.error(
                "Please upload one job description."
            )

        else:
            st.session_state.analysis_completed = True

            st.success(
                "Files are ready. The semantic scoring and ranking "
                "logic will be connected in the next implementation stage."
            )


# =========================================================
# ANALYSIS PAGE
# =========================================================

elif selected_page == "Analysis":

    st.markdown(
        """
        <div class="top-header">
            <h1>Candidate Analysis</h1>
            <p>
                Review candidate rankings, evaluation dimensions,
                semantic match scores and explainable decision factors.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.analysis_completed:

        st.info(
            "No completed analysis is currently available. "
            "Upload the required files in the Recruitment section "
            "and run candidate analysis."
        )

    else:

        st.success(
            "The upload workflow has been completed successfully."
        )

        st.markdown("### Candidate Ranking")

        st.warning(
            "The current version contains the professional interface. "
            "Your scoring, ranking, SBERT and SHAP logic will be "
            "connected here next."
        )


# =========================================================
# REPORTS PAGE
# =========================================================

elif selected_page == "Reports":

    st.markdown(
        """
        <div class="top-header">
            <h1>Recruitment Reports</h1>
            <p>
                Export candidate rankings, evaluation scores,
                matched skills, missing requirements and explanations.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.analysis_completed:

        st.info(
            "Reports will become available after candidate analysis "
            "has been completed."
        )

    else:

        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Available Exports</div>
                <div class="section-description">
                    Downloadable report functionality will be connected
                    after the scoring and ranking modules are integrated.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        report_col1, report_col2 = st.columns(2)

        with report_col1:
            st.button(
                "Prepare CSV Report",
                disabled=True,
                use_container_width=True
            )

        with report_col2:
            st.button(
                "Prepare Excel Report",
                disabled=True,
                use_container_width=True
            )


# =========================================================
# SETTINGS PAGE
# =========================================================

elif selected_page == "Settings":

    st.markdown(
        """
        <div class="top-header">
            <h1>System Settings</h1>
            <p>
                Review application status and manage the current
                recruitment session.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    setting_col1, setting_col2 = st.columns(2)

    with setting_col1:

        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">System Information</div>
                <div class="section-description">
                    Application: AI Recruitment Decision Support System<br>
                    Version: 1.0<br>
                    Interface: Streamlit<br>
                    Semantic Model: Sentence-BERT<br>
                    Explainability: SHAP
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with setting_col2:

        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Current Session</div>
                <div class="section-description">
                    Reset uploaded documents and clear the current
                    analysis state when beginning a new recruitment cycle.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        reset_button = st.button(
            "Reset Current Session",
            use_container_width=True
        )

        if reset_button:
            st.session_state.resumes = []
            st.session_state.job_description = None
            st.session_state.analysis_completed = False

            st.success("The recruitment session has been reset.")

            st.rerun()
