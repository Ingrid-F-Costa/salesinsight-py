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

MESES_PT = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}


def criar_colunas_derivadas(df):
    """Cria colunas derivadas a partir do dataset limpo."""
    df = df.copy()

    # receita da linha (operacao vetorizada)
    df["receita_total"] = df["quantidade"] * df["preco_unitario"]

    # componentes da data
    df["mes"] = df["data_venda"].dt.month
    df["mes_nome"] = df["mes"].map(MESES_PT)
    df["trimestre"] = "Q" + df["data_venda"].dt.quarter.astype(str)
    df["ano"] = df["data_venda"].dt.year

    # faixa de valor da linha (transformacao condicional com np.select)
    condicoes = [
        df["receita_total"] < 500,
        (df["receita_total"] >= 500) & (df["receita_total"] < 5000),
        df["receita_total"] >= 5000,
    ]
    faixas = ["Baixo Valor", "Medio Valor", "Alto Valor"]
    df["faixa_receita_item"] = np.select(condicoes, faixas, default="Nao Classificado")

    return df


# Usar a funcao no dataset limpo
df_final = criar_colunas_derivadas(df_limpo)
print(df_final[["data_venda", "quantidade", "preco_unitario", "receita_total",
                "mes", "mes_nome", "trimestre", "ano", "faixa_receita_item"]].head())
print(df_final["faixa_receita_item"].value_counts())

