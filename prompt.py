import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

def get_response(sentense):
    api_key = os.getenv("OPENAI_API_KEY")

    bot = OpenAI(api_key=api_key)
    content="rc의 명령어로는 GO, BACK, LEFT, RIGHT, STOP이 있어. 도형을 그려달라는 명령이 들어오면 해당 도형을 명령어를 사용해서 rc카로 그려줘. 명령어들을 \"GO\", \"BACK\", \"LEFT\"와 같은 형태로 명령어들의 모음을 만들어줘.  응답은 다른말 다 필요없고 명령어들만 보내줘"
    response = bot.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": content},
            {"role":"user", "content" : sentense}
        ],
        #max_tokens 1~16383
        max_tokens=256,
        #temperature 0 ~ 2
        temperature=1,
        #top_p 0 ~ 1
        top_p=1.0,
        #frequency_penalty 0 ~ 2
        frequency_penalty=0,
        #presence_penalty 0 ~ 2
        presence_penalty=0
    )

    return response.choices[0].message.content

def main():
    sentense = input("Input Country >> ")
    print( get_response(sentense) )

if __name__ == "__main__":
    main()