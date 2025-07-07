# legal-ai-app

一个法律RAG应用

## 配置

使用前需修改 config.py文件

## 爬虫运行

`python run_spider`

## web运行

`python app.py`

## 表结构设计
| 字段名  | 含义        |
|------|-----------|
| id | 自增主键      |
| url | 网页链接      |
| title | 网页标题      |
| row_text | 网页文本      |
| row_vector | 网页文本转化的向量 |

