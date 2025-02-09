#!/usr/bin/env python

from dotenv import load_dotenv  # (Make sure python-dotenv is installed)
from datetime import datetime
import streamlit as st  # Import Streamlit for the UI
import os
import sys
# Import the pysqlite3 module provided by chromadb-pysqlite3
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
load_dotenv()
# Determine the directory of the current file (which is latest_ai_development/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Since app_ui.py is at the top-level latest_ai_development, add the 'src' folder to sys.path.
src_path = os.path.join(current_dir, "src")
# Add the src folder to sys.path so the package is found
sys.path.insert(0, src_path)

# Now import your CrewAI code from the package.
from latest_ai_development.main import run  # noqa: E402

st.title("CrewAI Report Generator")

# Let the user enter custom inputs.
user_topic = st.text_input("Enter topic:", value="AI LLMs")
user_year = st.text_input("Enter current year:",
                          value=str(datetime.now().year))

if st.button("Generate Report"):
    st.info("Generating report...")

    # Build the inputs dictionary using values from the UI.
    inputs = {
        'topic': user_topic,
        'current_year': user_year
    }

    try:
        # Call the run() function with the inputs.
        result = run(inputs=inputs)
        st.subheader("Generated Report")
        # Access the "raw" attribute from the CrewOutput object
        if hasattr(result, 'raw'):
            raw_output = result.raw
            st.markdown(raw_output)
        else:
            st.write(result)
    except Exception as e:
        st.error(f"Error: {e}")
