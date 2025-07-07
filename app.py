from flask import Flask, request, jsonify, render_template
from utils.db_utils import DBClient
from utils.rag_utils import RAGGenerator
from config import SIMILARTHRESOLD, LIMIT

app = Flask(__name__)


@app.route('/ask', methods=['POST'])
def ask_question():
    """处理用户提问"""
    data = request.get_json()
    question = data.get('question', '').strip()

    if not question:
        return jsonify({"error": "please enter question"}), 400

    # 从数据库检索相关知识
    db = DBClient()
    rag = RAGGenerator()
    query_vector = rag.generate_embeddings(question)  # 生成嵌入向量
    context_docs = db.find_similar_texts(query_vector, SIMILARTHRESOLD, LIMIT)  # 从数据库中找到与输入向量相似的行
    db.close()

    # 生成回答
    answer = rag.generate_answer(question, context_docs)

    # 返回结果
    return jsonify({
        "question": question,
        "answer": answer,
        "sources": [{
            "id": doc[0],
            "title": doc[3],
            "url": doc[1],
        } for doc in context_docs]
    })


@app.route('/')
def index():
    """渲染前端界面"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)