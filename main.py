import io, json, re
from pathlib import Path

import fitz
import numpy as np
import pandas as pd
import shap
import streamlit as st
from docx import Document
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title='AI Recruitment System', page_icon='AR', layout='wide')

st.markdown('''
<style>
.stApp{background:#f6f8fb}.block-container{max-width:1450px;padding-top:2rem}#MainMenu,footer{visibility:hidden}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#111827,#172033 55%,#1e293b)}
[data-testid="stSidebar"] *{color:#f8fafc}[data-testid="stSidebar"] [role="radiogroup"] label{border-radius:10px;padding:.7rem .85rem;transition:.2s}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{transform:translateX(4px);background:rgba(255,255,255,.08)}
.brand{padding-bottom:1.2rem;border-bottom:1px solid rgba(255,255,255,.1);margin-bottom:1rem}.brand-title{font-size:1.2rem;font-weight:700}.brand-copy{color:#aab5c8;font-size:.78rem;line-height:1.55;margin-top:.5rem}
.header{background:#fff;border:1px solid #e2e8f0;border-radius:18px;padding:1.8rem 2rem;margin-bottom:1.5rem;box-shadow:0 8px 28px rgba(15,23,42,.04);transition:.22s}.header:hover{transform:translateY(-3px);box-shadow:0 16px 36px rgba(15,23,42,.08)}
.kicker{color:#2563eb;font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1px}.title{margin:.45rem 0 0;color:#111827;font-size:2rem;font-weight:730}.copy{color:#667085;max-width:900px;margin-top:.6rem;line-height:1.7}
.card{background:#fff;border:1px solid #e2e8f0;border-radius:15px;padding:1.35rem;min-height:130px;box-shadow:0 4px 16px rgba(15,23,42,.035);transition:.22s}.card:hover{transform:translateY(-6px);border-color:#cbd5e1;box-shadow:0 15px 34px rgba(15,23,42,.09)}
.label{color:#667085;font-size:.72rem;font-weight:680;letter-spacing:.75px;text-transform:uppercase}.value{color:#111827;font-size:1.7rem;font-weight:730;margin-top:.45rem}.small{color:#98a2b3;font-size:.78rem;margin-top:.3rem}
.stButton>button{width:100%;min-height:44px;background:linear-gradient(90deg,#172033,#263a59);color:#fff;border:none;border-radius:10px;font-weight:650;transition:.2s}.stButton>button:hover{transform:translateY(-3px);color:#fff;box-shadow:0 10px 22px rgba(23,32,51,.2)}
</style>
''', unsafe_allow_html=True)

DEFAULT_ROLE={
 'weights':{'Skills':40,'Experience':25,'Education':15,'Projects':10,'Certifications':5,'Soft_Skills':5},
 'required_skills':['Python','SQL','Git','Data Structures','Algorithms'],
 'preferred_skills':['Docker','AWS','Linux','REST API'],
 'minimum_experience':2,
 'education':['B.Tech','B.E.','Bachelor','M.Tech','MCA'],
 'project_keywords':['project','developed','implemented','built','created','application','system','model'],
 'certification_keywords':['certification','certificate','certified'],
 'soft_skills':['communication','teamwork','leadership','problem solving','adaptability']}
SKILLS=['Python','Java','C','C++','JavaScript','SQL','Git','GitHub','Docker','Kubernetes','AWS','Azure','GCP','Linux','REST API','Data Structures','Algorithms','Machine Learning','Deep Learning','NLP','TensorFlow','PyTorch','Scikit-learn','Pandas','NumPy','MySQL','PostgreSQL','MongoDB','HTML','CSS','React','Node.js']

def load_kb():
 p=Path('recruitment_knowledge_base.json')
 if not p.exists(): return {'Software Engineer':DEFAULT_ROLE}
 try: data=json.loads(p.read_text(encoding='utf-8'))
 except Exception: return {'Software Engineer':DEFAULT_ROLE}
 if 'job_role' in data:
  role=data.get('job_role','Software Engineer'); body={k:v for k,v in data.items() if k!='job_role'}; return {role:{**DEFAULT_ROLE,**body}}
 clean={k:{**DEFAULT_ROLE,**v} for k,v in data.items() if isinstance(v,dict)}
 return clean or {'Software Engineer':DEFAULT_ROLE}

@st.cache_resource(show_spinner=False)
def model(): return SentenceTransformer('all-MiniLM-L6-v2')

