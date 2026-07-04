import streamlit as st
import requests

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Business Requirement Writer",
    page_icon="📄",
    layout="wide"
)

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.stButton>button {
    width: 100%;
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
}

.stTextInput>div>div>input {
    border-radius: 10px;
}

textarea {
    border-radius: 10px !important;
}

.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("📄 Business Requirement Writer")

st.sidebar.info("""
AI-powered requirement generation system.

### Features
✅ Requirement Generation  
✅ AI-based Content  
✅ RAG Search  
✅ Chat Support  
✅ PDF Export  
""")

st.sidebar.success("Week 3 Project UI")

# -----------------------------------
# HEADER
# -----------------------------------

st.title("📄 Business Requirement Writer")

st.write(
    "Generate professional Business Requirement Documents using AI."
)

st.divider()

# -----------------------------------
# INPUT SECTION
# -----------------------------------

col1, col2 = st.columns(2)

with col1:

    title = st.text_input(
        "📌 Project Title",
        placeholder="Example: Online Food Delivery System"
    )

with col2:

    domain = st.text_input(
        "🌐 Project Domain",
        placeholder="Example: E-Commerce"
    )

features = st.text_area(
    "⚙ Required Features",
    placeholder="""
Example:
- User Login
- Payment Integration
- Admin Dashboard
- Order Tracking
- AI Recommendations
""",
    height=150
)

# -----------------------------------
# GENERATE REQUIREMENTS
# -----------------------------------

if st.button("🚀 Generate Requirements"):

    if title == "" or domain == "" or features == "":
        st.warning("Please fill all fields")

    else:

        with st.spinner("Generating requirements..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/generate",
                    json={
                        "title": title,
                        "domain": domain,
                        "features": features
                    }
                )

                if response.status_code == 200:

                    result = response.json()

                    generated_text = result["generated_requirement"]

                    st.session_state.history.append(generated_text)

                    st.success("Requirements Generated Successfully")

                    st.subheader("📋 Generated Requirement Document")

                    st.text_area(
                        "Output",
                        generated_text,
                        height=500
                    )

                else:

                    st.error("Backend Error")
                    st.text(response.text)

            except Exception as e:
                st.error(f"Error: {e}")

# -----------------------------------
# SIMPLE CHAT SECTION
# -----------------------------------

st.divider()

st.subheader("💬 Ask Questions")

question = st.text_input(
    "Enter your question",
    placeholder="What are functional requirements?"
)

if st.button("🤖 Ask AI"):

    if question == "":
        st.warning("Please enter a question")

    else:

        try:

            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={
                    "question": question
                }
            )

            if response.status_code == 200:

                result = response.json()

                st.success(result["answer"])

            else:

                st.error("Backend Error")
                st.text(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

# -----------------------------------
# RAG SEARCH
# -----------------------------------

st.divider()

st.subheader("📚 RAG Document Search")

rag_question = st.text_input(
    "Ask from Knowledge Base",
    placeholder="What is sprint planning?"
)

if st.button("🔍 Search Documents"):

    if rag_question == "":
        st.warning("Please enter a question")

    else:

        try:

            response = requests.post(
                "http://127.0.0.1:8000/rag-search",
                json={
                    "question": rag_question
                }
            )

            if response.status_code == 200:

                result = response.json()

                st.success("Relevant Documents Retrieved")

                for item in result["retrieved_results"]:
                    st.info(item)

            else:

                st.error("Backend Error")
                st.text(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

# -----------------------------------
# HISTORY SECTION
# -----------------------------------

st.divider()

st.subheader("🕘 Generation History")

if len(st.session_state.history) == 0:

    st.info("No history available")

else:

    for index, item in enumerate(
        reversed(st.session_state.history), start=1
    ):

        with st.expander(f"Generated Document {index}"):

            st.text(item[:1500])

# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(
    "Business Requirement Writer | Final Year GenAI Project"
)