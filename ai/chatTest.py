from openai import OpenAI

from ai.tokenLoader import TokenLoader


def run_test():
    token = TokenLoader().load("secrets\\API_KEY.txt")

    client = OpenAI(
        # This is the default and can be omitted
        api_key=token,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a JML (Java Modeling Language) expert. I will give you a JavaDoc comment and you will generate the JML specification for the method.",
            },
            {
                "role": "user",
                "content": "Generate JML from the following JavaDoc comment: /**\n * Multiplies two numbers\n */ Do not write any text only the JML. Surround the JML with /** and */.",
            }
        ],
        model="gpt-3.5-turbo",
    )

    print(chat_completion.choices[0].message.content)

#"Generate JML from the following JavaDoc comment: /**\n * Multiplies two numbers\n */"