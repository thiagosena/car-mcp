"""
Virtual Agent module for car search system.

This module implements a conversational agent that helps users search for cars
by interpreting natural language queries and converting them into structured filters.
The agent uses LLM for understanding user input and interacts with an MCP client
for retrieving car data.

Dependencies:
    - colorama: For terminal color output
    - dotenv: For environment variable management
    - langchain: For LLM prompt handling
    - local_ollama: For LLM implementation
    - mcp_client: For car data retrieval
"""

import asyncio
import json
import re

from colorama import Fore, init
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from car_mcp.agent.local_ollama import llm
from car_mcp.mcp.client import MCPClient

init(autoreset=True)

load_dotenv()


class VirtualAgent:
    """
    A virtual agent for handling car search conversations.

    This class manages the interaction between users and the car search system,
    interpreting natural language queries and presenting results in a user-friendly format.
    """

    def __init__(self):
        self.client = MCPClient()

    async def start_loop(self):
        """
        Start the conversation loop with the user.

        This method handles the main interaction loop, processing user inputs,
        managing search filters, and displaying results. The loop continues until
        the user decides to exit.

        Returns:
            None
        """
        print(f"{Fore.GREEN}Olá! Sou seu assistente virtual para busca de automóveis.")
        print(
            f"{Fore.GREEN}Como posso ajudar você hoje? Está procurando algum carro específico?"
        )

        filters = {}
        end_loop = False

        while not end_loop:
            user_input = input(f"{Fore.BLUE}Você: ")

            if user_input.lower() in ["sair", "finalizar", "tchau"]:
                print(f"{Fore.GREEN}Assistente: Foi um prazer ajudar! Até a próxima.")
                break

            new_filters, need_more_info, next_question = self._analyze_entry(
                user_input, filters
            )

            filters.update(new_filters)

            if not need_more_info and filters:
                print(
                    f"{Fore.GREEN}Assistente: Ótimo! Vou buscar carros com esses critérios:"
                )
                for key, value in filters.items():
                    print(f"{Fore.CYAN} - {key}: {value}")

                mcp_server_response = await self.client.process_query(filters)

                if mcp_server_response:
                    print(
                        f"{Fore.GREEN}Assistente: Encontrei {len(mcp_server_response)} veículos que correspondem à sua busca:"
                    )
                    for i, car in enumerate(mcp_server_response[:5], 1):
                        print(
                            f"{Fore.YELLOW}{i}. {car.brand} {car.model} {car.year} {car.motorization} {car.fuel} - {car.color}"
                        )
                        print(f"{Fore.YELLOW}   {car.mileage}km - R$ {car.price:.2f}")

                    if len(mcp_server_response) > 5:
                        print(
                            f"{Fore.YELLOW}... e mais {len(mcp_server_response) - 5} resultados."
                        )
                else:
                    print(
                        f"{Fore.GREEN}Assistente: Não encontrei veículos com esses critérios. Pode tentar outros filtros?"
                    )

                print(
                    f"{Fore.GREEN}Assistente: Faça uma nova busca ou digite sair para finalizar"
                )
                filters = {}
            elif need_more_info and next_question:
                print(f"{Fore.GREEN}Assistente: {next_question}")

    def _analyze_entry(self, user_input, current_filters):
        """
        Analyze user input to extract car search criteria.

        This method uses LLM to interpret natural language input and extract
        structured search filters.

        Args:
            user_input (str): The user's natural language input
            current_filters (dict): Currently active search filters

        Returns:
            tuple: Contains:
                - dict: New filters extracted from user input
                - bool: Whether more information is needed
                - str: Next question to ask if more info is needed
        """
        try:
            prompt_template = """
            Extrai os critérios de busca para automóveis do seguinte texto e se já houver critérios, atualiza-os:
            Texto do usuário: {user_input}
            Critérios atuais: {current_filters}

            Responda em formato JSON puro, sem usar blocos de código (sem ```json ou ```), apenas o objeto JSON com os seguintes campos:
            - new_filters: objeto com os novos filtros identificados (brand, model, year_min, year_max, fuel, price_min, price_max, color, transmission)
            - need_more_info: booleano indicando se você precisa fazer mais perguntas
            - next_question: se need_more_info for true, qual pergunta fazer em seguida
            """

            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["user_input", "current_filters"]
            )
            
            chain = prompt | llm | StrOutputParser()
            response = chain.invoke({
                "user_input": user_input if user_input else "",
                "current_filters": current_filters if current_filters else ""
            })

            try:
                json_answer = json.loads(response)
            except json.JSONDecodeError:
                json_match = re.search(r"(\{.*\})", response, re.DOTALL)
                if json_match:
                    json_answer = json.loads(json_match.group(1))
                else:
                    return (
                        {},
                        True,
                        "Pode me dar mais detalhes sobre o carro que está procurando?",
                    )

            new_filters = json_answer.get("new_filters", {})
            need_more_info = json_answer.get("need_more_info", True)
            next_question = json_answer.get(
                "next_question", "Pode me dar mais detalhes?"
            )

            return new_filters, need_more_info, next_question

        except Exception as e:
            print(f"{Fore.RED}Erro ao processar entrada: {e}")
            return (
                {},
                True,
                "Desculpe, tive um problema ao entender sua solicitação. Pode reformular?",
            )


if __name__ == "__main__":
    agent = VirtualAgent()
    asyncio.run(agent.start_loop())
