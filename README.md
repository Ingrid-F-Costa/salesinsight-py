# SalesInsight PY

## Sobre o projeto

Análise e visualização de dados de vendas desenvolvida em Python. O projeto simula o trabalho de um analista de dados júnior de uma empresa de varejo que precisa preparar um relatório para a reunião trimestral da diretoria. Ele carrega, limpa, transforma, agrega e visualiza um dataset de vendas, gera métricas por período, produto, categoria e região, e faz uma segmentação simples de clientes por faixa de gasto.

## O que o projeto analisa

- Receita total e volume de vendas por mês e por trimestre
- Top produtos e categorias por receita
- Desempenho por região
- Segmentação de clientes por nível de gasto (Bronze, Prata e Ouro)
- Relação entre quantidade vendida e receita por transação
- Exportação de relatórios em CSV e JSON e de gráficos em PNG

## Principais resultados

O dataset é sintético (gerado pelo próprio código, com semente fixa), então os números abaixo são ilustrativos e se repetem a cada execução.

- Dos 200 registros gerados, 6 foram removidos por data inválida e 194 foram analisados.
- Receita total de R$ 1.380.210,31, ticket médio de R$ 7.114,49 e 49 clientes.
- O Notebook é o produto de maior receita (R$ 493.242,63), e a categoria Computadores lidera.
- A região Centro-Oeste tem a maior receita total, e o Nordeste tem o maior ticket médio (R$ 8.653,08).
- Segmentação de clientes: 35 Ouro, 9 Prata e 5 Bronze.

## Conceitos aplicados (Módulo 01, Semanas 01 a 07)

- Lógica de programação: variáveis, tipos de dados, operadores, condicionais e repetição
- Estruturas de dados: listas, dicionários e estruturas compostas
- Funções: parâmetros, retorno, docstring, funções lambda e função de ordem superior
- Leitura e escrita de arquivos CSV e JSON
- Módulo datetime e conversão de tipos
- Pandas: DataFrames, filtros, groupby, np.select e transformações com apply
- Matplotlib e Seaborn: linha, barras, dispersão, subplots, customização e exportação em PNG
- Programação orientada a objetos básica: classe que organiza o fluxo
- Git e GitHub: branches, commits descritivos e pull requests

## Como executar

### Google Colab (recomendado)

1. Abra um notebook novo em colab.research.google.com.
2. Cole todo o conteúdo do arquivo `salesinsight.py` em uma célula e execute. Os gráficos aparecem na tela.
3. Alternativa: faça upload do `salesinsight.py` e execute `!python salesinsight.py`. Nesse caso os gráficos são salvos em PNG, mas não aparecem na tela.

O arquivo `vendas.csv` é gerado automaticamente na primeira execução, então não é preciso enviá-lo.

### Localmente (VS Code ou terminal)

1. Instale o Python 3.10 ou superior.
2. Instale as dependências com `pip install pandas numpy matplotlib seaborn`.
3. Execute no terminal `python salesinsight.py`.

## Estrutura do projeto

    salesinsight-py/
    |-- salesinsight.py              # fluxo principal
    |-- README.md
    |-- vendas.csv                   # gerado na primeira execução
    |-- outputs/                     # criada na execução
        |-- metricas_por_mes.csv
        |-- segmentacao_clientes.csv
        |-- estatisticas_gerais.json
        |-- graficos/
            |-- receita_por_mes.png
            |-- top_produtos.png
            |-- quantidade_vs_receita.png
            |-- painel_resumo.png

## Organização do código

Cada etapa do fluxo é uma função com parâmetros, retorno e docstring: gerar o dataset, inspecionar, tratar, criar colunas derivadas, calcular métricas, segmentar clientes, gerar gráficos e exportar resultados. A classe `AnalisadorDeVendas` guarda os dados e chama as etapas na ordem certa, e a função `main()` executa o fluxo completo a partir do bloco `if __name__ == "__main__":`.

## Decisões técnicas

- **Remover datas inválidas em vez de preenchê-las.** Uma data inventada distorceria os resultados por mês e por trimestre. Como apenas 6 de 200 registros foram afetados, removê-los preserva a confiabilidade da análise. O relatório de limpeza informa quantos registros entraram, quantos foram removidos e quantos permaneceram.
- **Limpeza antes de qualquer transformação.** A conversão de datas acontece antes das colunas derivadas, das agregações e dos gráficos, para que nenhuma etapa trabalhe com dados inválidos.
- **Operações vetorizadas.** A receita por linha e as faixas de valor (`np.select`) são calculadas na tabela inteira de uma vez, sem laços, o que é mais rápido e mais legível.
- **Semente fixa (seed=42).** Garante que qualquer pessoa que execute o projeto obtenha o mesmo dataset e os mesmos resultados.

## Oportunidades de melhoria

- Aceitar um CSV externo e os caminhos de saída por argumentos de linha de comando
- Adicionar testes automatizados para as funções de limpeza e de métricas
- Incluir gráficos adicionais, como histograma, boxplot e mapa de calor
- Enriquecer o dataset com uma tabela auxiliar de metas por região (merge) ou uma tabela cruzada de mês por categoria

## Versionamento

O projeto segue um GitFlow simplificado, com commits descritivos no padrão conventional commits.

- `main`: versão final e estável
- `develop`: integração do trabalho
- `feat/pipeline-dados`: desenvolvimento do fluxo de dados, das métricas, dos gráficos e da classe
- `docs/readme`: documentação do projeto

## Ferramentas utilizadas

- Python 3.10 ou superior
- Google Colab
- Bibliotecas: pandas, numpy, matplotlib, seaborn, json, datetime, os, random e sys
- GitHub para versionamento

## Vídeo de demonstração

[inserir o link do vídeo aqui]

*Projeto desenvolvido para o curso Desenvolvedor(a) em IA para Análise Preditiva, Módulo 01, Semana 07.*
