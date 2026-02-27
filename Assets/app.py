import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# AI Modules
from modules.question_generator import generate_question
from modules.answer_evaluator import evaluate_answer
from modules.scoring_engine import extract_score
from utils.tracker import save_result, load_history

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="AI Interview Intelligence System",
    layout="wide"
)

st.title("🤖 AI Interview Intelligence System")

# =========================
# Sidebar - Interview Setup
# =========================
st.sidebar.header("⚙️ Interview Setup")

roles = [
    "AI Data Analyst",
    "Data Analyst",
    "Senior Data Analyst",
    "Business Analyst",
    "AI Engineer",
    "Data Scientist",
    "Other"
]

selected_role = st.sidebar.selectbox("Select Target Role", roles)

if selected_role == "Other":
    role = st.sidebar.text_input("Enter Custom Role")
else:
    role = selected_role

experience = st.sidebar.slider("Years of Experience", 1, 10, 5)

round_type = st.sidebar.selectbox(
    "Select Interview Round",
    ["Technical", "Behavioral", "Case Study"]
)

# =========================
# Generate Question
# =========================
if st.button("🎯 Generate Question"):
    if role.strip() == "":
        st.warning("Please enter a valid role.")
    else:
        question = generate_question(role, experience, round_type)
        st.session_state.question = question

# =========================
# Question Section
# =========================
if "question" in st.session_state:

    st.subheader("📝 Interview Question")
    st.info(st.session_state.question)

    answer = st.text_area("✍️ Enter Your Answer", height=200)

    if st.button("📊 Evaluate Answer"):
        if answer.strip() == "":
            st.warning("Please enter your answer before evaluation.")
        else:
            feedback = evaluate_answer(
                st.session_state.question,
                answer
            )

            score = extract_score(feedback)

            st.subheader("📊 Evaluation Result")

            col1, col2 = st.columns(2)
            col1.metric("Final Score", f"{score}/10")
            col2.metric("Round Type", round_type)

            st.write("### 🧠 Detailed Feedback")
            st.write(feedback)

            # Save result
            save_result(role, experience, round_type, score)

# =========================
# Dashboard Section
# =========================
st.divider()
st.header("📈 Performance Dashboard")

history = load_history()

if not history.empty:

    history["timestamp"] = pd.to_datetime(history["timestamp"])
    history = history.sort_values("timestamp")

    col1, col2 = st.columns(2)

    # ---------------------
    # Score Trend
    # ---------------------
    with col1:
        st.write("### 📉 Score Trend Over Time")

        plt.figure()
        plt.plot(history["timestamp"], history["score"])
        plt.xticks(rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Score")
        st.pyplot(plt)

    # ---------------------
    # Average by Round
    # ---------------------
    with col2:
        st.write("### 📊 Average Score by Round")

        avg_round = history.groupby("round")["score"].mean()

        plt.figure()
        avg_round.plot(kind="bar")
        plt.xlabel("Round")
        plt.ylabel("Average Score")
        st.pyplot(plt)

    # ---------------------
    # Overall Stats
    # ---------------------
    st.subheader("📌 Overall Performance Summary")

    avg_score = round(history["score"].mean(), 2)
    best_score = history["score"].max()

    col1, col2 = st.columns(2)
    col1.metric("Overall Average", avg_score)
    col2.metric("Best Score", best_score)

else:
    st.info("No interview history found. Start practicing to see analytics!")