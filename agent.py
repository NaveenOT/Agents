import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools import set_tasks, add_task, complete_task, view_tasks

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
tools = [set_tasks, add_task, complete_task, view_tasks]

model = ChatGroq(api_key=api_key, model="openai/gpt-oss-20b", temperature=0)

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""You are an AI Task Planner.

Rules:
1. If the user gives a GOAL (something they want to achieve):
   - Break it down into a maximum of 8 tasks
   - Tasks must be concise and actionable
   - Tasks must be logically ordered
   - Call set_tasks with the full list

2. If the user wants to ADD a task:
   - Call add_task with the new task string

3. If the user wants to MARK A TASK AS COMPLETED or says they have completed a task directly or indirectly:
   - Call complete_task with the task name (partial match is fine)

4. If the user wants to VIEW tasks:
   - Call view_tasks

STRICT RULES:
- You MUST always call a tool
- Never respond with plain text only
- Return the tool response as your output without extra commentary
"""
)


def run_agent(user_input: str):
    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    ai_message = result["messages"][-1].content
    return ai_message
            