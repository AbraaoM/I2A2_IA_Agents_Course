from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent import AgentExecutor
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_KEY")


def get_df_agent(df: pd.DataFrame) -> AgentExecutor:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_KEY)
    agent = create_pandas_dataframe_agent(llm, df, allow_dangerous_code=True)
    return agent