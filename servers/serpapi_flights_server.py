"""
serpapi_flights_server.py

This module sets up a FastMCP server to search for flight information using the SerpAPI Google Flights API.
Users can query the server to obtain flight information, including prices, schedules, and available routes.

Flight data is retrieved from the SerpAPI Google Flights API.
For more information on the API, visit: https://serpapi.com/google-flights-api
"""

import os
import requests
from fastmcp import FastMCP

# Initialize the FastMCP server with a descriptive name
mcp = FastMCP(name="Flight Search Assistant")


@mcp.tool()
def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str = None,
    adults: int = 1,
    children: int = 0,
    infants: int = 0,
    currency: str = "TWD",
) -> dict:
    """
    Searches for flights using the SerpAPI Google Flights API.

    Parameters:
    - origin (str): The origin airport code (e.g., "JFK", "LAX")
    - destination (str): The destination airport code (e.g., "SFO", "LHR")
    - departure_date (str): The departure date in YYYY-MM-DD format
    - return_date (str, optional): The return date in YYYY-MM-DD format for round trips
    - adults (int, optional): Number of adult passengers (default: 1)
    - children (int, optional): Number of child passengers (default: 0)
    - infants (int, optional): Number of infant passengers (default: 0)
    - currency (str, optional): Currency code for prices (default: "USD")

    Returns:
    - dict: A dictionary containing the flight search results.

    Raises:
    - HTTPError: If the HTTP request to the SerpAPI fails.
    """
    # Ensure the SerpAPI API key is provided
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise EnvironmentError("Environment variable SERPAPI_API_KEY is not set. Please set it to access the SerpAPI.")
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_flights",
        "api_key": api_key,
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": departure_date,
        "adults": adults,
        "children": children,
        "infants": infants,
        "currency": currency,
    }

    if return_date:
        params["return_date"] = return_date

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Run the FastMCP server using Server-Sent Events (SSE)
    # Allow overriding the port via environment variable
    port = int(os.getenv("FLIGHTS_SERVER_PORT", "8001"))
    mcp.run(transport="sse", port=port)
