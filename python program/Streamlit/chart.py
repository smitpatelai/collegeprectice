import streamlit as st
import matplotlib.pyplot as plt

subjects = ["Python","AI","ML","DA","PowerBI"]
marks = [90,35,70,80,99]

fig, ax = plt.subplots()
ax.bar(subjects,marks)
ax.set_xlabel("Subjects")
ax.set_ylabel("Marks")
ax.set_title("Marks of Various Subjects")
st.pyplot(fig)

python = st.slider("Select Python Marks",min_value=35,max_value=100)
ai = st.slider("Select AI Marks",min_value=35,max_value=100)
ml = st.slider("Select ML Marks",min_value=35,max_value=100)

score = [python, ai, ml]
subjects2 = ["Python","AI","ML"]

fig1 , ax1 = plt.subplots()
ax1.bar(subjects2, score)

ax1.set_xlabel("Subjects")
ax1.set_ylabel("Marks")
ax1.set_title("Live Updating Marks")
st.pyplot(fig1)
