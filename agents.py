from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url

from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

# Read Mistral API Key
try:
    MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]
except Exception:
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Initialize LLM
llm = ChatMistralAI(
    api_key=MISTRAL_API_KEY,
    model="mistral-small-2506",
    temperature=0
)

# -----------------------------
# Search Agent
# -----------------------------
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )


# -----------------------------
# Reader Agent
# -----------------------------
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


# -----------------------------
# Writer Chain
# -----------------------------
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Write clear, structured and insightful reports."
    ),
    (
        "human",
        """
Write a detailed research report on the topic below.

Topic:
{topic}

Research Gathered:
{research}

Structure the report as:

# Introduction

# Key Findings
(Minimum 3 well explained points)

# Conclusion

# Sources
(List all URLs found in the research)

Write professionally and use markdown formatting.
"""
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# -----------------------------
# Critic Chain
# -----------------------------
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a strict research reviewer."
    ),
    (
        "human",
        """
Review the following report.

Report:
{report}

Respond in the following format:

Score: X/10

Strengths
- ...

Areas to Improve
- ...

Overall Verdict
...
"""
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()