def calcular_metricas(df):
    """
    Calcula as metricas agregadas do dataset.
    Retorna um dicionario no formato {nome_da_metrica: DataFrame}.
    """
    metricas = {}

    # receita, quantidade e numero de vendas por mes
    metricas["por_mes"] = (
        df.groupby("mes")
        .agg(receita_total=("receita_total", "sum"),
             quantidade=("quantidade", "sum"),
             n_vendas=("id_venda", "count"))
        .reset_index()
    )

    # top 5 produtos por receita
    metricas["top_produtos"] = (
        df.groupby("produto")["receita_total"].sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    # receita por categoria
    metricas["por_categoria"] = (
        df.groupby("categoria")["receita_total"].sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    # receita total e ticket medio por regiao
    metricas["por_regiao"] = (
        df.groupby("regiao")
        .agg(receita_total=("receita_total", "sum"),
             ticket_medio=("receita_total", "mean"))
        .sort_values("receita_total", ascending=False)
        .reset_index()
    )

    # exibir no console
    for nome, tabela in metricas.items():
        print(f"\n=== {nome.upper().replace('_', ' ')} ===")
        print(tabela.round(2).to_string(index=False))

    return metricas


# Usar a funcao no dataset com as colunas derivadas
metricas = calcular_metricas(df_final)

def segmentar_clientes(df):
    """
    Agrupa por cliente, soma a receita e classifica em
    Bronze / Prata / Ouro.
    Retorna um DataFrame com: cliente, total_gasto, segmento.
    """
    clientes = (
        df.groupby("cliente")["receita_total"].sum()
        .reset_index()
        .rename(columns={"receita_total": "total_gasto"})
        .sort_values("total_gasto", ascending=False)
        .reset_index(drop=True)
    )

    # funcao lambda aplicada com .apply()
    clientes["segmento"] = clientes["total_gasto"].apply(
        lambda gasto: "Bronze" if gasto < 5000
        else ("Prata" if gasto <= 15000 else "Ouro")
    )

    print("\n=== TOP 10 CLIENTES ===")
    print(clientes.head(10).round(2).to_string(index=False))

    print("\n=== DISTRIBUICAO POR SEGMENTO ===")
    print(clientes["segmento"].value_counts())

    return clientes


# Usar a funcao no dataset com as colunas derivadas
segmentacao = segmentar_clientes(df_final)

import matplotlib.pyplot as plt
import seaborn as sns
import os

CORES_CATEGORIA = {"Computadores": "#1f4e79", "Celulares": "#e07b39", "Periféricos": "#2a9d8f"}


def gerar_graficos(df, metricas, pasta="outputs/graficos", mostrar=False):
    """Gera as 4 figuras do projeto e salva em PNG."""
    os.makedirs(pasta, exist_ok=True)
    sns.set_theme(style="whitegrid")
    plt.rcParams["axes.titlesize"] = 14

    por_mes = metricas["por_mes"]
    top_produtos = metricas["top_produtos"]
    por_regiao = metricas["por_regiao"]

    # --- 1. linha: receita por mes ---
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(por_mes["mes"], por_mes["receita_total"],
            marker="o", linewidth=2, color="#1f4e79", label="Receita total")
    ax.set_title("Receita Total por Mes")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Receita Total (R$)")
    ax.set_xticks(range(1, 13))
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{pasta}/receita_por_mes.png", dpi=150)
    if mostrar:
        plt.show()
    plt.close()

    # --- 2. barras: top 5 produtos ---
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_produtos, y="produto", x="receita_total",
                hue="produto", legend=False, palette="Blues_d", ax=ax)
    ax.set_title("Top 5 Produtos por Receita")
    ax.set_xlabel("Receita Total (R$)")
    ax.set_ylabel("Produto")
    plt.tight_layout()
    plt.savefig(f"{pasta}/top_produtos.png", dpi=150)
    if mostrar:
        plt.show()
    plt.close()

    # --- 3. dispersao: quantidade x receita, colorido por categoria ---
    fig, ax = plt.subplots(figsize=(12, 6))
    for categoria, cor in CORES_CATEGORIA.items():
        parte = df[df["categoria"] == categoria]
        ax.scatter(parte["quantidade"], parte["receita_total"],
                   color=cor, alpha=0.7, label=categoria)
    ax.set_title("Quantidade Vendida x Receita por Transacao")
    ax.set_xlabel("Quantidade")
    ax.set_ylabel("Receita da Transacao (R$)")
    ax.legend(title="Categoria")
    plt.tight_layout()
    plt.savefig(f"{pasta}/quantidade_vs_receita.png", dpi=150)
    if mostrar:
        plt.show()
    plt.close()

    # --- 4. painel 2x2 ---
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))

    axes[0, 0].plot(por_mes["mes"], por_mes["receita_total"],
                    marker="o", linewidth=2, color="#1f4e79", label="Receita total")
    axes[0, 0].set_title("Receita por Mes")
    axes[0, 0].set_xlabel("Mes")
    axes[0, 0].set_ylabel("Receita (R$)")
    axes[0, 0].legend()

    axes[0, 1].bar(top_produtos["produto"], top_produtos["receita_total"],
                   color="#2a9d8f")
    axes[0, 1].set_title("Top 5 Produtos")
    axes[0, 1].set_xlabel("Produto")
    axes[0, 1].set_ylabel("Receita (R$)")
    axes[0, 1].tick_params(axis="x", rotation=30)

    for categoria, cor in CORES_CATEGORIA.items():
        parte = df[df["categoria"] == categoria]
        axes[1, 0].scatter(parte["quantidade"], parte["receita_total"],
                           color=cor, alpha=0.7, label=categoria)
    axes[1, 0].set_title("Quantidade x Receita")
    axes[1, 0].set_xlabel("Quantidade")
    axes[1, 0].set_ylabel("Receita (R$)")
    axes[1, 0].legend(title="Categoria")

    axes[1, 1].bar(por_regiao["regiao"], por_regiao["receita_total"],
                   color="#e07b39")
    axes[1, 1].set_title("Receita por Regiao")
    axes[1, 1].set_xlabel("Regiao")
    axes[1, 1].set_ylabel("Receita (R$)")
    axes[1, 1].tick_params(axis="x", rotation=30)

    fig.suptitle("SalesInsight PY - Painel Resumo", fontsize=16)
    plt.tight_layout()
    plt.savefig(f"{pasta}/painel_resumo.png", dpi=150)
    if mostrar:
        plt.show()
    plt.close()

    print(f"4 graficos salvos em {pasta}/")


# mostrar=True exibe os graficos aqui no Colab
gerar_graficos(df_final, metricas, mostrar=True)
