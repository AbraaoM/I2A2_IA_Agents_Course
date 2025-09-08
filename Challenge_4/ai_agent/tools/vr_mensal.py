from langchain_core.tools import tool
from ai_agent.agent_config import get_df_agent
from singletons import dataframes
import pandas as pd
from typing import Optional

@tool
def read_vr_mensal(query: str) -> str:
    """Consulta informações no DataFrame VR MENSAL."""
    df = dataframes.dataframes["vr_mensal"]
    agent = get_df_agent(df)
    return agent.run({"input": query})

@tool
def add_vr_mensal(
    matricula: int,
    admissao: str,
    sindicato_colaborador: str,
    competencia: str,
    dias: int,
    valor_diario_vr: float,
    total: float,
    custo_empresa: float,
    desconto_profissional: float,
    obs_geral: Optional[str] = None
) -> str:
    """
    Adiciona uma nova linha ao DataFrame VR MENSAL.
    
    Args:
        matricula (int): Número da matrícula do colaborador
        admissao (str): Data de admissão (formato dd/mm/yyyy)
        sindicato_colaborador (str): Sindicato do colaborador
        competencia (str): Competência (formato MM/yyyy)
        dias (int): Quantidade de dias de VR
        valor_diario_vr (float): Valor diário do VR
        total (float): Valor total do VR no período
        custo_empresa (float): Custo para a empresa
        desconto_profissional (float): Desconto do profissional
        obs_geral (str, optional): Observações gerais
        
    Returns:
        str: Confirmação da operação ou mensagem de erro
        
    Example:
        add_vr_mensal(
            matricula=35741,
            admissao="07/04/2024", 
            sindicato_colaborador="SINDPD",
            competencia="04/2024",
            dias=22,
            valor_diario_vr=15.50,
            total=341.00,
            custo_empresa=272.80,
            desconto_profissional=68.20,
            obs_geral="Admissão em abril"
        )
    """
    try:
        # Verificar se o DataFrame existe
        if "vr_mensal" not in dataframes.dataframes:
            return "Erro: DataFrame VR MENSAL não encontrado no singleton."
        
        df = dataframes.dataframes["vr_mensal"]
        
        # Validações básicas
        if matricula <= 0:
            return "Erro: Matrícula deve ser um número positivo."
        
        if dias < 0:
            return "Erro: Dias não pode ser negativo."
        
        if valor_diario_vr < 0:
            return "Erro: Valor diário VR não pode ser negativo."
        
        # Validar formato de competência (MM/yyyy)
        try:
            mes, ano = competencia.split('/')
            if len(mes) != 2 or len(ano) != 4:
                raise ValueError
            int(mes)
            int(ano)
        except (ValueError, AttributeError):
            return "Erro: Competência deve estar no formato MM/yyyy (ex: 04/2024)."
        
        # Validar formato de data de admissão (dd/mm/yyyy)
        try:
            dia, mes, ano = admissao.split('/')
            if len(dia) != 2 or len(mes) != 2 or len(ano) != 4:
                raise ValueError
            int(dia)
            int(mes) 
            int(ano)
        except (ValueError, AttributeError):
            return "Erro: Data de admissão deve estar no formato dd/mm/yyyy (ex: 07/04/2024)."
        
        # Criar nova linha
        new_row = {
            'MATRICULA': matricula,
            'ADMISSAO': admissao,
            'SINDICATO_COLABORADOR': sindicato_colaborador,
            'COMPETENCIA': competencia,
            'DIAS': dias,
            'VALOR_DIARIO_VR': valor_diario_vr,
            'TOTAL': total,
            'CUSTO_EMPRESA': custo_empresa,
            'DESCONTO_PROFISSIONAL': desconto_profissional,
            'OBS_GERAL': obs_geral
        }
        
        # Verificar se já existe registro para a mesma matrícula e competência
        if not df.empty:
            existing = df[
                (df['MATRICULA'] == matricula) & 
                (df['COMPETENCIA'] == competencia)
            ]
            if not existing.empty:
                return f"Aviso: Já existe registro para matrícula {matricula} na competência {competencia}. Use update_vr_mensal para atualizar."
        
        # Validar se o total está correto (dias * valor_diario_vr)
        total_calculado = dias * valor_diario_vr
        if abs(total - total_calculado) > 0.01:  # Tolerância para arredondamento
            return f"Aviso: Total informado ({total}) difere do calculado ({total_calculado:.2f}). Verifique os valores."
        
        # Adicionar nova linha ao DataFrame
        df.loc[len(df)] = new_row
        
        # Atualizar o singleton (garantir que a referência seja mantida)
        dataframes.dataframes["vr_mensal"] = df
        
        return f"✅ Nova linha adicionada com sucesso! Matrícula: {matricula}, Competência: {competencia}, Total: R$ {total:.2f}"
        
    except Exception as e:
        return f"Erro ao adicionar nova linha ao VR MENSAL: {str(e)}"