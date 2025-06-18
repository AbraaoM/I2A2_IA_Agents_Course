import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessagesHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from tools.extract_zip_tool import extract_zip_contents

load_dotenv()

template = """
You are a helpful assistant that extracts CSV files from a zip file and preserves their original format.

histótico da conversa:
{history}
Entrada do usuário:
{input}
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0.5
)

chain = prompt | llm

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessagesHistory(
    runnable=chain,
    chat_history=get_session_history("default_session"),
    input_message_key="input",
    history_messages_key="history"
)


def start():
    print("Starting the assistant...")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the assistant.")
            break
        
        # Simulate a session ID for this example
        session_id = "default_session"
        
        # Run the chain with the user input
        response = chain_with_history.invoke({"input": user_input, "session_id": session_id})
        
        # Print the response from the assistant
        print(f"Assistant: {response['output']}")


if __name__ == "__main__":
    start()

# print(extract_zip_contents("resources/202401_NFs.zip"))