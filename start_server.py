import os
import subprocess

# Set the default Streamlit port
port = os.getenv("PORT", 8501)

# Run Streamlit
subprocess.run(["streamlit", "run", "lower_gi_triage_streamlit.py", "--server.port", port, "--server.headless", "true"])
