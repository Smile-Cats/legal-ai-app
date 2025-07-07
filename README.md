# legal-ai-app

一个法律AI问答系统，使用RAG技术，让用户在询问法律问题时，系统可以根据资料库向用户生成合适的答案，系统生成的答案会展示法律信息的来源。

## 主要功能
1. 数据抓取，系统需要从华盛顿法律网上抓取相关法律数据，并保存到数据库，数据库使用postgresql，并开启向量支持功能
2. 将法律文本数据以向量的形式保存进数据库
3. 一个问答界面，当用户提出问题时，AI需要给出答案，并附上相关的引用链接

## 项目结构

- spider   // 爬虫文件
- sqls
  - create_table.sql   // 创建表语句
  - legal_text.sql  //  一些测试数据
- templates
- utils
  - db_utils.py  // 连接postgresql数据库
  - rag_utils.py  //  使用查询到的资料生成回答
- app.py  //  flask app的主文件
- run_spider.py  //  爬虫运行的文件
- config.py  //  配置文件

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

