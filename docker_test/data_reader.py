import pymysql
import pandas as pd

def query_table(table_name):
    try:
        # 建立連線
        conn = pymysql.connect(
            host='172.31.2.96',
            user='eds',
            password='!2018Eds',
            database='sports_unify_db',
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        return df
    except Exception as e:
        print(f"[DataReader] Failed to read table `{table_name}`: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()
