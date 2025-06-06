"""
serpapi_flights_server.py

This module sets up a FastMCP server to search for flight information using the SerpAPI Google Flights API.
Users can query the server to obtain flight information, including prices, schedules, and available routes.

Flight data is retrieved from the SerpAPI Google Flights API.
For more information on the API, visit: https://serpapi.com/google-flights-api
"""

import os
import requests
import json
from typing import Any, Dict, Optional, List
from fastmcp import FastMCP

# Initialize the FastMCP server with a descriptive name
mcp = FastMCP(name="Flight Search Assistant")


def _add_param(params: Dict[str, Any], key: str, value: Any) -> None:
    if value is not None and value != "":
        params[key] = value


def _validate_max_price(max_price: Any) -> Optional[int]:
    if max_price is None:
        return None
    try:
        max_price_int = int(max_price)
    except (TypeError, ValueError):
        raise ValueError("`max_price` must be a positive integer if provided.")
    if max_price_int <= 0:
        raise ValueError("`max_price` must be a positive integer if provided.")
    return max_price_int


def _validate_multicity_segments(multi_city_json: str) -> List[dict]:
    try:
        segments = json.loads(multi_city_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"`multi_city_json` must be a valid JSON string: {e}")
    if not isinstance(segments, list):
        raise ValueError("`multi_city_json` must be a JSON array of flight segments.")
    for i, seg in enumerate(segments):
        if not isinstance(seg, dict):
            raise ValueError(f"Segment #{i+1} in `multi_city_json` must be an object.")
        # If departure_id is missing, inherit from previous segment's arrival_id (if any)
        if "departure_id" not in seg or not seg.get("departure_id"):
            if i == 0:
                raise ValueError(
                    f"Missing `departure_id` in first segment of `multi_city_json`."
                )
            prev_arrival = segments[i - 1].get("arrival_id")
            if not prev_arrival:
                raise ValueError(
                    f"Cannot infer `departure_id` for segment #{i+1}; previous segment has no `arrival_id`."
                )
            seg["departure_id"] = prev_arrival
        if "arrival_id" not in seg or not seg.get("arrival_id"):
            raise ValueError(
                f"Missing `arrival_id` in `multi_city_json` parameter (flight #{i+1})."
            )
        if "date" not in seg or not seg.get("date"):
            raise ValueError(
                f"Missing `date` in `multi_city_json` parameter (flight #{i+1})."
            )
    return segments