def read_file(f):
 b=f.getvalue(); n=f.name.lower()
 if n.endswith('.pdf'):
  with fitz.open(stream=b,filetype='pdf') as pdf: return '\n'.join(p.get_text() for p in pdf)
 if n.endswith('.docx'):
  d=Document(io.BytesIO(b)); return '\n'.join(p.text for p in d.paragraphs)
 raise ValueError('Only PDF and DOCX are supported.')

def find_skills(text, skills):
 low=text.lower(); return sorted({s for s in skills if re.search(r'(?<!\w)'+re.escape(s.lower())+r'(?!\w)',low)})

def experience(text):
 vals=[float(x) for x in re.findall(r'(\d+(?:\.\d+)?)\+?\s*(?:years|year|yrs|yr)',text.lower()) if float(x)<50]
 vals += [float(x)/12 for x in re.findall(r'(\d+(?:\.\d+)?)\+?\s*(?:months|month|mos|mo)',text.lower()) if float(x)<600]
 return round(max(vals),2) if vals else 0.0

def education(text):
 deg=['Bachelor','B.Tech','B.E.','BCA','B.Sc','Master','MBA','M.Tech','MCA','M.Sc','PhD','Diploma']
 return sorted({d for d in deg if d.lower() in text.lower()})

def parse_jd(text, fallback):
 r=dict(fallback); s=find_skills(text,SKILLS); e=experience(text); ed=education(text)
 if s: r['required_skills']=s; r['preferred_skills']=[]
 if e: r['minimum_experience']=e
 if ed: r['education']=ed
 return r

def basic(text, fallback):
 lines=[x.strip() for x in text.splitlines() if x.strip()]
 name=next((x for x in lines if '@' not in x and 'linkedin' not in x.lower()),fallback)
 em=re.search(r'[\w\.-]+@[\w\.-]+\.\w+',text); ph=re.search(r'(\+?\d[\d\s\-\(\)]{8,}\d)',text)
 return name[:100], em.group(0) if em else 'Not found', ph.group(0).strip() if ph else 'Not found'

def semantic(candidate, required, mdl, threshold):
 if not required:return [],[],100.0
 if not candidate:return [],required,0.0
 ce=mdl.encode(candidate,convert_to_numpy=True,normalize_embeddings=True); re_=mdl.encode(required,convert_to_numpy=True,normalize_embeddings=True); mat=cosine_similarity(re_,ce)
 matched=[]; missing=[]
 for i,req in enumerate(required):
  j=int(np.argmax(mat[i])); score=float(mat[i][j])
  if score>=threshold: matched.append({'Required Skill':req,'Matched Skill':candidate[j],'Similarity':round(score,3)})
  else: missing.append(req)
 return matched,missing,round(len(matched)/len(required)*100,2)

def kw_score(text, words):
 if not words:return 0.0
 low=text.lower(); return round(sum(w.lower() in low for w in words)/len(words)*100,2)

def analyze(file_name,text,role,mdl,threshold):
 req=role.get('required_skills',[]); pref=role.get('preferred_skills',[]); skills=find_skills(text,list(dict.fromkeys(req+pref)))
 matched,missing,skill=semantic(skills,req,mdl,threshold); exp=experience(text); exp_s=100 if role.get('minimum_experience',0)<=0 else round(min(exp/float(role.get('minimum_experience',0)),1)*100,2)
 edu=education(text); cand=' '.join(edu).lower(); need=' '.join(role.get('education',[])).lower(); edu_s=100.0 if any(x in cand and x in need for x in ['bachelor','b.tech','b.e','master','m.tech','mba','mca']) else 0.0
 comps={'Skills':skill,'Experience':exp_s,'Education':edu_s,'Projects':kw_score(text,role.get('project_keywords',[])),'Certifications':kw_score(text,role.get('certification_keywords',[])),'Soft_Skills':kw_score(text,role.get('soft_skills',[]))}
 w=role.get('weights',{}); total=sum(float(w.get(k,0)) for k in comps) or 100; contrib={k:round(v*float(w.get(k,0))/total,2) for k,v in comps.items()}; final=round(sum(contrib.values()),2)
 decision='Strongly Recommended' if final>=80 else 'Recommended' if final>=65 else 'Review Required' if final>=45 else 'Not Recommended'; stage='Technical and Managerial Interview' if final>=80 else 'Technical Interview' if final>=65 else 'Recruiter Review' if final>=45 else 'Do Not Progress'
 name,email,phone=basic(text,Path(file_name).stem)
 return {'Candidate_Name':name,'Email':email,'Phone':phone,'Resume_File':file_name,'Skills':skills,'Experience_Years':exp,'Education':edu,'Skill_Score':skill,'Experience_Score':exp_s,'Education_Score':edu_s,'Projects_Score':comps['Projects'],'Certification_Score':comps['Certifications'],'Soft_Skills_Score':comps['Soft_Skills'],'Final_Score':final,'Decision':decision,'Interview_Stage':stage,'Matched_Skills':matched or [],'Missing_Skills':missing or [],'Contributions':contrib,'Required_Count':len(req),'Matched_Count':len(matched or []),'Missing_Count':len(missing or []),'Confidence':round(min(100.0,60+len(matched or [])*6+final*0.2),2)}

