import pandas as pd
import sqlite3

conn = sqlite3.connect('H2.db')
tabelas = ["clientes", "resultado"]

for tabela in tabelas:
    df = pd.read_csv(f"{tabela}.csv")
    df.to_sql(name=tabela, con=conn, if_exists='replace', index=False)

conn.close()
