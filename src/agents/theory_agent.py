from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool
from typing import Dict, Any
from bs4 import BeautifulSoup
import requests
import json
import os 
import dotenv

@tool
def inspect_text_references(references: list[str]) -> dict[str, Any]:
    """Tool focused in scraping and acessing the links provided in the references list."""
    
    references_content = {}
    for url in references:

        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            print("Successfully fetched the webpage!")
        else:
            print(f"Failed to fetch the webpage. Status code: {response.status_code}")
            
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = soup.get_text()
        references_content[url] = text_content[:2000]
        
    return references_content

def theory_agent(graph_state: Dict[str, Any]) -> Dict[str, Any]:
    
    theory_class = graph_state["theory_class"]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    
    theory_class_prompt = ChatPromptTemplate.from_messages([
        ("system",
        """You are an expert in creating structured theoretical classes for educational purposes.
        Given the following topic "{title}", create a well-structured class.
        This is a resume containing indications about the class content:
        {content}
        The expected duration of the class is {duration_minutes} minutes.
        If there are references provided in {references}, you should use the tool inspect_text_references.
        
        Your task is to:
            Develop a comprehensive theoretical class structure that includes:
            1. A clear and concise title.
            2. An in-depth content section that covers all necessary aspects of the topic.
            3. A list of references used to build the class.
            4. Use proper Markdown formatting for better readability.
            5. Ensure that the class fits the time provided, content asked and follows the references if any.
        """),
        ("placeholder", "{agent_scratchpad}"),
        ])
    
    agent = create_tool_calling_agent(llm, [inspect_text_references], theory_class_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[inspect_text_references], verbose=True)
    
    # Passa os dados pro agent_executor via invoke
    result = agent_executor.invoke({
        "title": theory_class['title'],
        "content": theory_class['content'],
        "duration_minutes": theory_class['duration_minutes'],
        "references": theory_class.get('references', [])
    })
    
    json_text = result['output'].strip()
    theory_class['result'] = json_text
    graph_state["theory_class"] = theory_class
    
    return graph_state

if __name__ == "__main__":
    dotenv.load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    
    # Teste rápido do agente de teoria
    graph_state: Dict[str, Any] = {
        "theory_class": {
            "title": "Introdução à Programação em Python",
            "content": "Python é uma linguagem de programação versátil e amplamente utilizada. Nesta aula, abordaremos os conceitos básicos, incluindo sintaxe, tipos de dados, estruturas de controle e funções.",
            "duration_minutes": 45,
            "references": [
                "https://docs.python.org/3/tutorial/",
                "https://www.w3schools.com/python/"
            ]
        }
    }
    
    updated_graph_state = theory_agent(graph_state)
    print(updated_graph_state["theory_class"]["result"])