import streamlit as st
import json
import requests
import os


api_key = os.getenv("OPENROUTER_API_KEY")
global response

st.title("Assignment Clarifier")
st.markdown("Paste your assignment question below and click ‘Clarify Assignment’")
assignment_question = st.text_area("enter the assignment question(s) here")
if st.button("Clarify Assignment"):
    if not api_key:
        raise ValueError("Set OPENROUTER_API_KEY in your environment")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "response_format": { "type": "json_object"},
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": assignment_question+"\ni jst want the plain-English explanation,example, task breakdown, required topics, and a suggested start plan and Return your response as a JSON object with the keys: 'Plain English', 'Example', 'Task Breakdown', 'Required Topics', and 'Start Plan'."}
        ]
    }
    with st.spinner("Clarifying assignment..."):
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Plain English","Example","Task Breakdown", "Required Topics", "Start Plan"])
    #output_dict = {"plain_english explanation": "", "task breakdown": "","required topics": "", "start plan": ""}
    output = response.json()

    raw_ai_text = output['choices'][0]['message']['content']
    ai_data = json.loads(raw_ai_text)

    tab1.write(ai_data["Plain English"])
    tab2.write(ai_data["Example"])
    tab3.write(ai_data["Task Breakdown"])
    tab4.write(ai_data["Required Topics"])
    tab5.write(ai_data["Start Plan"])



