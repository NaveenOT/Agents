import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(api_key)

parser = JsonOutputParser()
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an AI Task Planner.
Convert the user's goal into a structured JSON plan.
OUTPUT FORMAT:
{{
  "tasks": [
    "task 1",
    "task 2"
  ]
}}
Rules:
1. Maximum 8 tasks
2. Tasks must be concise and actionable
3. Tasks must be logically ordered
4. No vague tasks
5. Return ONLY valid JSON (no explanation, no text outside JSON)
6. No trailing commas
Example:
Input: "Learn React in 5 days"
Output:
{{
  "tasks": [
    "Understand JavaScript basics and JSX",
    "Learn React components and props"
  ]
}}
"""),
    ("user", "{goal}")
])

llm = ChatGroq(api_key=api_key, temperature=0.7,model="llama-3.1-8b-instant")
chain = prompt | llm | parser
if __name__ == "__main__":
    while True:
        goal = input("Enter your goal (or 'exit' to quit):")
        if goal.lower() == "exit":
            break
        try:
            result = chain.invoke({"goal": goal})
            print(json.dumps(result, indent=2))
            print("\nGenerated Plan:\n")
            print(result)
        except Exception as e:
            print(f"Error: {e}")
            




