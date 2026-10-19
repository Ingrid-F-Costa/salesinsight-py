# SalesInsight PY - Analise e Visualizacao de Dados de Vendas
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def gerar_dataset_vendas(n_registros=200, seed=42):
    """Gera um dataset sintético de vendas com dados sujos."""
    random.seed(seed)
    np.random.seed(seed)

    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor",
                "Teclado", "Mouse", "Headset"]
    categorias = {"Notebook": "Computadores", "Smartphone": "Celulares",
                  "Tablet": "Celulares", "Monitor": "Computadores",
                  "Teclado": "Periféricos", "Mouse": "Periféricos",
                  "Headset": "Periféricos"}
    precos = {"Notebook": 3500, "Smartphone": 2200, "Tablet": 1800,
              "Monitor": 1200, "Teclado": 250, "Mouse": 120,
              "Headset": 350}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

    data_inicio = datetime(2025, 1, 1)
    dados = []

    for i in range(n_registros):
        produto = random.choice(produtos)
        categoria = categorias[produto]
        quantidade = random.randint(1, 10)
        preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
        data = data_inicio + timedelta(days=random.randint(0, 364))
        data_txt = data.strftime("%Y-%m-%d")
        cliente = f"Cliente_{random.randint(1, 50):03d}"

        # --- sujeira proposital para a etapa de limpeza ---
        if random.random() < 0.03:
            data_txt = "DATA INVALIDA"

        dados.append({
            "id_venda": i + 1,
            "data_venda": data_txt,
            "cliente": cliente,
            "produto": produto,
            "categoria": categoria,
            "regiao": random.choice(regioes),
            "quantidade": quantidade,
            "preco_unitario": preco,
        })

    return pd.DataFrame(dados)

# Gerar e salvar o CSV bruto
df_bruto = gerar_dataset_vendas()
df_bruto.to_csv("vendas.csv", index=False)
print(f"Dataset gerado com {len(df_bruto)} registros.")
print(df_bruto.head())

def inspecionar_dados(df):
    """Exibe as informacoes estruturais do DataFrame."""
    print("\n=== INSPECAO INICIAL DO DATASET ===")
    print(f"Shape: {df.shape}")
    print(f"\nColunas: {list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nValores nulos por coluna:\n{df.isnull().sum()}")
    print(f"\nPrimeiros registros:\n{df.head()}")
    return df

# Carregar o CSV que foi salvo no RF01 e inspecionar
df = pd.read_csv("vendas.csv")
inspecionar_dados(df)

def tratar_dados(df):
    """
    Trata o DataFrame de vendas.
    Retorna: (df_limpo, relatorio)
    """
    df = df.copy()
    total_inicial = len(df)

    # 1. remover espacos extras nas colunas de texto
    colunas_texto = ["cliente", "produto", "categoria", "regiao"]
    celulas_com_espaco = 0
    for coluna in colunas_texto:
        texto_limpo = df[coluna].str.strip()
        celulas_com_espaco += int((texto_limpo != df[coluna]).sum())
        df[coluna] = texto_limpo

    # 2. converter data_venda e descartar datas invalidas
    df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce")
    datas_invalidas = int(df["data_venda"].isna().sum())
    df = df.dropna(subset=["data_venda"]).copy()

    # 3. ajustar os tipos numericos
    convertidos_quantidade = 0
    if df["quantidade"].dtype != "int64":
        convertidos_quantidade = len(df)
        df["quantidade"] = df["quantidade"].astype(int)

    convertidos_preco = 0
    if df["preco_unitario"].dtype != "float64":
        convertidos_preco = len(df)
        df["preco_unitario"] = df["preco_unitario"].astype(float)

    df = df.reset_index(drop=True)

    # 4. montar e imprimir o relatorio de limpeza
    relatorio = {
        "registros_iniciais": total_inicial,
        "removidos_data_invalida": datas_invalidas,
        "convertidos_data_para_datetime": len(df),
        "convertidos_quantidade_para_int": convertidos_quantidade,
        "convertidos_preco_para_float": convertidos_preco,
        "sem_alteracao_de_tipo_quantidade": len(df) - convertidos_quantidade,
        "sem_alteracao_de_tipo_preco": len(df) - convertidos_preco,
        "celulas_de_texto_com_espaco_corrigidas": celulas_com_espaco,
        "registros_finais": len(df),
    }

    print("\n=== RELATORIO DE LIMPEZA ===")
    for chave, valor in relatorio.items():
        print(f"{chave}: {valor}")

    return df, relatorio


# Usar a funcao no dataset lido do CSV
df_limpo, relatorio = tratar_dados(df)
print(df_limpo.dtypes)
