import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Recruitment System",
    page_icon="AR",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "uploaded_resumes" not in st.session_state:
    st.session_state.uploaded_resumes = []

if "uploaded_job_description" not in st.session_state:
    st.session_state.uploaded_job_description = None

if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False


# ============================================================
# CUSTOM CORPORATE UI
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       GLOBAL APPLICATION
    -------------------------------------------------------- */

    html, body, [class*="css"] {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }

    .stApp {
        background:
            linear-gradient(
                180deg,
                #f8fafc 0%,
                #f4f6f9 100%
            );
        color: #172033;
    }

    .block-container {
        max-width: 1480px;
        padding-top: 2rem;
        padding-bottom: 4rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent;
    }


    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #111827 0%,
                #172033 55%,
                #1e293b 100%
            );
        border-right: 1px solid rgba(255, 255, 255, 0.07);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.6rem;
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    .sidebar-brand {
        padding: 0.35rem 0.25rem 1.35rem 0.25rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.10);
        margin-bottom: 1.1rem;
    }

    .sidebar-brand-title {
        font-size: 1.18rem;
        font-weight: 700;
        letter-spacing: 0.15px;
        color: #ffffff;
    }

    .sidebar-brand-subtitle {
        margin-top: 0.45rem;
        color: #aab5c8;
        font-size: 0.78rem;
        line-height: 1.55;
    }

    [data-testid="stSidebar"] [role="radiogroup"] {
        gap: 0.35rem;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label {
        background: transparent;
        border: 1px solid transparent;
        border-radius: 10px;
        padding: 0.68rem 0.85rem;
        transition:
            transform 0.20s ease,
            background-color 0.20s ease,
            border-color 0.20s ease,
            box-shadow 0.20s ease;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        transform: translateX(4px);
        background: rgba(255, 255, 255, 0.075);
        border-color: rgba(255, 255, 255, 0.10);
        box-shadow: 0 7px 20px rgba(0, 0, 0, 0.12);
    }

    [data-testid="stSidebar"] [role="radiogroup"] label p {
        font-size: 0.9rem;
        font-weight: 540;
    }

    .sidebar-footer {
        margin-top: 2rem;
        padding-top: 1.15rem;
        border-top: 1px solid rgba(255, 255, 255, 0.10);
    }

    .sidebar-footer-title {
        color: #ffffff;
        font-weight: 650;
        font-size: 0.78rem;
        margin-bottom: 0.55rem;
    }

    .sidebar-footer-text {
        color: #aab5c8;
        font-size: 0.70rem;
        line-height: 1.75;
    }

    .sidebar-version {
        color: #758297;
        font-size: 0.64rem;
        margin-top: 0.8rem;
    }


    /* --------------------------------------------------------
       PAGE HEADER
    -------------------------------------------------------- */

    .page-header {
        background:
            linear-gradient(
                135deg,
                #ffffff 0%,
                #fbfcfe 100%
            );
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 1.8rem 2rem;
        box-shadow:
            0 4px 15px rgba(15, 23, 42, 0.035),
            0 14px 35px rgba(15, 23, 42, 0.025);
        margin-bottom: 1.5rem;
        transition:
            transform 0.22s ease,
            box-shadow 0.22s ease,
            border-color 0.22s ease;
    }

    .page-header:hover {
        transform: translateY(-3px);
        border-color: #cbd5e1;
        box-shadow:
            0 10px 26px rgba(15, 23, 42, 0.065),
            0 20px 45px rgba(15, 23, 42, 0.04);
    }

    .page-kicker {
        color: #2563eb;
        font-size: 0.72rem;
        font-weight: 720;
        text-transform: uppercase;
        letter-spacing: 1.1px;
        margin-bottom: 0.5rem;
    }

    .page-title {
        color: #111827;
        font-size: 2rem;
        font-weight: 720;
        line-height: 1.2;
        letter-spacing: -0.4px;
        margin: 0;
    }

    .page-description {
        color: #667085;
        max-width: 900px;
        margin-top: 0.65rem;
        margin-bottom: 0;
        font-size: 0.96rem;
        line-height: 1.7;
    }


    /* --------------------------------------------------------
       KPI CARDS
    -------------------------------------------------------- */

    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        padding: 1.35rem 1.4rem;
        min-height: 132px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.035);
        transition:
            transform 0.22s ease,
            box-shadow 0.22s ease,
            border-color 0.22s ease;
    }

    .metric-card:hover {
        transform: translateY(-6px);
        border-color: #cbd5e1;
        box-shadow:
            0 14px 32px rgba(15, 23, 42, 0.09),
            0 5px 14px rgba(15, 23, 42, 0.04);
    }

    .metric-label {
        color: #667085;
        font-size: 0.72rem;
        font-weight: 680;
        letter-spacing: 0.75px;
        text-transform: uppercase;
    }

    .metric-value {
        color: #111827;
        font-size: 1.85rem;
        font-weight: 730;
        margin-top: 0.45rem;
        line-height: 1.2;
    }

    .metric-description {
        color: #98a2b3;
        font-size: 0.77rem;
        margin-top: 0.35rem;
        line-height: 1.45;
    }


    /* --------------------------------------------------------
       CONTENT CARDS
    -------------------------------------------------------- */

    .content-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.45rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.03);
        margin-bottom: 1rem;
        transition:
            transform 0.22s ease,
            box-shadow 0.22s ease,
            border-color 0.22s ease;
    }

    .content-card:hover {
        transform: translateY(-5px);
        border-color: #cbd5e1;
        box-shadow:
            0 14px 32px rgba(15, 23, 42, 0.075),
            0 5px 14px rgba(15, 23, 42, 0.035);
    }

    .card-title {
        color: #172033;
        font-size: 1rem;
        font-weight: 690;
        margin-bottom: 0.45rem;
    }

    .card-description {
        color: #667085;
        font-size: 0.84rem;
        line-height: 1.62;
    }


    /* --------------------------------------------------------
       WORKFLOW CARDS
    -------------------------------------------------------- */

    .workflow-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        padding: 1.25rem;
        min-height: 160px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.03);
        transition:
            transform 0.22s ease,
            border-color 0.22s ease,
            box-shadow 0.22s ease;
    }

    .workflow-card:hover {
        transform: translateY(-7px);
        border-color: #93a8c7;
        box-shadow:
            0 16px 34px rgba(15, 23, 42, 0.09);
    }

    .workflow-number {
        width: 32px;
        height: 32px;
        border-radius: 9px;
        background: #172033;
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.82rem;
        margin-bottom: 0.85rem;
    }

    .workflow-title {
        color: #172033;
        font-weight: 690;
        font-size: 0.94rem;
    }

    .workflow-description {
        color: #667085;
        font-size: 0.79rem;
        line-height: 1.55;
        margin-top: 0.42rem;
    }


    /* --------------------------------------------------------
       SECTION LABEL
    -------------------------------------------------------- */

    .section-heading {
        margin-top: 1.6rem;
        margin-bottom: 0.85rem;
    }

    .section-heading-title {
        color: #172033;
        font-size: 1.13rem;
        font-weight: 700;
    }

    .section-heading-description {
        color: #7b8798;
        font-size: 0.82rem;
        margin-top: 0.25rem;
    }


    /* --------------------------------------------------------
       UPLOADERS
    -------------------------------------------------------- */

    [data-testid="stFileUploader"] {
        background: #ffffff;
        border: 1px solid #dfe5ed;
        border-radius: 14px;
        padding: 0.35rem;
        transition:
            transform 0.20s ease,
            border-color 0.20s ease,
            box-shadow 0.20s ease;
    }

    [data-testid="stFileUploader"]:hover {
        transform: translateY(-3px);
        border-color: #8fa4c2;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.07);
    }


    /* --------------------------------------------------------
       BUTTONS
    -------------------------------------------------------- */

    .stButton > button {
        width: 100%;
        min-height: 44px;
        background:
            linear-gradient(
                90deg,
                #172033 0%,
                #263a59 100%
            );
        color: #ffffff;
        border: 1px solid transparent;
        border-radius: 10px;
        font-weight: 640;
        font-size: 0.88rem;
        transition:
            transform 0.20s ease,
            box-shadow 0.20s ease,
            background 0.20s ease;
    }

    .stButton > button:hover {
        color: #ffffff;
        border-color: transparent;
        transform: translateY(-3px);
        background:
            linear-gradient(
                90deg,
                #111827 0%,
                #1f3554 100%
            );
        box-shadow: 0 10px 22px rgba(23, 32, 51, 0.20);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    .stDownloadButton > button {
        width: 100%;
        min-height: 43px;
        border-radius: 10px;
        font-weight: 620;
        transition:
            transform 0.20s ease,
            box-shadow 0.20s ease;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 22px rgba(15, 23, 42, 0.10);
    }


    /* --------------------------------------------------------
       STATUS LABELS
    -------------------------------------------------------- */

    .status-ready {
        display: inline-block;
        background: #ecfdf3;
        color: #027a48;
        border: 1px solid #abefc6;
        padding: 0.4rem 0.72rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 650;
    }

    .status-pending {
        display: inline-block;
        background: #fffaeb;
        color: #b54708;
        border: 1px solid #fedf89;
        padding: 0.4rem 0.72rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 650;
    }

    .divider {
        height: 1px;
        background: #e2e8f0;
        margin: 1.5rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">
                AI Recruitment System
            </div>

            <div class="sidebar-brand-subtitle">
                Explainable candidate evaluation through semantic
                matching and structured recruitment analysis.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
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
        <div class="sidebar-footer">

            <div class="sidebar-footer-title">
                Core Technologies
            </div>

            <div class="sidebar-footer-text">
                Python<br>
                Streamlit<br>
                Artificial Intelligence<br>
                Sentence-BERT<br>
                SHAP
            </div>

            <div class="sidebar-version">
                Research Prototype · Version 1.0
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.markdown(
        """
        <div class="page-header">

            <div class="page-kicker">
                Recruitment Intelligence
            </div>

            <h1 class="page-title">
                AI Recruitment Decision Support System
            </h1>

            <p class="page-description">
                A structured recruitment workspace for semantic
                resume matching, transparent candidate evaluation,
                explainable scoring and recruiter decision support.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    resume_count = len(st.session_state.uploaded_resumes)

    job_status = (
        "Available"
        if st.session_state.uploaded_job_description is not None
        else "Not available"
    )

    analysis_status = (
        "Completed"
        if st.session_state.analysis_complete
        else "Pending"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    Candidate Resumes
                </div>

                <div class="metric-value">
                    {resume_count}
                </div>

                <div class="metric-description">
                    Uploaded documents in the current recruitment cycle
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    Job Description
                </div>

                <div class="metric-value"
                     style="font-size:1.24rem; margin-top:0.72rem;">
                    {job_status}
                </div>

                <div class="metric-description">
                    Active role specification for candidate evaluation
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">
                    Semantic Model
                </div>

                <div class="metric-value"
                     style="font-size:1.24rem; margin-top:0.72rem;">
                    Ready
                </div>

                <div class="metric-description">
                    Sentence-BERT matching environment
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    Analysis Status
                </div>

                <div class="metric-value"
                     style="font-size:1.24rem; margin-top:0.72rem;">
                    {analysis_status}
                </div>

                <div class="metric-description">
                    Status of the most recent evaluation cycle
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="section-heading">
            <div class="section-heading-title">
                Recruitment Workflow
            </div>

            <div class="section-heading-description">
                Complete the candidate evaluation process in four
                structured stages.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    step1, step2, step3, step4 = st.columns(4)

    with step1:
        st.markdown(
            """
            <div class="workflow-card">
                <div class="workflow-number">01</div>

                <div class="workflow-title">
                    Upload Resumes
                </div>

                <div class="workflow-description">
                    Add one or more candidate resumes in PDF or DOCX
                    format for structured screening.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with step2:
        st.markdown(
            """
            <div class="workflow-card">
                <div class="workflow-number">02</div>

                <div class="workflow-title">
                    Add Job Description
                </div>

                <div class="workflow-description">
                    Provide the role requirements that will guide
                    semantic matching and scoring.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with step3:
        st.markdown(
            """
            <div class="workflow-card">
                <div class="workflow-number">03</div>

                <div class="workflow-title">
                    Run AI Analysis
                </div>

                <div class="workflow-description">
                    Evaluate candidate suitability using semantic
                    similarity and role-based criteria.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with step4:
        st.markdown(
            """
            <div class="workflow-card">
                <div class="workflow-number">04</div>

                <div class="workflow-title">
                    Review Results
                </div>

                <div class="workflow-description">
                    Examine candidate rankings, explanations and
                    recruitment reports.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# RECRUITMENT
# ============================================================

elif page == "Recruitment":

    st.markdown(
        """
        <div class="page-header">
            <div class="page-kicker">
                Recruitment Workspace
            </div>

            <h1 class="page-title">
                Candidate and Role Documents
            </h1>

            <p class="page-description">
                Upload candidate resumes and one job description.
                These documents will form the basis of the
                recruitment analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:

        st.markdown(
            """
            <div class="content-card">
                <div class="card-title">
                    Candidate Resumes
                </div>

                <div class="card-description">
                    Upload multiple candidate resumes. Supported
                    formats are PDF and DOCX.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        resumes = st.file_uploader(
            "Upload candidate resumes",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="resume_files"
        )

        if resumes:
            st.session_state.uploaded_resumes = resumes

            st.success(
                f"{len(resumes)} candidate resume(s) uploaded."
            )

            with st.expander("View uploaded files"):
                for number, resume in enumerate(resumes, start=1):
                    st.write(f"{number}. {resume.name}")

    with right:

        st.markdown(
            """
            <div class="content-card">
                <div class="card-title">
                    Job Description
                </div>

                <div class="card-description">
                    Upload the job description that will be used as
                    the evaluation reference.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        job_description = st.file_uploader(
            "Upload job description",
            type=["pdf", "docx"],
            accept_multiple_files=False,
            label_visibility="collapsed",
            key="job_description_file"
        )

        if job_description is not None:
            st.session_state.uploaded_job_description = job_description

            st.success("Job description uploaded.")

            st.caption(job_description.name)

    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-heading">
            <div class="section-heading-title">
                Evaluation Readiness
            </div>

            <div class="section-heading-description">
                Both document categories must be available before
                candidate analysis can begin.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    status1, status2, status3 = st.columns(3)

    with status1:
        if st.session_state.uploaded_resumes:
            st.markdown(
                '<span class="status-ready">'
                'Resumes available'
                '</span>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<span class="status-pending">'
                'Resumes required'
                '</span>',
                unsafe_allow_html=True
            )

    with status2:
        if st.session_state.uploaded_job_description is not None:
            st.markdown(
                '<span class="status-ready">'
                'Job description available'
                '</span>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<span class="status-pending">'
                'Job description required'
                '</span>',
                unsafe_allow_html=True
            )

    with status3:
        if (
            st.session_state.uploaded_resumes
            and st.session_state.uploaded_job_description is not None
        ):
            st.markdown(
                '<span class="status-ready">'
                'Ready for analysis'
                '</span>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<span class="status-pending">'
                'Upload process incomplete'
                '</span>',
                unsafe_allow_html=True
            )

    st.write("")

    run_analysis = st.button(
        "Run Candidate Analysis",
        use_container_width=True
    )

    if run_analysis:

        if not st.session_state.uploaded_resumes:
            st.error("Upload at least one candidate resume.")

        elif st.session_state.uploaded_job_description is None:
            st.error("Upload one job description.")

        else:
            st.session_state.analysis_complete = True

            st.success(
                "Document validation is complete. Candidate scoring "
                "and ranking will be connected to this action."
            )


# ============================================================
# ANALYSIS
# ============================================================

elif page == "Analysis":

    st.markdown(
        """
        <div class="page-header">
            <div class="page-kicker">
                Candidate Intelligence
            </div>

            <h1 class="page-title">
                Analysis and Explainability
            </h1>

            <p class="page-description">
                Review semantic matching, candidate suitability,
                structured evaluation scores and SHAP-based
                explanations.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.analysis_complete:

        st.info(
            "No completed analysis is available. Upload the required "
            "documents in the Recruitment workspace and run the analysis."
        )

    else:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
                <div class="content-card">
                    <div class="card-title">
                        Semantic Matching
                    </div>

                    <div class="card-description">
                        Sentence-BERT candidate-to-role similarity
                        results will appear here.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                """
                <div class="content-card">
                    <div class="card-title">
                        Structured Scoring
                    </div>

                    <div class="card-description">
                        Skills, experience, education and other
                        evaluated criteria will appear here.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                """
                <div class="content-card">
                    <div class="card-title">
                        SHAP Explanation
                    </div>

                    <div class="card-description">
                        Feature-level contribution and decision
                        transparency will appear here.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    st.markdown(
        """
        <div class="page-header">
            <div class="page-kicker">
                Recruitment Documentation
            </div>

            <h1 class="page-title">
                Candidate Reports
            </h1>

            <p class="page-description">
                Prepare ranking summaries, candidate evaluation
                reports and recruiter-ready exports.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.analysis_complete:

        st.info(
            "Reports will become available after candidate analysis."
        )

    else:

        left, right = st.columns(2)

        with left:
            st.markdown(
                """
                <div class="content-card">
                    <div class="card-title">
                        Candidate Ranking Report
                    </div>

                    <div class="card-description">
                        Export candidate names, scores, rankings and
                        recommendation outcomes.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.button(
                "Prepare Ranking Report",
                disabled=True,
                use_container_width=True
            )

        with right:
            st.markdown(
                """
                <div class="content-card">
                    <div class="card-title">
                        Detailed Evaluation Report
                    </div>

                    <div class="card-description">
                        Export matched skills, missing requirements
                        and explainability results.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.button(
                "Prepare Detailed Report",
                disabled=True,
                use_container_width=True
            )


# ============================================================
# SETTINGS
# ============================================================

elif page == "Settings":

    st.markdown(
        """
        <div class="page-header">
            <div class="page-kicker">
                Application Management
            </div>

            <h1 class="page-title">
                System Settings
            </h1>

            <p class="page-description">
                Review the application configuration and manage the
                current recruitment session.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:
        st.markdown(
            """
            <div class="content-card">
                <div class="card-title">
                    System Configuration
                </div>

                <div class="card-description">
                    Application: AI Recruitment Decision Support System<br><br>
                    Semantic Model: Sentence-BERT<br><br>
                    Explainability Method: SHAP<br><br>
                    Interface: Streamlit
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        st.markdown(
            """
            <div class="content-card">
                <div class="card-title">
                    Current Recruitment Session
                </div>

                <div class="card-description">
                    Reset all uploaded documents and clear the current
                    analysis status before beginning another recruitment
                    cycle.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        reset = st.button(
            "Reset Current Session",
            use_container_width=True
        )

        if reset:
            st.session_state.uploaded_resumes = []
            st.session_state.uploaded_job_description = None
            st.session_state.analysis_complete = False

            st.success("The current session has been reset.")

            st.rerun()
