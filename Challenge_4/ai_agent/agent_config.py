from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_KEY")


def get_df_agent(df: pd.DataFrame) -> AgentExecutor:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=GEMINI_KEY)
    agent = create_pandas_dataframe_agent(llm, df, allow_dangerous_code=True)
    return agent

def get_agent(tools: list) -> AgentExecutor:
    """
    Cria e retorna um AgentExecutor configurado para usar uma lista de ferramentas.

    Args:
        tools (list): Uma lista de objetos Tool da LangChain.

    Returns:
        AgentExecutor: Um executor de agente pronto para ser invocado.
    """
    # 1. Inicializar o LLM (modelo de linguagem)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=GEMINI_KEY)

    # 2. Criar o Prompt do agente
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Você é um assistente de IA útil que tem acesso a diversas ferramentas. Use-as para responder às perguntas do usuário. Responda de forma concisa e útil."),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # 3. Criar o agente com as ferramentas
    agent = create_tool_calling_agent(llm, tools, prompt)

    # 4. Criar o executor do agente
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor