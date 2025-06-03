"""
cwa_server.py

This module sets up a FastMCP server to deliver weather forecasts using the Central Weather Administration (CWA) Open Data API.
Users can query the server to obtain weather forecasts, with the option to filter results by specific location names.

Weather data is retrieved from the CWA Open Data API.
For more information on the API, visit: https://opendata.cwa.gov.tw/dist/opendata-swagger.html
"""

import os
import requests
from fastmcp import FastMCP

# Initialize the FastMCP server with a descriptive name
mcp = FastMCP(name="Taiwan Weather Checker")


@mcp.tool()
def get_weather_forecast(locationName: str = None) -> dict:
    """
    Fetches a 36-hour weather forecast from the Central Weather Administration (CWA) Open Data API.

    Parameters:
    - locationName (str, optional): The name of the city or county to filter the weather forecast.
      If not provided, the forecast for all available locations will be returned.

    Returns:
    - dict: A dictionary containing the weather forecast data.

    Raises:
    - HTTPError: If the HTTP request to the CWA API fails.
    """
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {}
    api_key = os.getenv("CWA_API_KEY")
    if api_key:
        params["Authorization"] = api_key
    if locationName:
        params["locationName"] = locationName
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Run the FastMCP server using Server-Sent Events (SSE) on port 8000
    mcp.run(transport="sse", port=8000)
