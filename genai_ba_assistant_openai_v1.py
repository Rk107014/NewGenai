import streamlit as st
import os
from dotenv import main
from openai import AzureOpenAI


# Load environment variables
main.load_dotenv()
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Create AzureOpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version
)

def genai_response(prompt):
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful Business Analyst assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] {str(e)}"

# Streamlit UI
st.set_page_config(page_title="GenAI BA Assistant", layout="centered")
st.title("🤖 GenAI BA Assistant")

task = st.selectbox("Choose your task", [
    "Generate User Stories",
    "Generate UAT Test Cases",
    "Summarize Requirements",
    "Generate Sprint Report"
])

input_text = st.text_area("Paste your input here", height=200)

if st.button("Generate"):
    if not input_text.strip():
        st.warning("Please enter some input to proceed.")
    else:
        if task == "Generate User Stories":
            prompt = f"""You are a Business Analyst assistant. Convert the following notes into user stories with acceptance criteria.

Format:
- As a [user], I want to [goal], so that [benefit].
- Acceptance Criteria:
  - [AC 1]
  - [AC 2]

Notes:
{input_text}
"""
        elif task == "Generate UAT Test Cases":
            prompt = f"""Create UAT test cases based on the user story and acceptance criteria below:

{input_text}

Format:
- Test Case ID
- Scenario
- Steps
- Expected Result
"""
        elif task == "Summarize Requirements":
            prompt = f"""Summarize the following business requirements into a one-pager with key bullets and impacted modules:

{input_text}
"""
        elif task == "Generate Sprint Report":
            prompt = f"""Summarize the sprint activity below into:
- Completed
- In Progress
- Blockers
- Next Steps

Tasks:
{input_text}
"""
        else:
            prompt = input_text

        result = genai_response(prompt)
        st.subheader("📄 GenAI Output")
        st.code(result, language='markdown')
