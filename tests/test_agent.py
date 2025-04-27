"""
Test module for Virtual Agent functionality.

This module contains tests for the VirtualAgent class, focusing on the conversation
flow and car search functionality.
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from car_mcp.agent.agent import VirtualAgent
from car_mcp.models.car import Car


@pytest.fixture
def virtual_agent():
    """Fixture that returns a VirtualAgent instance with mocked client."""
    with patch("car_mcp.agent.agent.MCPClient") as mock_client:
        agent = VirtualAgent()
        agent.client.process_query = AsyncMock()
        return agent


@pytest.fixture
def sample_car():
    """Fixture that returns a sample Car object."""
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
        price=120000.00,
        air_conditioning=True,
        electric_steering=True,
        status="Novo",
    )


@pytest.mark.asyncio
async def test_start_loop_complete_search(virtual_agent, sample_car):
    mock_response = {
        "new_filters": {
            "brand": "Toyota",
            "model": "Corolla",
            "year_min": 2020,
            "price_max": 150000,
        },
        "need_more_info": False,
        "next_question": False,
    }

    inputs = ["Quero um Toyota Corolla a partir de 2020 até 150 mil reais", "sair"]
    input_mock = MagicMock(side_effect=inputs)

    with patch("builtins.input", input_mock), patch(
        "builtins.print"
    ) as print_mock, patch("car_mcp.agent.agent.llm"), patch("car_mcp.agent.agent.StrOutputParser") as parser_mock:

        parser_mock.return_value = MagicMock(return_value=json.dumps(mock_response))

        virtual_agent.client.process_query.return_value = [sample_car]

        await virtual_agent.start_loop()

        virtual_agent.client.process_query.assert_called_once()
        assert input_mock.call_count == 2
        assert print_mock.call_count > 0


@pytest.mark.asyncio
async def test_start_loop_incomplete_search(virtual_agent):
    """Test start_loop with an incomplete car search that needs more information."""
    mock_response = {
        "new_filters": {"brand": "Toyota"},
        "need_more_info": True,
        "next_question": "Qual modelo de Toyota você está procurando?",
    }

    # Mock user inputs
    inputs = ["Quero um Toyota", "sair"]
    input_mock = MagicMock(side_effect=inputs)

    with patch("builtins.input", input_mock), patch(
        "builtins.print"
    ) as print_mock, patch("car_mcp.agent.agent.llm"), patch("car_mcp.agent.agent.StrOutputParser") as parser_mock:

        # Setup LLM mock
        parser_mock.return_value = MagicMock(return_value=json.dumps(mock_response))

        # Run the conversation loop
        await virtual_agent.start_loop()

        # Verify interactions
        virtual_agent.client.process_query.assert_not_called()
        assert input_mock.call_count == 2
        assert print_mock.call_count > 0


@pytest.mark.asyncio
async def test_start_loop_no_results(virtual_agent):
    """Test start_loop when no cars match the search criteria."""
    mock_response = {
        "new_filters": {
            "brand": "Toyota",
            "model": "Corolla",
        },
        "need_more_info": False,
        "next_question": False,
    }

    inputs = ["Quero um Toyota Corolla", "sair"]
    input_mock = MagicMock(side_effect=inputs)

    with patch("builtins.input", input_mock), patch(
        "builtins.print"
    ) as print_mock, patch("car_mcp.agent.agent.llm"), patch("car_mcp.agent.agent.StrOutputParser") as parser_mock:

        parser_mock.return_value = MagicMock(return_value=json.dumps(mock_response))

        virtual_agent.client.process_query.return_value = []

        await virtual_agent.start_loop()

        virtual_agent.client.process_query.assert_called_once()
        assert input_mock.call_count == 2
        assert print_mock.call_count > 0
