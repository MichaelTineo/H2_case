import pandas as pd
import sqlite3


conn = sqlite3.connect('H2.db')

# Considerando todos os clientes cadastrados, sexo feminino tem maior percentual de ganhadoras.
# Considerando apenas os clientes ativos (que tenham pelo menos um registro de resultado), o sexo masculino tem maior
# percentual de ganhadores.
query = """
    WITH winners AS (
    SELECT
        clientes_id,
        CASE WHEN SUM(winning) > 0 THEN 1 ELSE 0 END winner
    FROM resultado
    GROUP BY clientes_id
    )
    SELECT
        sexo,
        COUNT(1) qty_customers,
        SUM(winner) qty_winners,
        printf('%.2f%', CAST(SUM(winner) AS REAL) / COUNT(1) * 100) percent_winners
    FROM clientes
    LEFT JOIN winners ON clientes_id = id
    WHERE sexo IS NOT NULL
    GROUP BY sexo
    ORDER BY percent_winners DESC
"""

result = pd.read_sql_query(query, conn)
print(result)

conn.close()
