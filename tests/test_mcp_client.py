"""
Test module for MCP client functionality.

This module contains tests for the MCPClient class, focusing on the process_query method
and its interaction with the MCP server.
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from car_mcp.mcp.client import MCPClient
from car_mcp.models.car import Car


@pytest.fixture
def sample_car_dict():
    """Fixture that returns a sample car dictionary for testing."""
    return {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "motorization": 2.0,
        "fuel": "Flex",
        "color": "Preto",
        "mileage": 0,
        "doors": 4,
        "transmission": "Automática",
        "price": "120000.00",
        "air_conditioning": True,
        "electric_steering": True,
        "status": "Novo"
    }


@pytest.fixture
def mock_response():
    """Fixture that creates a mock response object."""
    mock = MagicMock()
    mock.content = [MagicMock()]
    return mock


@pytest.mark.asyncio
async def test_process_query_with_results(sample_car_dict, mock_response):
    """Test process_query when results are found."""
    # Prepare mock response
    mock_response.content[0].text = json.dumps({"cars": [sample_car_dict]})

    # Create mock session
    mock_session = AsyncMock()
    mock_session.initialize = AsyncMock()
    mock_session.call_tool = AsyncMock(return_value=mock_response)

    # Create mock context managers
    mock_sse = AsyncMock()
    mock_sse.__aenter__.return_value = ["stream"]
    mock_client_session = AsyncMock()
    mock_client_session.__aenter__.return_value = mock_session

    with patch('car_mcp.mcp.client.sse_client', return_value=mock_sse), \
         patch('car_mcp.mcp.client.ClientSession', return_value=mock_client_session):
        
        client = MCPClient()
        result = await client.process_query({"brand": "Toyota"})

        assert len(result) == 1
        assert isinstance(result[0], Car)
        assert result[0].brand == "Toyota"
        assert result[0].model == "Corolla"


@pytest.mark.asyncio
async def test_process_query_no_results(mock_response):
    """Test process_query when no results are found."""
    # Prepare mock response
    mock_response.content[0].text = json.dumps({"cars": []})

    # Create mock session
    mock_session = AsyncMock()
    mock_session.initialize = AsyncMock()
    mock_session.call_tool = AsyncMock(return_value=mock_response)

    # Create mock context managers
    mock_sse = AsyncMock()
    mock_sse.__aenter__.return_value = ["stream"]
    mock_client_session = AsyncMock()
    mock_client_session.__aenter__.return_value = mock_session

    with patch('car_mcp.mcp.client.sse_client', return_value=mock_sse), \
         patch('car_mcp.mcp.client.ClientSession', return_value=mock_client_session):
        
        client = MCPClient()
        result = await client.process_query({})

        assert len(result) == 0


@pytest.mark.asyncio
async def test_process_query_invalid_response(mock_response):
    """Test process_query with invalid response format."""
    # Prepare mock response with invalid format
    mock_response.content[0].text = json.dumps({"invalid": "response"})

    # Create mock session
    mock_session = AsyncMock()
    mock_session.initialize = AsyncMock()
    mock_session.call_tool = AsyncMock(return_value=mock_response)

    # Create mock context managers
    mock_sse = AsyncMock()
    mock_sse.__aenter__.return_value = ["stream"]
    mock_client_session = AsyncMock()
    mock_client_session.__aenter__.return_value = mock_session

    with patch('car_mcp.mcp.client.sse_client', return_value=mock_sse), \
         patch('car_mcp.mcp.client.ClientSession', return_value=mock_client_session):
        
        client = MCPClient()
        result = await client.process_query({})

        assert len(result) == 0