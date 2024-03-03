import mysql.connector
import sqlite3
import pandas as pd


tabela = "raw_data"
conn = mysql.connector.connect(
    host='40b8f30251.nxcli.io',
    user='a4f2b49a_padawan',
    password='KaratFlanksUgliedSpinal',
    database='a4f2b49a_sample_database'
)

query = f"SELECT datahora_acesso, modalidade, rake, clientes_id FROM {tabela}"
df = pd.read_sql_query(query, con=conn)
conn.close()

df["ano_mes"] = df['datahora_acesso'].str.slice(0, 7)
df_rake = df.groupby('ano_mes')['rake'].sum().reset_index()

df_players = df.groupby('ano_mes')['clientes_id'].nunique().reset_index()
df_players = df_players.rename(columns={'clientes_id': 'jogadores'})

df_rake_cash = df[df['modalidade'] == "Cash Game"].groupby('ano_mes')['rake'].sum().reset_index()
df_rake_cash = df_rake_cash.rename(columns={'rake': 'rake_cash_game'})

df_rake_torneio = df[df['modalidade'] == "Torneio"].groupby('ano_mes')['rake'].sum().reset_index()
df_rake_torneio = df_rake_torneio.rename(columns={'rake': 'rake_torneio'})

df_players_cash = df[df['modalidade'] == "Cash Game"].groupby('ano_mes')['clientes_id'].nunique().reset_index()
df_players_cash = df_players_cash.rename(columns={'clientes_id': 'jogadores_cash_game'})

df_players_torneio = df[df['modalidade'] == "Torneio"].groupby('ano_mes')['clientes_id'].nunique().reset_index()
df_players_torneio = df_players_torneio.rename(columns={'clientes_id': 'jogadores_torneio'})

df_new_players = df.groupby('clientes_id')['ano_mes'].min().reset_index()
df_new_players = df_new_players.groupby('ano_mes')['clientes_id'].nunique().reset_index()
df_new_players = df_new_players.rename(columns={'clientes_id': 'novos_jogadores'})

df = pd.merge(df_rake, df_players, on="ano_mes")\
    .merge(df_rake_cash, on="ano_mes")\
    .merge(df_rake_torneio, on="ano_mes")\
    .merge(df_players_cash, on="ano_mes")\
    .merge(df_players_torneio, on="ano_mes")\
    .merge(df_new_players, on="ano_mes")

conn = sqlite3.connect('H2.db')
df.to_sql(name=tabela, con=conn, if_exists='replace', index=False)
conn.close()