def report_df(results):
 rows=[]
 for i,r in enumerate(results,1): rows.append({'Rank':i,'Candidate Name':r['Candidate_Name'],'Email':r['Email'],'Phone':r['Phone'],'Final Score':r['Final_Score'],'Confidence':r.get('Confidence',0),'Decision':r['Decision'],'Interview Stage':r['Interview_Stage'],'Skill Score':r['Skill_Score'],'Experience Score':r['Experience_Score'],'Education Score':r['Education_Score'],'Projects Score':r['Projects_Score'],'Certification Score':r['Certification_Score'],'Soft Skills Score':r['Soft_Skills_Score'],'Matched Skills':'; '.join(x['Required Skill'] for x in r['Matched_Skills']),'Missing Skills':', '.join(r['Missing_Skills'])})
 return pd.DataFrame(rows)

def feedback(c):
 strengths=[]; weaknesses=[]
 if c['Skill_Score']>=70: strengths.append('Strong technical-skill alignment.')
 else: weaknesses.append('Technical-skill alignment needs review.')
 if c['Experience_Score']>=80: strengths.append('Experience requirement is satisfied.')
 else: weaknesses.append('Experience is below the stated requirement.')
 if c['Education_Score']>=100: strengths.append('Education requirement is satisfied.')
 else: weaknesses.append('Education could not be fully verified.')
 if c['Missing_Skills']: weaknesses.append('Missing skills: '+', '.join(c['Missing_Skills']))
 return strengths,weaknesses

def assistant_answer(q,results):
 if not results:return 'Run candidate analysis first.'
 q=q.lower(); top=results[0]
 if 'rank' in q or 'top' in q:return f"{top['Candidate_Name']} ranked first with {top['Final_Score']:.2f}%. Largest contributions: "+', '.join(f'{k} {v:.2f}' for k,v in sorted(top['Contributions'].items(),key=lambda x:x[1],reverse=True)[:3])+'.'
 if 'compare' in q and len(results)>1:
  a,b=results[:2]; return f"{a['Candidate_Name']} scored {a['Final_Score']:.2f}% while {b['Candidate_Name']} scored {b['Final_Score']:.2f}%."
 if 'missing' in q:return 'Missing skills for the top candidate: '+(', '.join(top['Missing_Skills']) or 'None detected.')
 if 'interview' in q:return f"Recommended next stage: {top['Interview_Stage']}."
 return 'Ask why the top candidate ranked first, compare the top two candidates, list missing skills, or ask for the interview stage.'

