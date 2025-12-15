from dotenv import load_dotenv
import os
from Tools.custom_tool import pdf_extractor
from crewai import Agent
load_dotenv()

def agent1(llm) -> Agent:
    return Agent(
        role="pdf_context_extractor",
        goal="Extract text content from documents (PDF or DOCX format) using the provided tool. "
             "Read the document using the provided tool and return its contents accurately.",
        backstory="You are a document processing specialist. Your sole responsibility is to use "
                   "the pdf_extractor tool to read documents and extract their text content. "
                   "You do not modify, summarize, or interpret the content.",
        llm=llm,
        max_iter=3,
        verbose=True,
        tools=[pdf_extractor],
        allow_delegation=False
    )


def agent2(llm) -> Agent:
    return Agent(
        role="resume_analyzer",
        goal="Perform comprehensive analysis of resumes against job descriptions. "
             "Evaluate all resume components including technical skills, professional summary, "
             "education, projects, and work experience. Identify alignment with job requirements "
             "and provide clear assessment of strengths and weaknesses.",
        backstory="You are an experienced HR analyst and technical recruiter with expertise in "
                   "resume evaluation. You systematically compare candidate qualifications against "
                   "job requirements, examining each section of the resume in detail. Your analysis "
                   "is thorough, objective, and focused on identifying how well the candidate matches "
                   "the role. You provide actionable insights about major strengths and weaknesses.",
        llm=llm,
        max_iter=3,
        verbose=True,
        allow_delegation=False
    )

def agent3(llm) -> Agent:
    return Agent(
        role="hiring_decision_compiler",
        goal="Convert detailed resume analysis into a structured hiring assessment with score, "
             "recommendation, qualifications, concerns, and justification based strictly on the analysis report.",
        backstory="You are a hiring decision compiler who structures analysis reports into hiring decisions. "
                   "You extract information directly from the detailed report without adding assumptions or "
                   "external knowledge. Your role is to organize findings into a clear assessment format, "
                   "calculate scores based on strengths versus weaknesses, and provide evidence-based recommendations.",
        llm=llm,
        max_iter=3,
        verbose=True,
        allow_delegation=False
    )