@mcp.tool()
def search_flights(
    origin: str = None,
    destination: str = None,
    departure_date: str = None,
    return_date: str = None,
    trip_type: str = "oneway",  # 'oneway', 'roundtrip', or 'multicity'
    multi_city_json: str = None,
    gl: str = None,
    hl: str = None,
    currency: str = "TWD",
    adults: int = 1,
    children: int = 0,
    infants_in_seat: int = 0,
    infants_on_lap: int = 0,
    travel_class: int = 1,
    show_hidden: bool = False,
    deep_search: bool = False,
    sort_by: int = 1,
    stops: int = 0,
    exclude_airlines: str = None,
    include_airlines: str = None,
    bags: int = 0,
    outbound_times: str = None,
    return_times: str = None,
    layover_duration: str = None,
    exclude_conns: str = None,
    departure_token: str = None,
    booking_token: str = None,
    no_cache: bool = False,
    async_req: bool = False,
    zero_trace: bool = False,
    output: str = "json",
) -> dict:
    """
    Searches for flights using the SerpAPI Google Flights API.

    Parameters:
    - origin (str): The origin airport code(s) or kgmid(s) (e.g., "JFK", "LAX", "/m/0vzm")
    - destination (str): The destination airport code(s) or kgmid(s)
    - departure_date (str): The departure date in YYYY-MM-DD format
    - return_date (str, optional): The return date in YYYY-MM-DD format for round trips
    - trip_type (str, optional): 'oneway', 'roundtrip', or 'multicity' (default: 'oneway')
    - multi_city_json (str, optional): JSON string for multi-city flights
    - gl (str, optional): Country code for localization
    - hl (str, optional): Language code for localization
    - currency (str, optional): Currency code for prices (default: "TWD")
    - adults (int, optional): Number of adult passengers (default: 1)
    - children (int, optional): Number of child passengers (default: 0)
    - infants_in_seat (int, optional): Number of infants in seat (default: 0)
    - infants_on_lap (int, optional): Number of infants on lap (default: 0)
    - travel_class (int, optional): 1=Economy, 2=Premium economy, 3=Business, 4=First (default: 1)
    - show_hidden (bool, optional): Include hidden results (default: False)
    - deep_search (bool, optional): Enable deep search (default: False)
    - sort_by (int, optional): 1=Top, 2=Price, 3=Departure, 4=Arrival, 5=Duration, 6=Emissions (default: 1)
    - stops (int, optional): 0=Any, 1=Nonstop, 2=1 stop, 3=2 stops (default: 0)
    - exclude_airlines (str, optional): Comma-separated airline codes/alliances to exclude
    - include_airlines (str, optional): Comma-separated airline codes/alliances to include
    - bags (int, optional): Number of carry-on bags (default: 0)
    - outbound_times (str, optional): Outbound time range (e.g., "4,18,3,19")
    - return_times (str, optional): Return time range (for round trip)
    - layover_duration (str, optional): Min,max layover duration in minutes (e.g., "90,330")
    - exclude_conns (str, optional): Comma-separated connecting airport codes to exclude
    - departure_token (str, optional): For returning flights or next leg
    - booking_token (str, optional): For booking options
    - no_cache (bool, optional): Force no cache (default: False)
    - async_req (bool, optional): Async request (default: False)
    - zero_trace (bool, optional): ZeroTrace mode (default: False)
    - output (str, optional): 'json' (default) or 'html'

    Returns:
    - dict: A dictionary containing the flight search results.

    Raises:
    - HTTPError: If the HTTP request to the SerpAPI fails.
    - ValueError: If required parameters are missing or invalid.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Environment variable SERPAPI_API_KEY is not set. Please set it to access the SerpAPI."
        )
    url = "https://serpapi.com/search"

    # Map trip_type to type param and validate trip-specific fields
    if trip_type == "roundtrip":
        if not return_date:
            raise ValueError("`return_date` is required if `trip_type` is 'roundtrip'.")
        type_param = 1
    elif trip_type == "multicity":
        if not multi_city_json:
            raise ValueError(
                "`multi_city_json` is required if `trip_type` is 'multicity'."
            )
        _validate_multicity_segments(multi_city_json)
        type_param = 3
    else:
        type_param = 2  # oneway

    params = {
        "engine": "google_flights",
        "api_key": api_key,
        "type": type_param,
        "travel_class": travel_class,
        "show_hidden": str(show_hidden).lower(),
        "deep_search": str(deep_search).lower(),
        "sort_by": sort_by,
        "stops": stops,
        "bags": bags,
        "adults": adults,
        "children": children,
        "infants_in_seat": infants_in_seat,
        "infants_on_lap": infants_on_lap,
        "currency": currency,
        "output": output,
        "no_cache": str(no_cache).lower(),
        "async": str(async_req).lower(),
        "zero_trace": str(zero_trace).lower(),
    }

    if trip_type != "multicity":
        _add_param(params, "departure_id", origin)
        _add_param(params, "arrival_id", destination)
        _add_param(params, "outbound_date", departure_date)
        if return_date and trip_type == "roundtrip":
            _add_param(params, "return_date", return_date)
    if multi_city_json and trip_type == "multicity":
        _add_param(params, "multi_city_json", multi_city_json)
    _add_param(params, "gl", gl)
    _add_param(params, "hl", hl)
    _add_param(params, "exclude_airlines", exclude_airlines)
    _add_param(params, "include_airlines", include_airlines)
    _add_param(params, "outbound_times", outbound_times)
    _add_param(params, "return_times", return_times)
    _add_param(params, "layover_duration", layover_duration)
    _add_param(params, "exclude_conns", exclude_conns)
    _add_param(params, "departure_token", departure_token)
    _add_param(params, "booking_token", booking_token)

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Run the FastMCP server using Server-Sent Events (SSE)
    # Allow overriding the port via environment variable
    port = int(os.getenv("FLIGHTS_SERVER_PORT", "8001"))
    mcp.run(transport="sse", port=port)
