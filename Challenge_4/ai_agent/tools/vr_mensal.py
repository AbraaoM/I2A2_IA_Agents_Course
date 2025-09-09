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
    admissao: str = "",
    sindicato_colaborador: str = "",
    competencia: str = "",
    dias: int = 0,
    valor_diario_vr: float = 0.0,
    total: float = 0.0,
    custo_empresa: float = 0.0,
    desconto_profissional: float = 0.0,
    obs_geral: Optional[str] = None
) -> str:
    """
    Adiciona uma nova linha ao DataFrame VR MENSAL de forma simplificada.
    """
    try:
        if "vr_mensal" not in dataframes.dataframes:
            return "Erro: DataFrame VR MENSAL não encontrado no singleton."
        df = dataframes.dataframes["vr_mensal"]

        new_row = {
            'MATRICULA': matricula,
            'ADMISSAO': admissao,
            'SINDICATO DO COLABORADOR': sindicato_colaborador,
            'COMPETENCIA': competencia,
            'DIAS': dias,
            'VALOR DIARIO VR': valor_diario_vr,
            'TOTAL': total,
            'CUSTO EMPRESA': custo_empresa,
            'DESCONTO PROFISSIONAL': desconto_profissional,
            'OBS GERAL': obs_geral
        }

        df.loc[len(df)] = new_row
        dataframes.dataframes["vr_mensal"] = df

        return f"✅ Linha adicionada! Matrícula: {matricula}, Competência: {competencia}, Total: R$ {total:.2f}"
    except Exception as e:
        return f"Erro ao adicionar linha: {str(e)}"
    
