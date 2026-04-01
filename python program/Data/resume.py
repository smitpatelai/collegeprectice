import streamlit as st
import PyPDF2
import pandas as pd

st.title("HR Resume Analysis")

job_desc = st.text_area("Enter Job Description (Skills Required)")

# upload resume
upload_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

def extract_text(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:   # avoid None error
            text += page_text

    return text.lower()

if upload_file and job_desc:
    job_skills = job_desc.lower().split()
    result = []

    for file in upload_file:
        text = extract_text(file)

        matched = []
        missing = []

        for skill in job_skills:
            if skill in text:
                matched.append(skill)
            else:
                missing.append(skill)

        score = int((len(matched) / len(job_skills)) * 100)

        result.append({
            "Candidate": file.name,
            "Match Score": score,
            "Matched Skills": ", ".join(matched),
            "Missing Skills": ", ".join(missing)
        })

    df = pd.DataFrame(result)

    # sort ranking
    df = df.sort_values(by="Match Score", ascending=False)

    st.subheader("Candidate Ranking")
    st.dataframe(df)

    st.subheader("Ranking Chart")
    st.bar_chart(df.set_index("Candidate")["Match Score"])

    # top candidate
    st.subheader("Top Candidate")
    st.success(df.iloc[0]["Candidate"])

    # download csv
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download Results",
        data=csv,
        file_name="resume_ranking.csv",
        mime="text/csv"
    )