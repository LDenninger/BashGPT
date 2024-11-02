import datetime
import requests
import os

import arxiv
import webbrowser

from .FunctionTemplate import FunctionTemplate


class OpenArxivArticle(FunctionTemplate):
    def __init__(self):
        super().__init__(
            name="OpenArxivArticle",
            description="Fetches an article from the Arxiv API.",
            parameters={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the article you want to retrieve.",
                    },
                },
                "required": ["title"],
                "additionalProperties": False,
            }
        )

        if "OPENAI_API_KEY" not in os.environ:
            print("OPENAI_API_KEY not set in environment. Please set it before running BashGPT.")
            self.api_key = None
            
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.num_results = 5

    def __call__(self, title):
        # Search for the paper by title
        search = arxiv.Search(
            query=title,
            max_results=self.num_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        paper_number = 0
        results = list(search)
        import ipdb; ipdb.set_trace()
        num_results = len(results)
        if num_results > 1:
            print(f"Found {num_results} papers matching '{title}'.")
            for i, result in enumerate(search.results(), start=1):
                print(f"{i}: {result.title}")

            number = input("Enter number of paper to open (or '0' to exit): ")
            if number.isdigit() and int(number) <= num_results:
                paper_number = int(number) - 1
            else:
                print("Invalid input. Exiting.")
                return None
        import ipdb; ipdb.set_trace()
        paper = results[paper_number]
        
        paper_url = paper.pdf_url
        print(f"Opening paper: {result.title}")
        print(f"URL: {paper_url}")
        
        # Open the PDF in the default web browser
        webbrowser.open(paper_url)
            
        return None
        



class WeatherFunction(FunctionTemplate):

    def __init__(self):
        super().__init__(
            name="WeatherFunction",
            description="Fetches weather data for a given location and time. It requires an API key from OpenWeatherMap.",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location the user wants to retrieve the weather data for in latitude and longitude coordinates. If no information provided, use the location of the OpenAI headquarters.",
                    },
                    "date": {
                        "type": "string",
                        "description": "The date the user wants to retrieve the weather data for in format: 'YYYY-MM-DD'. If none provided use the current date.",
                    },
                },
                "required": ["order_id"],
                "additionalProperties": False,
            }
        )

        if "OPENWEATHERMAP_API_KEY" not in os.environ:
            print("OPENWEATHERMAP_API_KEY not set in environment. Please set it before running BashGPT.")
            self.api_key = None
            
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    def __call__(self, location, date):
        """
        Retrieve weather information for a specific date.

        :param api_key: Your OpenWeatherMap API key.
        :param location: The location for which to retrieve weather data (e.g., "London,UK").
        :param date: The date for which to retrieve weather data (format: "YYYY-MM-DD").
        :return: Weather information for the specified date.
        """
        if self.api_key is None:
            return "OpenWeatherMap API key not set"
        # Convert the date to a Unix timestamp
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        timestamp = int(date_obj.timestamp())
        
        # Make a request to the OpenWeatherMap API
        url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine"
        params = {
            'lat': location['lat'],
            'lon': location['lon'],
            'dt': timestamp,
            'appid': self.api_key,
            'units': 'metric'  # Use 'imperial' for Fahrenheit
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Unable to retrieve weather data"}
        
    
    def to_prompt(self, response:str):
        """
        Generate a prompt for the user to provide the location and date for the weather function.

        :param response: The weather data as a JSON string.
        :return: Prompt for the user to provide location and date.
        """
        return "Please formulate a quick weather report given the following weather data:\n {response}."
    



