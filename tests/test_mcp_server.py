"""
Test module for MCP server functionality.

This module contains tests for the MCP server endpoints and data fetching capabilities.
"""

from unittest.mock import Mock, patch

import pytest

from car_mcp.mcp.server import fetch_data
from car_mcp.models.car import Car


@pytest.fixture
def sample_car():
    """Fixture that returns a sample Car object for testing."""
    return Car(
        brand="Toyota",
        model="Corolla",
        year=2022,
        motorization=2.0,
        fuel="Flex",
        color="Preto",
        mileage=0,
        doors=4,
        transmission="Automática",
        price="120000.00",
        air_conditioning=True,
        electric_steering=True,
        status="Novo",
    )


@pytest.mark.asyncio
async def test_fetch_data_with_empty_filters():
    """Test fetch_data function with empty filters."""
    with patch("car_mcp.mcp.server.DatabaseManager") as mock_db:
        mock_instance = Mock()
        mock_db.return_value = mock_instance
        mock_instance.search.return_value = []

        result = await fetch_data({})

        assert result == {"cars": []}
        mock_instance.search.assert_called_once_with({})


@pytest.mark.asyncio
async def test_fetch_data_with_filters(sample_car):
    """Test fetch_data function with specific filters."""
    test_filters = {"brand": "Toyota", "year_min": 2022}

    with patch("car_mcp.mcp.server.DatabaseManager") as mock_db:
        mock_instance = Mock()
        mock_db.return_value = mock_instance
        mock_instance.search.return_value = [sample_car]

        result = await fetch_data(test_filters)

        assert result == {"cars": [sample_car.to_dict()]}
        mock_instance.search.assert_called_once_with(test_filters)


@pytest.mark.asyncio
async def test_fetch_data_with_none_filters():
    """Test fetch_data function with None filters."""
    with patch("car_mcp.mcp.server.DatabaseManager") as mock_db:
        mock_instance = Mock()
        mock_db.return_value = mock_instance
        mock_instance.search.return_value = []

        result = await fetch_data(None)

        assert result == {"cars": []}
        mock_instance.search.assert_called_once_with({})
