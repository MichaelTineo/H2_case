import pandas as pd
import sqlite3


conn = sqlite3.connect('H2.db')

query = """
    SELECT
        SUBSTR(data_acesso, 1, 7) ano_mes,
        printf('R$%.2f', SUM(rake)) rake
    FROM resultado
    GROUP BY SUBSTR(data_acesso, 1, 7)
    ORDER BY ano_mes DESC
"""

result = pd.read_sql_query(query, conn)
print(result)

conn.close()
