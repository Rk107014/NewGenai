import streamlit as st
import toml
import os
from openai import AzureOpenAI

with open("secrets.toml", "r") as f:
    secrets = toml.load(f)
# Load environment variables

endpoint = secrets["api"]["AZURE_OPENAI_ENDPOINT"]
api_key = secrets["api"]["AZURE_OPENAI_API_KEY"]
deployment = secrets["api"]["AZURE_OPENAI_DEPLOYMENT"]
api_version =secrets["api"]["AZURE_OPENAI_API_VERSION"]
print(f"endpoint: {endpoint}")
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
            prompt = f"""You are a senior Business Analyst specialized in mobile fitness applications like Chuze.

Your task is to convert the following functional requirement into detailed, high-quality Agile user stories with:

1. A clear, concise title.
2. User stories written from specific user roles (e.g., Member, Trainer, Admin).
3. Well-defined acceptance criteria covering normal, edge, and negative scenarios.
4. Explicit test case suggestions including boundary conditions.
5. Backend integration notes, such as API calls, data syncing with external systems like ABC, and audit logging.
6. Use markdown formatting with headers and bullet points for clarity.
7. Make the output ready to be used directly in JIRA or similar Agile tools.


Always assume the user roles might include: 
- Gym Member
- Trainer
- Admin
- Frontdesk Staff
- Nutritionist
- Mobile app User (In case of Chuze mobile app)

Output Guidelines:
- Use markdown formatting with headers
- Include 1 main user story and supporting user stories if applicable
- Clearly list acceptance criteria (at least 4), focusing on edge cases, validations, system sync (e.g., ABC), and user actions
- If applicable, include backend integration steps and data handling like profile updates, logs, or notes
- Include test case suggestions with boundary and negative scenarios
- Ensure the tone is suitable for JIRA-ready tickets

Output format:

## Main User Story
**Title:**  
**As a** [user type], **I want** [functionality] **so that** [value/goal]

**Acceptance Criteria:**
1. [AC 1]
2. [AC 2]
3. ...

## 🎨 Figma Mockup Description
- Screen Title: 
- Sections: 
- Fields/Buttons:
- User Flow Notes:

## 🔁 Backend/Sync Notes
- [Any backend processes, API calls, data sync details etc.]
Keep all outputs specific to fitness business logic. Always assume the app is mobile-first unless told otherwise. Also generate the Figma Mockup image based on the generated Userstory.
Respond only with the formatted output.

Notes:
{input_text}
"""
        elif task == "Generate UAT Test Cases":
            prompt = f"""Create UAT test cases Consider this for specific to Fitness Domain, based on the user story and acceptance criteria below:

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
