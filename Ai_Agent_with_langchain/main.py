from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
import os
import requests




load_dotenv()
###intilize Gemini flash 2.5


def get_weather(city: str):
  """ Get weather for a given city """
  api_key = os.getenv("OPENWEATHER_API_KEY")
  base_url = "http://api.openweathermap.org/data/2.5/weather"
  params = {
    "q":city,
    "appid": api_key,
    'units': 'metric'
  }
  response = requests.get(base_url,params=params)
  data = response.json()
  return data
  

def get_location():
  """ Get user's  current location , use this when  user asks about weather without asking about the city """
  ###base_url = "https://ipapi.co/json"
  response = requests.get("https://ipapi.co/json", headers={"User-agent": "your-bot 0.1"})
  data = response.json()
  city = data.get('city')
  country_name = data.get('country_name')
  ##country = data.get('country_name')
  return f"{city}, {country_name}"
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
3- use your knowledge to determine which temperature unit is standard for the given location 

"""
## The Agent = llm + toold
agent = create_agent(
    model=llm,
    tools=[get_weather, get_location],
    system_prompt=system_prompt

)
if __name__ == "__main__":

        user_query = input("Enter your query:")
        ## ask the questision 
        response = agent.invoke(
            {"messages": [{'role': 'user',
                            'content': user_query}]})

        print(response["messages"][-1].text)