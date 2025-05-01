import json
from openai import OpenAI
import os

# api_key = os.getenv('GEMINI_API_KEY')
api_key = "AIzaSyCnqvJEs73BV1HJ3RWWsOXwRFfe4_ja_zo"
print(api_key)

client = OpenAI(
  api_key = api_key,
  base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

query = input(">> ")

system_prompt = """

You are an AI Assistant who solves the query by breaking it down into multiple steps and then come up with the answer

If user gives any query , break down the complex query into multiple smaller steps. These steps involve analyze , think , think again , output , validate the output.

Rule:
the output should be in Json Format. Strictly follow the format
Always perform one step at a time and wait for next intput
carefully analyze the query

1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next input
3. Carefully analyse the user query

output format:
{{"step" : "", "content" :""}}

Example:

Input : what is 5*200
Output : {{"step" : "analyze", "content" : "user wants the computation result of 5 * 200"}}
Output :{{ "step": "think" ,  "content": "since the operator is mutiply , we need to perform multiplication between two operands"
}}
Output :{{  "step": "think", "content" : " operation should be performed left to right"}}
Output :{{   "step" : "output", "content": " 5 multiplied by 200 gives result as 1000"}}
Output :{{    "step" : "validate", "content": "1000 seems correct"}}

"""
response = client.chat.completions.create(
    model = "gemini-2.0-flash",
    response_format={"type": "json_object"},
    messages = [
        {"role": "system", "content": system_prompt},
        {"role" : "user", "content": query},
        {"role": "assistant", "content": json.dumps( {
"step": "analyze",
"content": "The user is asking for a definition or explanation of 'love'."
})},
{"role": "assistant", "content": json.dumps({
"step": "think",
"content": "Love is a complex concept with philosophical, religious, and personal interpretations. I need to formulate a general and comprehensive definition."
})},
{"role": "assistant", "content": json.dumps({
  "step": "output",
  "content": "Love is a profound and multifaceted emotion characterized by strong affection, care, and attachment towards another person or thing. It encompasses a wide range of feelings, from passionate desire to deep commitment and nurturing compassion. Love can be expressed through various actions, words, and gestures, and it often involves a sense of empathy, understanding, and acceptance."
})}

    ]
)

print(response.choices[0].message.content)        