def pdf_bytes(results):
 buf=io.BytesIO(); doc=SimpleDocTemplate(buf,pagesize=A4); styles=getSampleStyleSheet(); story=[Paragraph('AI Recruitment Decision Support Report',styles['Title']),Spacer(1,.2*inch)]
 for i,c in enumerate(results,1):
  story.append(Paragraph(f"Rank {i}: {c['Candidate_Name']}",styles['Heading2'])); data=[['Final Score',f"{c['Final_Score']:.2f}%"],['Decision',c['Decision']],['Interview Stage',c['Interview_Stage']],['Missing Skills',', '.join(c['Missing_Skills']) or 'None']]; t=Table(data,colWidths=[1.5*inch,5.2*inch]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),colors.HexColor('#E8EEF7')),('GRID',(0,0),(-1,-1),.5,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP')])); story += [t,Spacer(1,.2*inch)]
 doc.build(story); return buf.getvalue()

for key,default in {'results':[],'chat':[],'role_data':None,'notes':{}}.items():
 if key not in st.session_state: st.session_state[key]=default

with st.sidebar:
 st.markdown('<div class="brand"><div class="brand-title">AI Recruitment System</div><div class="brand-copy">Semantic matching, explainable scoring and recruiter decision support.</div></div>',unsafe_allow_html=True)
 page=st.radio('Navigation',['Dashboard','Recruitment','Analysis','Explainability','Candidate Feedback','Recruiter Assistant','Reports'],label_visibility='collapsed')

kb=load_kb(); roles=list(kb)

def header(k,t,c): st.markdown(f'<div class="header"><div class="kicker">{k}</div><h1 class="title">{t}</h1><p class="copy">{c}</p></div>',unsafe_allow_html=True)

if page=='Dashboard':
 header('Recruitment Intelligence','AI Recruitment Decision Support System','Semantic resume matching, candidate ranking, explainability, feedback and reports.')
 r=st.session_state.results; top=r[0]['Final_Score'] if r else 0; rec=sum(x['Decision'] in {'Recommended','Strongly Recommended'} for x in r)
 for col,(lab,val,small) in zip(st.columns(4),[('Candidates',len(r),'Analyzed'),('Top Score',f'{top:.2f}%','Highest suitability'),('Recommended',rec,'Decision support'),('Model','Sentence-BERT','Semantic matching')]):
  with col: st.markdown(f'<div class="card"><div class="label">{lab}</div><div class="value">{val}</div><div class="small">{small}</div></div>',unsafe_allow_html=True)
elif page=='Recruitment':
 header('Recruitment Workspace','Upload and Analyze','The uploaded job description dynamically determines skills, experience and education requirements.')
 role=st.selectbox('Fallback role',roles); threshold=st.slider('Semantic threshold',.4,.9,.6,.05); a,b=st.columns(2)
 with a: resumes=st.file_uploader('Candidate resumes',type=['pdf','docx'],accept_multiple_files=True)
 with b: jd=st.file_uploader('Job description',type=['pdf','docx'])
 if st.button('Run Candidate Analysis',use_container_width=True):
  if not resumes or jd is None: st.error('Upload at least one resume and one job description.'); st.stop()
  try:
   with st.spinner('Running Sentence-BERT analysis...'):
    mdl=model(); role_data=parse_jd(read_file(jd),kb[role]); st.session_state.role_data=role_data; out=[]; bar=st.progress(0)
    for i,f in enumerate(resumes): out.append(analyze(f.name,read_file(f),role_data,mdl,threshold)); bar.progress((i+1)/len(resumes))
    out.sort(key=lambda x:x['Final_Score'],reverse=True); st.session_state.results=out
   st.success('Analysis completed successfully.')
  except Exception as e: st.exception(e)
elif page=='Analysis':
 header('Candidate Intelligence','Ranking and Analysis','Review scores, decisions, matched skills and missing requirements.')
 r=st.session_state.results
 if not r: st.info('Run analysis first.')
 else:
  df=report_df(r); st.dataframe(df[['Rank','Candidate Name','Final Score','Decision','Interview Stage','Skill Score','Experience Score','Education Score']],use_container_width=True,hide_index=True); st.bar_chart(df.set_index('Candidate Name')['Final Score'])
  for i,c in enumerate(r,1):
   with st.expander(f"Rank {i} - {c['Candidate_Name']} - {c['Final_Score']:.2f}%"):
    cols=st.columns(5); cols[0].metric('Final Score',f"{c['Final_Score']:.2f}%"); cols[1].metric('Confidence',f"{c.get('Confidence',0):.2f}%"); cols[2].metric('Decision',c['Decision']); cols[3].metric('Experience',f"{c['Experience_Years']} years"); cols[4].metric('Next Stage',c['Interview_Stage'])
    counts=st.columns(3); counts[0].metric('Required Skills',c.get('Required_Count',0)); counts[1].metric('Matched Skills',c.get('Matched_Count',0)); counts[2].metric('Missing Skills',c.get('Missing_Count',0))
    x,y=st.columns(2)
    with x:
     st.markdown('**Matched skills**')
     matched=[item for item in (c.get('Matched_Skills') or []) if isinstance(item,dict)]
     if matched:
      st.dataframe(pd.DataFrame(matched),use_container_width=True,hide_index=True)
     else:
      st.info('No required skills matched above threshold.')
    with y:
     st.markdown('**Missing skills**')
     missing=[s for s in (c.get('Missing_Skills') or []) if s]
     if missing:
      for s in missing:
       st.write('- '+str(s))
     else:
      st.success('No required skills missing.')
    note_key=c.get('Resume_File',c.get('Candidate_Name','candidate'))
    note_value=st.text_area('Recruiter notes',value=st.session_state.notes.get(note_key,''),key=f'note_{i}')
    if st.button('Save Notes',key=f'save_note_{i}',use_container_width=True):
     st.session_state.notes[note_key]=note_value
     st.success('Recruiter notes saved.')
elif page=='Explainability':
 header('Explainable AI','SHAP and Feature Contributions','Inspect the factors influencing candidate scores.')
 r=st.session_state.results
 if not r: st.info('Run analysis first.')
 else:
  idx=st.selectbox('Candidate',range(len(r)),format_func=lambda i:r[i]['Candidate_Name']); c=r[idx]; st.bar_chart(pd.DataFrame({'Feature':list(c['Contributions']),'Contribution':list(c['Contributions'].values())}).set_index('Feature'))
  if len(r)<2: st.warning('Analyze at least two candidates for a SHAP surrogate explanation.')
  else:
   try:
    cols=['Skill_Score','Experience_Score','Education_Score','Projects_Score','Certification_Score','Soft_Skills_Score']
    X=pd.DataFrame([[float(z.get(k,0)) for k in cols] for z in r],columns=cols)
    y=pd.Series([float(z.get('Final_Score',0)) for z in r])
    lm=LinearRegression().fit(X,y)
    values=shap.Explainer(lm,X)(X)
    import matplotlib.pyplot as plt
    shap.plots.waterfall(values[idx],show=False)
    st.pyplot(plt.gcf(),bbox_inches='tight')
    plt.close()
   except Exception as e:
    st.error(f'SHAP explanation could not be generated: {e}')
elif page=='Candidate Feedback':
 header('Decision Support','Feedback and Interview Questions','Generate recruiter-facing strengths, weaknesses and questions.')
 r=st.session_state.results
 if not r: st.info('Run analysis first.')
 else:
  idx=st.selectbox('Candidate',range(len(r)),format_func=lambda i:r[i]['Candidate_Name'])
  c=r[idx]
  strengths,weaknesses=feedback(c)
  strengths=[x for x in (strengths or []) if x]
  weaknesses=[x for x in (weaknesses or []) if x]
  st.write(f"{c['Candidate_Name']} scored {c['Final_Score']:.2f}% and is {c['Decision']}. Suggested stage: {c['Interview_Stage']}.")
  a,b=st.columns(2)
  with a:
   st.subheader('Strengths')
   if strengths:
    for item in strengths:
     st.write('- '+str(item))
   else:
    st.info('No strengths generated.')
  with b:
   st.subheader('Areas for review')
   if weaknesses:
    for item in weaknesses:
     st.write('- '+str(item))
   else:
    st.info('No areas for review generated.')
  st.subheader('Interview questions')
  qs=[f'Describe a project where you used {s}.' for s in (c.get('Skills') or [])[:4]]+[f'What exposure do you have to {s}?' for s in (c.get('Missing_Skills') or [])[:3]]+['Describe a difficult technical problem you solved.']
  qs=[q for q in qs if q]
  for number,question in enumerate(qs,1):
   st.write(f'{number}. {question}')
elif page=='Recruiter Assistant':
 header('Recruiter Assistant','Ask About Results','Ask why a candidate ranked first, compare candidates, or identify missing skills.')
 for m in st.session_state.chat:
  with st.chat_message(m['role']): st.write(m['content'])
 q=st.chat_input('Ask a recruiter question')
 if q: st.session_state.chat += [{'role':'user','content':q},{'role':'assistant','content':assistant_answer(q,st.session_state.results)}]; st.rerun()
elif page=='Reports':
 header('Recruitment Documentation','Download Reports','Export candidate results in CSV, Excel and PDF formats.')
 r=st.session_state.results
 if not r: st.info('Run analysis first.')
 else:
  df=report_df(r); excel=io.BytesIO();
  with pd.ExcelWriter(excel,engine='openpyxl') as writer: df.to_excel(writer,index=False,sheet_name='Candidate Ranking')
  a,b,c=st.columns(3)
  with a: st.download_button('Download CSV',df.to_csv(index=False).encode(),file_name='AI_RDSS_Report.csv',mime='text/csv',use_container_width=True)
  with b: st.download_button('Download Excel',excel.getvalue(),file_name='AI_RDSS_Report.xlsx',mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',use_container_width=True)
  with c: st.download_button('Download PDF',pdf_bytes(r),file_name='AI_RDSS_Report.pdf',mime='application/pdf',use_container_width=True)
  st.dataframe(df,use_container_width=True,hide_index=True)
