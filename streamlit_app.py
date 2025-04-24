import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_streamlit_app():
    st.set_page_config(page_title="Agentic AI Insights", layout="wide")
    
    st.title("🤖 Agentic AI Insight System")
    st.write("Upload your data, ask questions, and get AI-powered insights.")
    
    # Initialize the orchestrator
    if "orchestrator" not in st.session_state:
        api_key = os.getenv("PERPLEXITY_API_KEY")
        st.session_state.orchestrator = AgentOrchestrator(api_key=api_key)
    
    # File upload
    uploaded_file = st.file_uploader("Upload your data file", 
                                    type=['csv', 'xlsx', 'jpg', 'jpeg', 'png', 'sql'])
    user_query = st.text_area("What insights are you looking for?", 
                             "Analyze this data and provide business insights.")
    
    if uploaded_file and st.button("Process", type="primary"):
        with st.spinner("Processing your data..."):
            # Save uploaded file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process the file
            result = st.session_state.orchestrator.process_file(temp_path, user_query)
            
            # Display results
            if result["success"]:
                st.success("Analysis complete!")
                
                # Create tabs for different outputs
                tab1, tab2, tab3 = st.tabs(["📊 Insights", "📈 Visualizations", "🔍 Q&A"])
                
                with tab1:
                    st.markdown(result["insights"])
                
                with tab2:
                    st.write("### Data Visualizations")
                    viz_status = create_visualizations(st.session_state.orchestrator)
                    
                    # Display visualizations if created successfully
                    try:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.image("numeric_distributions.png")
                        with col2:
                            st.image("categorical_distributions.png")
                        
                        st.image("correlations.png")
                    except:
                        st.write(viz_status)
                
                with tab3:
                    st.write("### Ask Follow-up Questions")
                    follow_up = st.text_input("What else would you like to know?")
                    
                    if follow_up and st.button("Ask", type="secondary"):
                        with st.spinner("Thinking..."):
                            answer = st.session_state.orchestrator.answer_question(follow_up)
                            st.markdown(answer)
            else:
                st.error(f"Analysis failed: {result['message']}")
            
            # Clean up temporary file
            os.remove(temp_path)

if __name__ == "__main__":
    create_streamlit_app()
