import zipfile
import os
from typing import List, Dict
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.tools import Tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DocumentProcessor:
    def __init__(self):
        self.documents = {}

    def read_zip_contents(self) -> Dict[str, str]:
        zip_path = os.path.join('resources', '202401_NFs.zip')
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    with zip_ref.open(file) as f:
                        content = f.read()
                        try:
                            self.documents[file] = content.decode('utf-8')
                        except UnicodeDecodeError:
                            print(f"\n{file} appears to be a binary file")
            return self.documents

        except (zipfile.BadZipFile, FileNotFoundError, Exception) as e:
            print(f"An error occurred: {str(e)}")
            return {}

def create_document_tools(doc_processor: DocumentProcessor) -> List[Tool]:
    return [
        Tool(
            name="read_document",
            func=lambda x: doc_processor.documents.get(x, "Document not found"),
            description="Reads the content of a specific document by its name"
        ),
        Tool(
            name="list_documents",
            func=lambda _: "\n".join(doc_processor.documents.keys()),
            description="Lists all available documents"
        )
    ]

def setup_agent():
    # Initialize the document processor
    doc_processor = DocumentProcessor()
    doc_processor.read_zip_contents()

    # Create tools
    tools = create_document_tools(doc_processor)

    # Create the prompt template
    prompt = PromptTemplate.from_template("""
    You are an AI assistant that helps analyze document contents.
    You have access to the following tools:
    {tools}

    Use the following format:
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Question: {input}
    Thought: {agent_scratchpad}
    """)

    # Initialize Groq LLM
    llm = ChatGroq(
        temperature=0,
        model_name="meta-llama/llama-4-scout-17b-16e-instruct"
    )

    # Create the agent
    agent = create_react_agent(llm, tools, prompt)
    
    # Create the agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

def main():
    agent_executor = setup_agent()
    
    while True:
        user_input = input("\nAsk a question about the documents (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
            
        try:
            response = agent_executor.invoke({"input": user_input})
            print("\nAnswer:", response["output"])
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()