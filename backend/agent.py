from langgraph.graph import StateGraph
from langchain_aws import ChatBedrock
from pydantic import BaseModel
import boto3

class AgentState(BaseModel):
    topic: str
    draft: str = ""
    approved: bool = False

llm = ChatBedrock(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="us-east-1"
)

s3 = boto3.client("s3")

def generate_post(topic: str):
    response = llm.invoke(f"Write a professional LinkedIn post about {topic}")
    return response.content if hasattr(response, "content") else str(response)

def approve_post(draft: str):
    review = llm.invoke(f"Check if this content is safe and professional:\n{draft}")
    return True

def generate_content_node(state: AgentState):
    draft = generate_post(state.topic)
    return {"draft": draft}

def approve_content_node(state: AgentState):
    approved = approve_post(state.draft)
    return {"approved": approved}