@tool 
def update_vr_mensal_row(
    matricula: int,
    competencia: str,
    dias: Optional[int] = None,
    valor_diario_vr: Optional[float] = None,
    total: Optional[float] = None,
    custo_empresa: Optional[float] = None,
    desconto_profissional: Optional[float] = None,
    obs_geral: Optional[str] = None
) -> str:
    """
    Atualiza uma linha existente no DataFrame VR MENSAL com base na matrícula e competência.
    
    Args:
        matricula (int): Número da matrícula do colaborador
        competencia (str): Competência (formato MM/yyyy)
        dias (int, optional): Quantidade de dias de VR
        valor_diario_vr (float, optional): Valor diário do VR
        total (float, optional): Valor total do VR no período
        custo_empresa (float, optional): Custo para a empresa
        desconto_profissional (float, optional): Desconto do profissional
        obs_geral (str, optional): Observações gerais
        
    Returns:
        str: Confirmação da operação ou mensagem de erro
        
    Example:
        update_vr_mensal_row(
            matricula=35741,
            competencia="04/2024",
            dias=20,
            valor_diario_vr=16.00,
            total=320.00
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
        
        # Validar formato de competência (MM/yyyy)
        try:
            mes, ano = competencia.split('/')
            if len(mes) != 2 or len(ano) != 4:
                raise ValueError
            int(mes)
            int(ano)
        except (ValueError, AttributeError):
            return "Erro: Competência deve estar no formato MM/yyyy (ex: 04/2024)."
        
        # Localizar a linha a ser atualizada
        row_index = df[
            (df['MATRICULA'] == matricula) & 
            (df['COMPETENCIA'] == competencia)
        ].index
        
        if row_index.empty:
            return f"Erro: Nenhuma linha encontrada para matrícula {matricula} na competência {competencia}."
        
        # Pegar o primeiro índice (deve ser único)
        idx = row_index[0]
        
        # Lista para rastrear campos atualizados
        campos_atualizados = []
        
        # Atualizar apenas os campos fornecidos
        if dias is not None:
            if dias < 0:
                return "Erro: Dias não pode ser negativo."
            df.loc[idx, 'DIAS'] = dias
            campos_atualizados.append(f"Dias: {dias}")
        
        if valor_diario_vr is not None:
            if valor_diario_vr < 0:
                return "Erro: Valor diário VR não pode ser negativo."
            df.loc[idx, 'VALOR_DIARIO_VR'] = valor_diario_vr
            campos_atualizados.append(f"Valor Diário VR: R$ {valor_diario_vr:.2f}")
        
        if total is not None:
            if total < 0:
                return "Erro: Total não pode ser negativo."
            df.loc[idx, 'TOTAL'] = total
            campos_atualizados.append(f"Total: R$ {total:.2f}")
        
        if custo_empresa is not None:
            if custo_empresa < 0:
                return "Erro: Custo empresa não pode ser negativo."
            df.loc[idx, 'CUSTO_EMPRESA'] = custo_empresa
            campos_atualizados.append(f"Custo Empresa: R$ {custo_empresa:.2f}")
        
        if desconto_profissional is not None:
            if desconto_profissional < 0:
                return "Erro: Desconto profissional não pode ser negativo."
            df.loc[idx, 'DESCONTO_PROFISSIONAL'] = desconto_profissional
            campos_atualizados.append(f"Desconto Profissional: R$ {desconto_profissional:.2f}")
        
        if obs_geral is not None:
            df.loc[idx, 'OBS_GERAL'] = obs_geral
            campos_atualizados.append(f"Observações: {obs_geral}")
        
        # Verificar se pelo menos um campo foi fornecido para atualização
        if not campos_atualizados:
            return "Aviso: Nenhum campo foi fornecido para atualização."
        
        # Validação de consistência: se dias e valor_diario_vr foram fornecidos, verificar o total
        if dias is not None and valor_diario_vr is not None:
            total_calculado = dias * valor_diario_vr
            total_atual = df.loc[idx, 'TOTAL']
            
            if abs(total_atual - total_calculado) > 0.01:  # Tolerância para arredondamento
                return f"Aviso: Total atual ({total_atual}) não coincide com o calculado ({total_calculado:.2f}). Considere atualizar o total também."
        
        # Atualizar o singleton
        dataframes.dataframes["vr_mensal"] = df
        
        # Retornar confirmação detalhada
        campos_str = ", ".join(campos_atualizados)
        return f"✅ Linha atualizada com sucesso! Matrícula: {matricula}, Competência: {competencia}. Campos atualizados: {campos_str}"
        
    except Exception as e:
        return f"Erro ao atualizar linha no VR MENSAL: {str(e)}"

@tool
def delete_vr_mensal_row(matricula: int, competencia: str) -> str:
    """
    Remove uma linha do DataFrame VR MENSAL com base na matrícula e competência.
    
    Args:
        matricula (int): Número da matrícula do colaborador
        competencia (str): Competência (formato MM/yyyy)
        
    Returns:
        str: Confirmação da operação ou mensagem de erro
        
    Example:
        delete_vr_mensal_row(matricula=35741, competencia="04/2024")
    """
    try:
        # Verificar se o DataFrame existe
        if "vr_mensal" not in dataframes.dataframes:
            return "Erro: DataFrame VR MENSAL não encontrado no singleton."
        
        df = dataframes.dataframes["vr_mensal"]
        
        # Validações básicas
        if matricula <= 0:
            return "Erro: Matrícula deve ser um número positivo."
        
        # Validar formato de competência (MM/yyyy)
        try:
            mes, ano = competencia.split('/')
            if len(mes) != 2 or len(ano) != 4:
                raise ValueError
            int(mes)
            int(ano)
        except (ValueError, AttributeError):
            return "Erro: Competência deve estar no formato MM/yyyy (ex: 04/2024)."
        
        # Localizar a linha a ser removida
        row_index = df[
            (df['MATRICULA'] == matricula) & 
            (df['COMPETENCIA'] == competencia)
        ].index
        
        if row_index.empty:
            return f"Erro: Nenhuma linha encontrada para matrícula {matricula} na competência {competencia}."
        
        # Obter informações da linha antes de remover (para confirmação)
        linha_removida = df.loc[row_index[0]]
        total_removido = linha_removida['TOTAL']
        
        # Remover a linha
        df = df.drop(row_index)
        
        # Resetar índices
        df = df.reset_index(drop=True)
        
        # Atualizar o singleton
        dataframes.dataframes["vr_mensal"] = df
        
        return f"✅ Linha removida com sucesso! Matrícula: {matricula}, Competência: {competencia}, Total removido: R$ {total_removido:.2f}. Registros restantes: {len(df)}"
        
    except Exception as e:
        return f"Erro ao remover linha do VR MENSAL: {str(e)}"

@tool
def get_vr_mensal_by_matricula(matricula: int) -> str:
    """
    Busca todos os registros de VR MENSAL para uma matrícula específica.
    
    Args:
        matricula (int): Número da matrícula do colaborador
        
    Returns:
        str: Lista de registros encontrados ou mensagem de erro
        
    Example:
        get_vr_mensal_by_matricula(matricula=35741)
    """
    try:
        # Verificar se o DataFrame existe
        if "vr_mensal" not in dataframes.dataframes:
            return "Erro: DataFrame VR MENSAL não encontrado no singleton."
        
        df = dataframes.dataframes["vr_mensal"]
        
        # Validações básicas
        if matricula <= 0:
            return "Erro: Matrícula deve ser um número positivo."
        
        # Filtrar registros pela matrícula
        registros = df[df['MATRICULA'] == matricula]
        
        if registros.empty:
            return f"Nenhum registro encontrado para matrícula {matricula}."
        
        # Criar relatório detalhado
        relatorio = [f"📊 REGISTROS VR MENSAL PARA MATRÍCULA {matricula}:"]
        relatorio.append(f"Total de registros: {len(registros)}")
        relatorio.append("")
        
        for idx, row in registros.iterrows():
            relatorio.append(f"Competência: {row['COMPETENCIA']}")
            relatorio.append(f"  - Admissão: {row.get('ADMISSAO', 'N/A')}")
            relatorio.append(f"  - Sindicato: {row.get('SINDICATO_COLABORADOR', 'N/A')}")
            relatorio.append(f"  - Dias: {row['DIAS']}")
            relatorio.append(f"  - Valor Diário: R$ {row['VALOR_DIARIO_VR']:.2f}")
            relatorio.append(f"  - Total: R$ {row['TOTAL']:.2f}")
            relatorio.append(f"  - Custo Empresa: R$ {row['CUSTO_EMPRESA']:.2f}")
            relatorio.append(f"  - Desconto Prof.: R$ {row['DESCONTO_PROFISSIONAL']:.2f}")
            if row.get('OBS_GERAL'):
                relatorio.append(f"  - Observações: {row['OBS_GERAL']}")
            relatorio.append("")
        
        total_geral = registros['TOTAL'].sum()
        relatorio.append(f"💰 TOTAL GERAL: R$ {total_geral:.2f}")
        
        return "\n".join(relatorio)
        
    except Exception as e:
        return f"Erro ao buscar registros por matrícula: {str(e)}"