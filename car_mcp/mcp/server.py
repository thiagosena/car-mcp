"""
MCP (Model-Client-Protocol) server implementation for car search system.

This module provides a FastMCP server that handles car data requests using
Server-Sent Events (SSE). It exposes an endpoint for fetching car data based
on specified filters.

Dependencies:
    - db_manager: For database operations
    - mcp.server.fastmcp: For FastMCP server implementation
"""

from mcp.server.fastmcp import FastMCP

from car_mcp.database.db_manager import DatabaseManager

mcp = FastMCP("car")


@mcp.tool("fetch_data")
async def fetch_data(filters: dict):
    """
    Fetch car data from the database based on provided filters.

    This function is registered as an MCP tool and handles database queries
    for car information. It converts the retrieved Car objects to dictionaries
    for JSON serialization.

    Args:
        filters (dict): Search criteria for filtering cars. Can include various
                       car attributes such as brand, model, year, etc.

    Returns:
        dict: A dictionary containing a list of car dictionaries under the 'cars' key.
              Example: {'cars': [{'brand': 'Toyota', 'model': 'Corolla', ...}, ...]}
    """
    db_manager = DatabaseManager()
    cars = db_manager.search(filters or {})

    return {"cars": [car.to_dict() for car in cars]}


if __name__ == "__main__":
    mcp.run(transport="sse")
