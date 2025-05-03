from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import requests

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


client = OpenAI(
    api_key= api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_weather(city : str) :
    # TODO: Perform an actual API call
    print("🔨 Tool Called: get_weather", city)

    url = f"https://wttr.in/{city}?format=%C+%t"

    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"

    return "Something went wrong"

available_tools = {
    
        "get_weather":
        {
            # don't give it as string get_weather as we will be calling this
            "fn" : get_weather,  
            "description" : "this function takes city name as input and return the real time weather of the city"
        }
    
}
system_prompt = """


You are a helpful AI Assistant who is specialized in resolving user's query.
You work on start, plam, action, observe mode.

For the given user query and given available tools , plan step by step execution
Based on planning , chose the relevent tool from available tool
Based on tool selection, u perform an action
Wait for observation and based on observation from the tool query resolve the query

Rules:
Follow the JSON Format for output
Execute one step at a time and wait for next input and then execute the nezt step
Carefully analyze the query

Output JSON Format 
{{
 "step" : "string",
 "content" : "string",
 "function" : " The name of the function if step is action"
 "input" :"string"

}}



Example 
user query : What is weather of New York?
Output : {{ "step" : "plan" , " content " : " user is interested in weather data of New York"}}
Output : {{ "step" : "plan" , " content " : " from the available tools , call get_weather function"}}
Output : {{ "step" : "action" , " function " : "get_weather function" , "input": "New York"}}
Output : {{ "step" : "observe" , "content" : "the output weather returned by get weather is 31 degree celsius"}}
Output : {{ "step" : "output" , "content" : "Weather of New York is 31 degree celsius"}}


"""

messages = [
    {
        "role" : "system" , "content" : system_prompt
    }
]
while True:
        query = input(">> ")
        messages.append(
            {"role": "user" , "content" : query}
        )

        while True :

            result = client.chat.completions.create(

                model = "gemini-2.0-flash",
                response_format =  {"type":"json_object"},
                messages = messages
            )
            parsed_response = json.loads(result.choices[0].message.content)
            messages.append({
                "role" : "assistant",
                "content" : json.dumps(parsed_response)
            })

            if parsed_response.get("step") == "action":
                tool_name = parsed_response.get("function")
                tool_input = parsed_response.get("input")
                if available_tools.get(tool_name) :
                    output = available_tools[tool_name].get("fn")(tool_input)
                    messages.append(
                        {
                            "role" : "assistant",
                            "content" : json.dumps (
                                {"step" : "output",
                                "content": output
                                }

                            )

                        }
                    )
                print("🧠",parsed_response.get("content"))
                continue

            elif parsed_response.get("step") != "output":
                print(parsed_response)
                continue
        
            else:
                print("🤖",parsed_response.get("content"))
                break


