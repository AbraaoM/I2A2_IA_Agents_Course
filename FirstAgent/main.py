from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import logging

# Configure logging
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create a simple prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant that provides clear and concise answers."),
    ("human", "{input_text}")
])

# Initialize the model
model = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    temperature=0.7,
    model="meta-llama/llama-4-scout-17b-16e-instruct"
)

# Create the chain using LCEL
chain = prompt | model

def chat():
    print("Simple Chat (type 'quit' to exit)")
    print("---------------------------------")
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check for quit command
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break
            
        try:
            # Get response from model
            response = chain.invoke({"input_text": user_input})
            print(f"\nAssistant: {response.content}")
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            print("Sorry, I encountered an error. Please try again.")

if __name__ == "__main__":
    chat()