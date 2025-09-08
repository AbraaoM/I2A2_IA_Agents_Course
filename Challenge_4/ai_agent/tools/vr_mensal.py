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