import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Embedded AI TA Chatbot", page_icon="🤖")

st.title("Embedded AI & Robotics TA Chatbot 🤖")
st.write("Ask anything about Arduino, sensors, motors, or tiny ML!")

# Load API Key
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("Missing OPENAI_API_KEY in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": (
                "You are a helpful TA for an Embedded AI & Robotics lab. "
                "Explain concepts clearly to first-year students using simple analogies "
                "and avoid unnecessary jargon."
            ),
        }
    ]

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask your robotics question…")

if user_input:
    # Append user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant response (streaming)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_reply = ""

        try:
            stream = client.responses.create(
                model="gpt-4.1-mini",
                input=st.session_state["messages"],
                stream=True,
            )

            # Correct streaming loop
            for event in stream:
                if event.type == "response.output_text.delta":
                    token = event.delta
                    full_reply += token
                    placeholder.markdown(full_reply)

        except Exception as e:
            full_reply = f"⚠️ Error: {str(e)}"
            placeholder.markdown(full_reply)

    # Append assistant message
    st.session_state["messages"].append({"role": "assistant", "content": full_reply})
