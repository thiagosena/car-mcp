"""
MCP (Model-Client-Protocol) client implementation for car search system.

This module provides a client interface for communicating with the MCP server
using Server-Sent Events (SSE). It handles data fetching and car object
conversion for the automobile search system.

Dependencies:
    - json: For JSON data handling
    - car: For Car model class
    - mcp: For ClientSession implementation
    - mcp.client.sse: For SSE client functionality
"""

import json

from mcp import ClientSession
from mcp.client.sse import sse_client

from car_mcp import config
from car_mcp.models.car import Car


class MCPClient:
    """
    Client class for handling MCP protocol communications.
    
    This class manages the connection to the MCP server and processes
    queries for car data using Server-Sent Events.
    """

    async def process_query(self, query):
        """
        Process a car search query through the MCP server.

        Args:
            query (dict): Search filters for querying car data.
                         The filters can include a lot car attributes
                         such as brand, model, year, etc.

        Returns:
            list[Car]: A list of Car objects matching the query criteria.
                      Returns an empty list if no matches are found or
                      if there's an error in the response.
        """
        async with sse_client(url=config.MCP_SERVER_URL) as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()

                response = await session.call_tool(
                    "fetch_data", arguments={"filters": query}
                )

                data = json.loads(response.content[0].text)

                if data and "cars" in data:
                    return [Car.from_dict(car) for car in data["cars"]]

                return []
