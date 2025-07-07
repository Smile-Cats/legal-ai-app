# postgresql config
HOST = "127.0.0.1"
PORT = 5432
USER = "postgres"
PASSWORD = "abCD20.."
DATABASE = "postgres"

# openai config
APIKEY = "ollama"  # openai的api-key
AIURL = "http://localhost:11434/v1"  # openai的url，如果是本地模型则填写为本地url

CHAT_MODEL = "deepseek-r1:7b"  # 问答模型
EMBED_MODEL = "nomic-embed-text:latest"  # 嵌入模型
SIMILARTHRESOLD = 0.6  # 余弦相似度阈值，大于这个值的是相似文本
LIMIT = 5  # 最多展示5个来源