from openai import OpenAI
from config import AIURL, APIKEY, CHAT_MODEL, EMBED_MODEL


class RAGGenerator:
    def __init__(self):
        self._client = OpenAI(
            base_url=AIURL,
            api_key=APIKEY,
        )

    def generate_embeddings(self, text):
        """将切割好的文本使用openai生成嵌入向量"""
        response = self._client.embeddings.create(
            input=text,
            model=EMBED_MODEL
        )
        return response.data[0].embedding

    def generate_answer(self, question: str, context: list) -> str:
        """基于检索到的上下文生成答案"""
        if not context:
            return "Sorry, I couldn't find any relevant information."

        # 构建上下文提示
        context_str = "\n\n".join([
            f"### Info {idx + 1} (source: app.leg.wa.gov)\n"
            f"title: {raw[3]}"
            f"summary: {raw[2][:500]}...\n"
            f"url: {raw[1]}"
            for idx, raw in enumerate(context)
        ])

        prompt = f"""
        You are a knowledge Q&A assistant, please answer questions based on the information retrieved below.
        Answer requirements:
         1. Accurately and concisely answer users' questions
         2. Include the source link of relevant information in the answer, in the format of: [Document Source] (URL)
         4. Present links in Markdown format
         5. Ensure that the link points to the original data source
        Information retrieved:
        {context_str}

        question：{question}
        """

        try:
            response = self._client.chat.completions.create(
                model=CHAT_MODEL,
                store=True,
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )
            answer = response.choices[0].message.content
            return answer
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "Error generating answer, please try again later."


if __name__ == '__main__':
    rag = RAGGenerator()
    #  测试RAG生成答案
    content = [(16, 'http://app.leg.wa.gov/RCW/default.aspx?cite=1.08.013', 'PDF,RCW  ,1.04.030,New laws to be added to code.,All laws of a general and permanent nature enacted after January 1, 1949, shall, from time to time, be incorporated into and become a part of said code.,[ ,1950 ex.s. c 16 s 3,.]')]
    answser = rag.generate_answer('What was the supplement to the 1950 Washington State Revised Code?', content)
    print(answser)
    # 测试文本转向量
    # vector = rag.generate_embeddings("What was the supplement to the 1950 Washington State Revised Code?")
    # print(vector)