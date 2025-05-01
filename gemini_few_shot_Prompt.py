from openai import OpenAI

import os

# api_key = os.getenv('GEMINI_API_KEY')
api_key = "AIzaSyCnqvJEs73BV1HJ3RWWsOXwRFfe4_ja_zo"
print(api_key)

client = OpenAI(
  api_key = api_key,
  base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

system_prompt = """
You are an AI assistant who is expert in Maths.You should not answer any query that is not related to maths.

For given user query , compute the result carefully and give correct answer
Example
1) Input: 30 *4
Output: Here we are mutliplying two numbers 30 and 4 and their result after performing multiplication will be 120

2)
Input: 5+5+5+5+5
Output: Here we are adding 5 5times , so either we can perform addition of 5 , five no of times or we can multiply 5 with no of times the no is added . so our answer will be 5*5 =25

3)
Input: " what is color of my tongue"
Output: " Bruh!! what is wrong with u"

"""
query = input(">> ")
response = client.chat.completions.create(
    model = "gemini-2.0-flash",
    messages = [
        {'role': 'system' , 'content':system_prompt },
        {'role': 'user', 'content': query}
    ]
)
print(response.choices[0].message.content)