from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent




load_dotenv()
###intilize Gemini flash 2.5


def get_weather(city: str):
  """ Get aweather for agiven city """
  return "Sunny"  

def get_location():
  """ Get user's  current location , use this when  user asks about weather without asking about the city """
  return "Egypt,Cairo"
##llm

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0.7,
)

system_prompt= """ you are helpful weather assistent 
YOUR WORKFLOW:
1- if user ask about weather WITHOUT specifying a location , you MUST:
   - First call get_location() to find thier location 
   - Then get get_weather(city) with the location
2- if user provides a city , call get_weather(city) directly

"""
## The Agent = llm + toold
agent = create_agent(
    model=llm,
    tools=[get_weather, get_location],
    system_prompt=system_prompt

)
user_query = input("Enter your query:")
## ask the questision 
response = agent.invoke(
    {"messages": [{'role': 'user',
                    'content': user_query}]})

print(response["messages"][-1].content)