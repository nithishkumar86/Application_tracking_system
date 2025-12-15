from crewai import Task,LLM
from dotenv import load_dotenv
from Agents.agents import agent1
import os
from Tools.custom_tool import pdf_extractor
load_dotenv()
from pydantic import BaseModel,Field
from typing_extensions import List

class ResumeContent(BaseModel):
    resume_content: str

class DetailedReport(BaseModel):
    detailed_report:str


class HiringAssessment(BaseModel):
    overall_score: float = Field(description="Overall candidate score from 0-10")
    recommendation: str = Field(description="Strongly Recommend, Recommend with Reservations, or Do Not Recommend")
    key_qualifications: List[str] = Field(description="Top 5 qualifications")
    areas_of_concern: List[str] = Field(description="Top 5 concerns or gaps")
    hiring_justification: str = Field(description="2-3 sentence executive summary")

def text_extractor(agent) -> Task:
    return Task(
        name="context_extractor",
        description="internally you have the pdf extractor tool behind the hood the tool"
                    "have the path and have the ability to load and extract content from the document"
                    "just hand over task to pdf_extractor tool"
                    "that will take care of everything."
                    "strictly Use the pdf_extractor tool to load the document"
                    "and extract all text content. "
                    "Do not add any additional information or modify the extracted text.",
        expected_output="""
                        The complete text content extracted from the document,
                        without any modifications, additions, or interpretations
                        provide the answer in below mentioned format

                        {
                          "resume_content": "extracted text context without modification to the summarizer"
                        }
                        """,                
        agent=agent,
        output_pydantic=ResumeContent
    )

def resume_analyzer(agent,task) -> Task:
    return Task(
        name="detailed_resume_analyser",
        description="You will receive two inputs: {resume_content} containing the candidate's resume text "
                    "and {job_description} containing the job requirements. "
                    "Perform a detailed analysis following these steps:\n\n"
                    "1. Extract and evaluate the Technical Skills section - identify all programming languages, "
                    "frameworks, tools, and technologies mentioned. Compare against job requirements.\n\n"
                    "2. Analyze the Professional Summary - assess how well it aligns with the role's core objectives "
                    "and whether it highlights relevant qualifications.\n\n"
                    "3. Review the Education section - evaluate degrees, certifications, institutions, and relevance "
                    "to the position.\n\n"
                    "4. Examine all Projects - analyze each project's description, technologies used, complexity, "
                    "and relevance to the job requirements.\n\n"
                    "5. Assess Work Experience - review job titles, responsibilities, duration, and achievements. "
                    "Determine relevance and depth of experience for the target role.\n\n"
                    "6. Based on your complete analysis, identify the Major Strengths - list the top 3-5 strongest "
                    "qualifications that make this candidate suitable for the role.\n\n"
                    "7. Identify the Major Weaknesses - list the top 5-10 gaps, missing qualifications, or areas "
                    "where the candidate falls short of job requirements.\n\n"
                    "Provide specific examples and evidence from both the resume and job description to support "
                    "your findings.",
        expected_output=("""
            {
              "detailed_report": "a detailed report for the decision making"
            }
        """),
        agent=agent,
        output_pydantic=DetailedReport,
        
        context=[task]
    )


def final_task(agent,task) -> Task:
    return Task(
        name="hiring_assessment",
        description=(
            "You will receive a detailed resume analysis report in {detailed_report}.\n\n"
            " CRITICAL INSTRUCTIONS \n"
            "You MUST base your assessment STRICTLY and ONLY on the information provided in the detailed_report.\n"
            "DO NOT use any external knowledge, assumptions, or information not present in the report.\n"
            "DO NOT make inferences beyond what is explicitly stated in the report.\n"
            "Every point you make MUST be directly supported by evidence from the detailed_report.\n\n"
            "Create a hiring assessment with the following:\n\n"
            "1. **Overall Score (0-10)**:\n"
            "   - Calculate this score ONLY based on the strengths and weaknesses mentioned in the detailed_report\n"
            "   - Consider: technical skills match, experience relevance, project quality, and education fit\n"
            "   - Each strength adds value, each weakness reduces value\n"
            "   - Scoring guide: 0-3 (Poor fit), 4-6 (Moderate fit), 7-8 (Good fit), 9-10 (Excellent fit)\n\n"
            "2. **Recommendation**:\n"
            "   - Choose ONLY ONE: 'Strongly Recommend', 'Recommend with Reservations', or 'Do Not Recommend'\n"
            "   - Base this strictly on the overall score from the detailed_report:\n"
            "     * Score 8-10 → 'Strongly Recommend'\n"
            "     * Score 5-7 → 'Recommend with Reservations'\n"
            "     * Score 0-4 → 'Do Not Recommend'\n\n"
            "3. **Key Qualifications (Exactly 5)**:\n"
            "   - Extract the TOP 5 strongest points from the detailed_report's strengths section\n"
            "   - Use EXACT evidence and examples from the report\n"
            "   - Quote specific skills, achievements, or experiences mentioned\n"
            "   - DO NOT add qualifications not mentioned in the report\n\n"
            "4. **Areas of Concern (Exactly 5)**:\n"
            "   - compare with job description requirements\n"
            "   - you are to extract gaps and concerns from detailed report\n"
            "   - don't add any external knowledge or assumptions\n"
            "   - only provide what is missing or weak as per detailed report\n"
            "   - Extract the TOP 5 concerns from the detailed_report's weaknesses section\n"
            "   - Use EXACT evidence and gaps identified in the report\n"
            "   - Focus on skill gaps, missing requirements, or concerns explicitly mentioned\n"
            "   - DO NOT add concerns not mentioned in the report\n\n"
            "5. **Hiring Justification (2-3 sentences)**:\n"
            "   - Summarize your decision using ONLY facts from the detailed_report\n"
            "   - Reference specific points from the key qualifications and areas of concern\n"
            "   - Explain why the score and recommendation are justified based on the report\n"
            "   - DO NOT introduce new information\n\n"
            "   - Ensure All parts of your assessment are directly traceable to the detailed_report.\n\n"
            "   - concern that you are ONLY compiling a decision based on the provided report.\n\n"
            " VALIDATION CHECKLIST \n"
            "Before submitting, verify:\n"
            "- ✓ Score is justified by strengths/weaknesses in the report\n"
            "- ✓ Recommendation matches the scoring guide\n"
            "- ✓ Every qualification is directly from the report's strengths\n"
            "- ✓ Every concern is directly from the report's weaknesses\n"
            "- ✓ Justification only uses information from the report\n"
            "- ✓ No external assumptions or knowledge added\n\n"
            "Remember: You are ONLY a decision compiler. Your job is to structure the information "
            "from the detailed_report into a hiring decision format. You are NOT creating new analysis."
        ),
        expected_output=(
            "{\n"
            '  "overall_score": 8.5,\n'
            '  "recommendation": "Strongly Recommend",\n'
            '  "key_qualifications": ["qualification 1", "qualification 2", "qualification 3", "qualification 4", "qualification 5"],\n'
            '  "areas_of_concern": ["concern 1", "concern 2", "concern 3", "concern 4", "concern 5"],\n'
            '  "hiring_justification": "2-3 sentence executive summary explaining the hiring decision"\n'
            "}\n"
        ),
        agent=agent,
        output_pydantic=HiringAssessment,
        context=[task]
    )