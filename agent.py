import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI
import requests
import re
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"Weather in {city} is {response.text}"
    return "Something Went Wrong!"

available_tools = {
    "get_weather": get_weather
}

SYSTEM_PROMPT = """
You are a helpful weather assistant.

You can answer questions about current weather conditions.
When the user asks about weather in a city, use the available tool.
For every tool call wait for the OBSERVE step to get the output of the tool and then plan your next step accordingly.

Rules:
- Use the weather tool whenever weather data is needed.
- Do not guess weather information.
- Strictly follow the given JSON output format.
- Only run one step at a time.
- The sequence of steps is START(Where user gives an input) -> PLAN(This step can be repeated multiple times) -> TOOL(Use available tools) -> OUTPUT(Result given to the user)
- CRITICAL: Provide ONLY ONE JSON object per response. Do not provide multiple steps at once. 
- After every TOOL call, stop and wait for the OBSERVE data.

OUTPUT JSON FORMAT:
{"step":"START/PLAN/TOOL/OBSERVE/OUTPUT","content":"content to be shown to user or tool input or tool output it is generally string","tool":"tool name if step is TOOL or OBSERVE","input":"tool input if step is TOOL","output":"tool output if step is OBSERVE"}

Available tool:
    get_weather - Takes city name as input string and return the weather information about the city


Example1 :
START: What is the weather of delhi?
PLAN: {"step":"PLAN":"content":"Seems like the user is interested in getting the weather of delhi in india"}
PLAN: {"step":"PLAN":"content":"Lets see if I have any available tools to fullfil the user request"}
PLAN: {"step":"PLAN":"content":"Great! I have get_weather tool available for this query"}
PLAN: {"step":"TOOL":"tool":"get_weather","input":"delhi"}
PLAN: {"step":"OBSERVE":"tool":"get_weather","output":"Weather in delhi is Sunny +30°C"}
PLAN: {"step":"PLAN":"content":"Great! I have got the weather information for delhi using get_weather tool"}
OUTPUT: {"step":"OUTPUT","content":"Weather in delhi is Sunny and the temperature is 30 degree celsius."}

Example2 :
START: What is the weather of delhi and mumbai?
PLAN: {"step":"PLAN":"content":"Seems like the user is interested in getting the weather of delhi and mumbai in india"}
PLAN: {"step":"PLAN":"content":"Lets see if I have any available tools to fullfil the user request"}
PLAN: {"step":"PLAN":"content":"Great! I have get_weather tool available for this query"}
PLAN: {"step":"TOOL":"tool":"get_weather","input":"delhi"}
PLAN: {"step":"OBSERVE":"tool":"get_weather","output":"Weather in delhi is Sunny +30°C"}
PLAN: {"step":"PLAN":"content":"Great! I have got the weather information for delhi using get_weather tool. Lets get the weather information for mumbai now"}
PLAN: {"step":"TOOL":"tool":"get_weather","input":"mumbai"}
PLAN: {"step":"OBSERVE":"tool":"get_weather","output":"Weather in mumbai is Rainy +25°C"}
PLAN: {"step":"PLAN":"content":"Great! I have got the weather information for mumbai using get_weather tool"}
OUTPUT: {"step":"OUTPUT","content":"Weather in delhi is Sunny and the temperature is 30 degree celsius. Weather in mumbai is Rainy and the temperature is 25 degree celsius."}
"""

message_history = [
    {
        "role":"system",
        "content": SYSTEM_PROMPT
    }
]

user_query = input("> ")
message_history.append({
    "role":"user",
    "content": user_query
})
while True:
    try:
        response = client.chat.completions.create(
           model="gemini-2.5-flash",
           messages=message_history
        )
        raw_result = response.choices[0].message.content
        if not raw_result: continue

        message_history.append({"role": "assistant", "content": raw_result})

        json_match = re.search(r'\{.*\}', raw_result, re.DOTALL)
        if not json_match:
            print(f"🤖: {raw_result}")
            continue
            
        parsed_result = json.loads(json_match.group())
        step = parsed_result.get("step")

        if step in ["START", "PLAN"]:
            print("🤖: " + parsed_result.get("content"))
            continue

        if step == "TOOL":
            tool_name = parsed_result.get("tool")
            tool_input = parsed_result.get("input")
            print(f"🔧 Calling {tool_name} for {tool_input}...")
            
            tool_response = available_tools[tool_name](tool_input)
            
            message_history.append({
                "role": "user", 
                "content": f"OBSERVE: {json.dumps({'step':'OBSERVE', 'tool': tool_name, 'output': tool_response})}"
            })
            continue

        if step == "OUTPUT":
            print("🤖: " + parsed_result.get("content"))
            break

    except Exception as e:
        if "429" in str(e):
            print("⏳ Rate limit reached. Waiting 10 seconds before retrying...")
            time.sleep(10)
            continue
        print(f"⚠️ An error occurred: {e}")
        break