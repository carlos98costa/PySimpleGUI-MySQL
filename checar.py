import mysql.connector
from mysql.connector import Error

def read_query(cnx, query):
    cursor = cnx.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

puxarDados = """
SELECT *
FROM tbl_users;
"""

cnx = mysql.connector.connect(user='root',
                                database='pysimpleguitest',
                                charset='utf8mb4')
results = read_query(cnx, puxarDados)

for result in results:
  print(result)