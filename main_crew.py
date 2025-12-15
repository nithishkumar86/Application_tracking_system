from crewai import Crew, Process, LLM
from typing import Dict, Any
from Agents.agents import agent1, agent2, agent3
from Tasks.tasks import text_extractor, resume_analyzer, final_task
from Config.configloader import load_config
from dotenv import load_dotenv
import json
import os

# Load environment variables from .env file
load_dotenv()
# Load configuration
config = load_config()

# OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    llm= LLM(
        model=config["model"]["provider"] + '/' + config["model"]["name"],
        api_key=GROQ_API_KEY,
        temperature=config['model']['temperature']
        )
else:
    raise EnvironmentError("there is no OPENROUTER_API_KEY")

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# if GOOGLE_API_KEY:
#     llm= LLM(
#         model=config["model1"]["provider"] + '/' + config["model1"]["name"],
#         api_key = GOOGLE_API_KEY,
#         temperature=config['model1']['temperature']
#         )
# else:
#     raise EnvironmentError("there is no OPENROUTER_API_KEY")


# if OPENROUTER_API_KEY:
#     llm = LLM(
#         model=config['model']['provider'] + '/' + config['model']['name'],  # Free model
#         base_url="https://openrouter.ai/api/v1",
#         api_key=OPENROUTER_API_KEY,
#         # Add rate limiting parameters
#         temperature=config['model']['temperature'],
#         max_tokens=config['model']['max_tokens']
#     )
# else:
#     raise EnvironmentError("there is no OPENROUTER_API_KEY")

def run_resume_screening_crew(job_description: str):
    """
    Main function to execute the resume screening crew workflow.
    
    Args:
        resume_path: Path to the resume file (PDF or DOCX)
        job_description: Job description text to compare against
        
    Returns:
        Dictionary containing the final decision report
    """

    agent_1 = agent1(llm)
    agent_2 = agent2(llm)
    agent_3 = agent3(llm)

    task_1 = text_extractor(agent_1)
    task_2 = resume_analyzer(agent_2,task_1)
    task_3 = final_task(agent_3,task_2)

    crew = Crew(
        agents=[agent_1,agent_2,agent_3],
        tasks=[task_1,task_2,task_3],
        process=Process.sequential,
        verbose=True
    )

    crew_output = crew.kickoff(inputs={"resume_content": "", "job_description": job_description,"detailed_report": ""})

    # Print the type of crew_output

    return crew_output


    # Check all attributes of crew_output

    # if hasattr(crew_output, 'json_dict'):
    #     print("crew_output.json_dict:", crew_output.json_dict)
    #     print("=" * 50)


    # print("Crew Output:", type(crew_output))
    
    # if hasattr(crew_output, "final_output"):
    #     print("Final Output Found:", crew_output.final_output)
    
    # if isinstance(crew_output, dict):
    #     print("Crew Output is a dictionary.", crew_output)
    
    # if isinstance(crew_output, str):
    #     print("Crew Output is a string.", crew_output)
    
    # if crew_output.raw:
    #     print("Crew Output has raw attribute.", crew_output)
    
    

        # CASE 1: CrewOutput object
    # if hasattr(crew_output, "final_output") and crew_output.final_output:
    #     return crew_output.final_output

    # if hasattr(crew_output, "final_output"):
    #     return crew_output.final_output

    # if crew_output.final_output:
    #     return crew_output.final_output

    # if isinstance(crew_output, dict):
    #     return crew_output

    # if isinstance(crew_output, str):
    #     try:
    #         return json.loads(crew_output)
    #     except json.JSONDecodeError:
    #         return {"raw_output": crew_output}

    # return {"raw_output": str(crew_output)}
    # # Crew 1: Text Extraction
    # crew_1 = Crew(name="text extractor", agents=[agent_1], tasks=[task_1])
    # crew_result_1 = crew_1.kickoff(inputs=input_data)
    
    # if isinstance(crew_result_1,dict):
    #     input_data["resume_content"] = crew_result_1["resume_content"]
    #     input_data["job_description"] = job_description
    # else:
    #     return "an error occured in text extractor crew"
    
    # # Crew 2: Resume Analysis
    # crew_2 = Crew(name="summarizer", agents=[agent_2], tasks=[task_2])
    # crew_result_2 = crew_2.kickoff(inputs=input_data)  # ← Fixed: crew_2 instead of crew_1
    
    # if isinstance(crew_result_2,dict):
    #     input_data["detailed_report"] = crew_result_2["detailed_report"]
    # else:
    #     return "an error occured in text extractor crew"
    
    # # Crew 3: Decision Making
    # crew_3 = Crew(name="decision taker", agents=[agent_3], tasks=[task_3])
    # crew_result_3 = crew_3.kickoff(inputs=input_data)
    
    # if isinstance(crew_result_3, dict):
    #     return crew_result_3
    # else:
    #     return "Error occurred in decision taker agent"


# def main():
#     """
#     Example usage of the resume screening crew.
#     """
    
#     # # Example inputs
#     # resume_path = "E:/CREWAI_APPLICATION_TRACKING_SYSTEM/Resume/refactored_resume.pdf"

    
#     # job_description = """
#     #     Job Title: Agentic AI Internship

#     #     Requirements:
#     #     - Experience with LLMs (GPT-4, Claude) and agent frameworks (CrewAI, LangChain, AutoGPT)
#     #     - Python programming proficiency
#     #     - Knowledge of prompt engineering and AI workflows
#     # """
    
#     try:
#         # Run the crew
#         result = run_resume_screening_crew(
#             resume_path=resume_path,
#             job_description=job_description
#         )
#         return result
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         import traceback
#         traceback.print_exc()  # ← Added for better debugging
#         return None
    
# if __name__ == "__main__":
#     job_description = """
    # Job Title: Agentic AI Internship

    # Requirements:
    # - Hands-on experience with LLM frameworks (CrewAI, LangChain, AutoGPT)
    # - Python proficiency and prompt engineering skills
    # - Knowledge of multi-agent systems and RAG architectures
    # """
#     run_resume_screening_crew(job_description=job_description)
    
