"""
-> Exemplos:
    serie_ou_dataframe.apply(funcao, axis=0)  # Aplicar às colunas (axis=0)
    serie_ou_dataframe.apply(funcao, axis=1)  # Aplicar às linhas (axis=1)
"""

import pandas as pd

dados = {'Nome': ['Alice', 'Bob', 'Charlie'], 'Idade': [25, 30, 22]}
df = pd.DataFrame(dados)

# Cria nova coluna Idade Dobrada = a função dobrar_idade de cada linha da coluna Idade
df['Idade Dobrada'] = df['Idade'].apply(lambda idade: idade * 2)

print(df)