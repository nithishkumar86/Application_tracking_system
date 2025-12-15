import streamlit as st
import os
from pathlib import Path
import requests
import json


def init_session():
    session_default = {
        "path_to_resume":None
    }

    for key,value in session_default.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

def save_resume_to_directory(file_name: str):
    path = Path.cwd()
    folder_path = path / "Resume"  # Just the directory, not including filename
    Path.mkdir(folder_path, parents=True, exist_ok=True)
    
    # Return the full file path (directory + filename)
    file_path = folder_path / "resume.pdf"
    return str(file_path)


st.set_page_config(page_icon="📄", page_title="ATS", layout="centered")
st.header(" 🤖 Application Tracking System using Crewai in Multi Agent")

with st.expander(label="Upload the resume in the pdf format", icon="📑"):
    upload = st.file_uploader(label="Upload your resume", accept_multiple_files=False, type=['.pdf'])

    if st.button(label="Check to process", type="primary"):
        if upload:
            try:
                file_path = save_resume_to_directory(upload.name)
                with open(file_path, "wb") as f:
                    f.write(upload.getbuffer())
                st.session_state['path_to_resume'] = file_path
                st.success("file save successfully")
                st.code(file_path)
            except Exception as e:
                st.error(f"An error occurred during file saving: {e}")
        else:
            st.warning("Please upload the resume to process")

if st.session_state['path_to_resume']:

    job_description = st.text_area(label="Provide the job description")
    if st.button(label="process resume", type="primary"):
        if job_description:
            payload = {"description": job_description}

            response = requests.post(
                url="http://127.0.0.1:8000/response",
                json=payload,   # ✅ correct
                timeout=300
            )

            if response.status_code == 200:
                result = response.json()
                
                final_result = result.get("response",{})
                
                # Get the raw data
                if len(final_result)>0:
                    raw_data = final_result.get("raw", None)
                else:
                    raw_data = {}
                    
                # Check if it's already a dict or a string
                if isinstance(raw_data, str):
                    answer = json.loads(raw_data)  # Parse if it's a string to dict
                elif isinstance(raw_data, dict):
                    answer = raw_data  # Use directly if it's already a dict
                else:
                    answer = {}  # Fallback to empty dict
    
                # Now extract fields safely
                overall_score = answer.get("overall_score")
                recommendation = answer.get("recommendation", "N/A")
                key_qualifications = answer.get("key_qualifications", [])
                areas_of_concern = answer.get("areas_of_concern", [])
                hiring_justification = answer.get("hiring_justification", "N/A")

                
                st.markdown("---")
                st.header("📊 Hiring Assessment Results")
                
                # Score and Recommendation in columns
                col1, col2 = st.columns(2)
            
                with col1:
                    if overall_score is not None and overall_score > 0:
                        st.metric(
                            label="Overall Score",
                            value=f"{overall_score:.1f}/10",
                            delta=None
                        )
                    else:
                        st.metric(
                            label="Overall Score",
                            value="N/A",
                            delta=None
                        )
            
                with col2:
                    # Color code recommendation
                    if recommendation == "Strongly Recommend":
                        st.success(f"✅ {recommendation}")
                    elif recommendation == "Recommend with Reservations":
                        st.warning(f"⚠️ {recommendation}")
                    else:
                        st.error(f" {recommendation}")
            
                st.subheader("✅ Key Qualifications")
                if key_qualifications:
                    for idx, qualification in enumerate(key_qualifications, start=1):
                        st.markdown(f"**{idx}.** {qualification}")
                else:
                    st.info("No qualifications listed")
                    
                st.markdown("---")

                # Areas of Concern
                st.subheader("⚠️ Areas of Concern")
                if areas_of_concern:
                    for idx, concern in enumerate(areas_of_concern, start=1):
                        st.markdown(f"**{idx}.** {concern}")
                else:
                    st.info("No concerns listed")
                        
                st.markdown("---")
            
                # Hiring Justification
                st.subheader("💡 Hiring Justification")
                st.info(hiring_justification)
                

                st.success(hiring_justification)

                # Download results
                st.markdown("---")
                result_json = json.dumps(answer, indent=2)
                st.download_button(
                    label="📥 Download Assessment (JSON)",
                    data=result_json,
                    file_name="hiring_assessment.json",
                    mime="application/json"
                )
       
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        else:
            st.warning("Please provide the job description to process")