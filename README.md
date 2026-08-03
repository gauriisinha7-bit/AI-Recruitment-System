# 🤖 Explainable AI-Powered Recruitment Decision Support System (AI-RDSS)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20Application-red)
![Sentence-BERT](https://img.shields.io/badge/Sentence--BERT-Semantic%20Matching-green)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-orange)
![SHAP](https://img.shields.io/badge/Explainable%20AI-SHAP-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)


📌 Project Description

The **Explainable AI-Powered Recruitment Decision Support System (AI-RDSS)** is an intelligent recruitment platform designed to improve the transparency, fairness, and efficiency of candidate evaluation during the hiring process.

Unlike traditional Applicant Tracking Systems (ATS), which primarily rely on keyword matching, this system performs **semantic resume-job matching** using **Sentence-BERT embeddings** and **Machine Learning**. The platform also incorporates **Explainable Artificial Intelligence (XAI)** techniques to provide transparent explanations for recruitment decisions, enabling recruiters to understand why a candidate receives a particular score.

The system has been developed as an academic research prototype to demonstrate the application of Explainable AI in recruitment and decision support.


🎯 Objectives

The project aims to:

- Improve resume-job matching using semantic similarity.
- Reduce limitations of keyword-based Applicant Tracking Systems.
- Provide transparent and explainable hiring recommendations.
- Assist recruiters in ranking candidates objectively.
- Demonstrate the practical application of Explainable AI in Human Resource Management.


Features
Resume Parsing

- PDF Resume Upload
- DOCX Resume Upload
- Automatic Text Extraction


💼 Job Description Analysis

- Upload Job Description
- Extract Required Skills
- Define Experience Requirements
- Define Education Criteria

🧠 Semantic Resume Matching

- Sentence-BERT Embeddings
- Cosine Similarity Matching
- Skill Matching
- Experience Matching
- Education Matching
- Certification Matching


📊 Candidate Evaluation

- Weighted Scoring System
- Final Candidate Score
- Candidate Ranking
- Recommendation Generation

🤖 Explainable AI

- SHAP Feature Importance
- Transparent Candidate Evaluation
- Feature Contribution Analysis
- Explainable Recruitment Decisions

📈 Recruiter Dashboard

- Upload Multiple Resumes
- Upload Job Description
- Analyze Candidates
- Rank Candidates
- Download Results

📑 Report Generation

- CSV Export
- Excel Export
- Candidate Summary
- Ranking Report

🏗️ Project Architecture

```text
Candidate Resume
        │
        ▼
Resume Parsing
        │
        ▼
Text Preprocessing
        │
        ▼
Sentence-BERT Embedding
        │
        ▼
Semantic Similarity
        │
        ▼
Feature Extraction
        │
        ▼
Machine Learning Model
        │
        ▼
Explainable AI (SHAP)
        │
        ▼
Candidate Ranking
        │
        ▼
Recruiter Dashboard
```
🛠️ Technology Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python |
| Frontend | Streamlit |
| Machine Learning | Scikit-learn |
| NLP | Sentence-BERT |
| Explainable AI | SHAP |
| Data Handling | Pandas |
| Numerical Computing | NumPy |
| Resume Parsing | PyMuPDF, python-docx |
| Visualization | Matplotlib |
| File Export | OpenPyXL |

⚙️ Installation

Clone Repository

```bash
git clone https://github.com/gauriisinha7-bit/AI-Recruitment-System.git
```


Move into Project

```bash
cd AI-Recruitment-System
```

Create Virtual Environment

Windows

bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```


## Run Application

```bash
streamlit run app.py
```


📂 Project Structure

```text
AI-Recruitment-System
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── models
│     recruitment_knowledge_base.json
│
├── data
│     resumes
│     job_descriptions
│
├── utils
│     resume_parser.py
│     semantic_matching.py
│     scoring.py
│     explainability.py
└──    report_generator.py


🔬 Methodology

The proposed methodology consists of the following stages:

1. Resume Collection
2. Job Description Collection
3. Resume Parsing
4. Text Cleaning and Preprocessing
5. Sentence-BERT Embedding Generation
6. Semantic Similarity Computation
7. Feature Extraction
8. Weighted Candidate Scoring
9. Explainable AI using SHAP
10. Candidate Ranking
11. Recruiter Decision Support





# 🌍 Research Contribution

This project contributes to Explainable Artificial Intelligence in Human Resource Management by integrating semantic NLP techniques with transparent machine learning models to support fair and interpretable recruitment decisions.

The proposed framework aims to address limitations of conventional keyword-based Applicant Tracking Systems by incorporating semantic understanding and explainability into candidate evaluation.

---

# 🚀 Future Scope

Future enhancements may include:

- Multi-role recruitment support
- LLM-powered interview feedback
- AI chatbot for candidate interaction
- Fairness and bias detection
- OCR support for scanned resumes
- Cloud deployment
- Database integration
- Role-based authentication
- REST API integration
- Recruiter analytics dashboard


📚 Citation

If you use this work in your research, please cite:

```text
Sinha, G. (2026).
Explainable AI-Powered Recruitment Decision Support System:
Semantic Resume-Job Matching and Transparent Candidate Evaluation using Sentence-BERT and SHAP.
GitHub Repository.
https://github.com/gauriisinha7-bit/AI-Recruitment-System
```


📄 License

This project is licensed under the MIT License.


👩‍💻 Author

**Gauri Sinha**

M.A. Personnel Management & Industrial Relations (PMIR)

Patna University

Research Interests:

- Explainable AI
- Human Resource Analytics
- Artificial Intelligence in Recruitment
- Machine Learning
- Industrial Relations
- HR Technology

GitHub:

https://github.com/gauriisinha7-bit
