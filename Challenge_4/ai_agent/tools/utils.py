from langchain_core.tools import tool
import pandas as pd
from io import StringIO
import os
from datetime import datetime

@tool
def response_to_df(response: str) -> pd.DataFrame:
    """
    Tenta converter uma resposta tabular (CSV ou Markdown) em DataFrame pandas.
    Limpa separadores e espaços dos nomes das colunas e dos valores das células.
    """
    def clean_cell(cell):
        if isinstance(cell, str):
            return cell.strip().replace('|', '').strip()
        return cell

    # Tenta ler como CSV
    try:
        df = pd.read_csv(StringIO(response))
        df.columns = [clean_cell(col) for col in df.columns]
        df = df.applymap(clean_cell)
        return df
    except Exception:
        print("Não foi possível converter a resposta em DataFrame CSV.")
        pass
    # Tenta ler como tabela Markdown
    try:
        df = pd.read_table(StringIO(response), sep="|", engine="python")
        # df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = [clean_cell(col) for col in df.columns]
        df = df.applymap(clean_cell)
        return df
    except Exception:
        print("Não foi possível converter a resposta em DataFrame.")
        pass
    return None


@tool
def df_to_excel(dataframe_data: str, filename: str = None) -> str:
    """
    Converte um DataFrame em arquivo Excel (.xlsx).
    
    Args:
        dataframe_data (str): Dados do DataFrame em formato CSV ou tabular
        filename (str, optional): Nome do arquivo. Se None, gera automaticamente
        
    Returns:
        str: Caminho do arquivo Excel gerado ou mensagem de erro
    """
    try:
        # Primeiro converte para DataFrame
        df = response_to_df.invoke(dataframe_data)
        
        if df is None or df.empty:
            return "Erro: Não foi possível converter os dados em DataFrame válido"
        
        # Gerar nome do arquivo se não fornecido
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_{timestamp}.xlsx"
        
        # Garantir extensão .xlsx
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        # Caminho completo do arquivo
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filepath = os.path.join(output_dir, filename)
        
        # Salvar como Excel
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        return f"Arquivo Excel gerado com sucesso: {filepath}"
        
    except Exception as e:
        return f"Erro ao gerar arquivo Excel: {str(e)}"


@tool
def df_to_csv(dataframe_data: str, filename: str = None) -> str:
    """
    Converte um DataFrame em arquivo CSV.
    
    Args:
        dataframe_data (str): Dados do DataFrame em formato CSV ou tabular
        filename (str, optional): Nome do arquivo. Se None, gera automaticamente
        
    Returns:
        str: Caminho do arquivo CSV gerado ou mensagem de erro
    """
    try:
        # Primeiro converte para DataFrame
        df = response_to_df.invoke(dataframe_data)
        
        if df is None or df.empty:
            return "Erro: Não foi possível converter os dados em DataFrame válido"
        
        # Gerar nome do arquivo se não fornecido
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_{timestamp}.csv"
        
        # Garantir extensão .csv
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        # Caminho completo do arquivo
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filepath = os.path.join(output_dir, filename)
        
        # Salvar como CSV
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        return f"Arquivo CSV gerado com sucesso: {filepath}"
        
    except Exception as e:
        return f"Erro ao gerar arquivo CSV: {str(e)}"


@tool 
def gerar_planilha_excel(dataframe_data: str, filename: str = "relatorio_vr_mensal", add_summary: bool = True) -> str:
    """
    Gera uma planilha Excel formatada a partir de dados tabulares, ideal para relatórios VR.
    
    Args:
        dataframe_data (str): Dados do DataFrame em formato CSV ou tabular
        filename (str): Nome base do arquivo (sem extensão)
        add_summary (bool): Se True, adiciona aba com resumo dos dados
        
    Returns:
        str: Caminho do arquivo Excel gerado com formatação ou mensagem de erro
    """
    try:
        # Converter para DataFrame
        df = response_to_df.invoke(dataframe_data)
        
        if df is None or df.empty:
            return "Erro: Não foi possível converter os dados em DataFrame válido"
        
        # Preparar arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_final = f"{filename}_{timestamp}.xlsx"
        
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filepath = os.path.join(output_dir, filename_final)
        
        # Criar Excel com formatação
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Aba principal com dados
            df.to_excel(writer, sheet_name='Relatório', index=False)
            
            # Formatação da aba principal
            worksheet = writer.sheets['Relatório']
            
            # Ajustar largura das colunas
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Aba de resumo (se solicitado)
            if add_summary:
                resumo_data = {
                    'Métrica': [
                        'Total de Registros',
                        'Colaboradores Afastados',
                        'Colaboradores Ativos',
                        'Data de Geração'
                    ],
                    'Valor': [
                        len(df),
                        len(df[df.get('AFASTADO', '') == 'SIM']) if 'AFASTADO' in df.columns else 'N/A',
                        len(df[df.get('AFASTADO', '') == 'NÃO']) if 'AFASTADO' in df.columns else 'N/A',
                        datetime.now().strftime("%d/%m/%Y %H:%M")
                    ]
                }
                
                df_resumo = pd.DataFrame(resumo_data)
                df_resumo.to_excel(writer, sheet_name='Resumo', index=False)
        
        return f"Planilha Excel formatada gerada com sucesso: {filepath}"
        
    except Exception as e:
        return f"Erro ao gerar planilha Excel: {str(e)}"