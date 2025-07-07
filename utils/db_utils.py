import psycopg2
from config import HOST, PORT, USER, PASSWORD, DATABASE


class DBClient(object):
    def __init__(self):
        self._conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
        self._cursor = self._conn.cursor()

    def find_similar_texts(self, query_vector: list, threshold: float, k: int):
        """找出与查询向量预先距离值最近的数据行"""
        sql = """
        SELECT 
            id,
            url,
            row_text,
            title, 
            row_vector <=> CAST(%s AS VECTOR) AS distance
        FROM legal_text
        WHERE 
            row_vector <=> CAST(%s AS VECTOR) > %s
        ORDER BY 
            row_vector <=> CAST(%s AS VECTOR) ASC
        LIMIT %s
        """

        params = (query_vector, query_vector, threshold, query_vector, k)

        self._cursor.execute(sql, params)
        results = self._cursor.fetchall()
        return results

    def insert_data(self, title, url, raw_text, vector):
        try:
            # 使用PostgreSQL的vector扩展支持的格式
            # 将向量转换为PostgreSQL数组字符串格式
            vector_array = "[" + ",".join(map(str, vector)) + "]"

            # 插入数据的SQL语句
            insert_sql = """INSERT INTO legal_text (title, url, row_text, row_vector) VALUES (%s, %s, %s, %s)"""
            # 执行插入
            self._cursor.execute(insert_sql, (title, url, raw_text, vector_array))
            # 提交事务
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            print(f"数据库插入错误: {e}")
            raise

    def close(self):
        self._conn.close()


if __name__ == '__main__':
    db = DBClient()
    # 测试插入数据
    # db.insert_data('ssss', '22222', [-0.00093536545]*768)
    # 测试向量搜索
    from rag_utils import RAGGenerator
    rag = RAGGenerator()
    vector = rag.generate_embeddings("What was the supplement to the 1950 Washington State Revised Code?")
    print(vector)
    result = db.find_similar_texts(vector, 0.6, 5)
    print(result)