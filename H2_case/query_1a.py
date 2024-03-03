import pandas as pd
import sqlite3


conn = sqlite3.connect('H2.db')

# No enunciado do teste não deixa claro se os nascidos em 2010 são Z ou Alpha, eu considerei Alpha.
query = """
    WITH temp AS (
        SELECT 
            id,
            CASE
                WHEN CAST(SUBSTR(data_nascimento, 1, 4) AS INT) <= 1940 THEN 'Veterano'
                WHEN CAST(SUBSTR(data_nascimento, 1, 4) AS INT) <= 1959 THEN 'Baby Boomer'
                WHEN CAST(SUBSTR(data_nascimento, 1, 4) AS INT) <= 1979 THEN 'Geração X'
                WHEN CAST(SUBSTR(data_nascimento, 1, 4) AS INT) <= 1995 THEN 'Geração Y'
                WHEN CAST(SUBSTR(data_nascimento, 1, 4) AS INT) <= 2009 THEN 'Geração Z'
                ELSE 'Geração Alpha'
            END geracao
        FROM clientes
    )
    SELECT 
        geracao,
        printf('R$%.2f', SUM(rake)) rake_total
    FROM  resultado
    INNER JOIN temp ON id = clientes_id
    GROUP BY geracao
    ORDER BY SUM(rake) DESC
"""

result = pd.read_sql_query(query, conn)
print(result)

conn.close()
