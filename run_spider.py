from utils.db_utils import DBClient
from spider.crawler import get_html_url, extract_inner_text, logger
from utils.rag_utils import RAGGenerator


def get_legal_data():
    """craw data and insert to db"""
    db = DBClient()
    rag = RAGGenerator()
    inner_url_lst = get_html_url()
    for inner_url in inner_url_lst:
        title, inner_text = extract_inner_text(inner_url)
        vector = rag.generate_embeddings(inner_text)
        logger.info("insert data to db")
        db.insert_data(title, inner_url, inner_text, vector)
    db.close()


if __name__ == "__main__":
    get_legal_data()