from langgraph.graph import StateGraph, START, END
from schemas.state_classes import GraphState

from agents.complete_code_agent import complete_code_agent
from agents.incomplete_code_agent import incomplete_code_agent
from agents.pratical_doc import pratical_doc_agent
from agents.theory_agent import theory_agent
from agents.search_agent import search_agent

import os
import dotenv
from pathlib import Path


def save_markdown_log(file_name: str, content: str) -> str:
    """Persist the provided content as a Markdown file under logs_execucao."""
    logs_dir = Path(__file__).resolve().parent.parent / "logs_execucao"
    logs_dir.mkdir(parents=True, exist_ok=True)

    safe_name = file_name.strip() or "log"
    if not safe_name.lower().endswith(".md"):
        safe_name += ".md"

    title = Path(safe_name).stem.replace("_", " ").strip().title() or "Log"
    markdown_content = f"# {title}\n\n{content.strip()}\n"

    file_path = logs_dir / safe_name
    file_path.write_text(markdown_content, encoding="utf-8")
    return str(file_path)


def create_graph() -> StateGraph:
    dotenv.load_dotenv()
    os.environ["OPENAI_API_KEY"] = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")
    os.environ["TAVILY_API_KEY"] = dotenv.get_key(dotenv.find_dotenv(), "TAVILY_API_KEY")

    graph = StateGraph(GraphState)

    graph.add_node("theory_agent", theory_agent)
    graph.add_node("pratical_doc_agent", pratical_doc_agent)
    graph.add_node("incomplete_code_agent", incomplete_code_agent)
    graph.add_node("complete_code_agent", complete_code_agent)
    graph.add_node("search_agent", search_agent)

    graph.add_edge(START, "search_agent")
    graph.add_edge("search_agent", "theory_agent")
    graph.add_edge("theory_agent", "complete_code_agent")
    graph.add_edge("complete_code_agent", "incomplete_code_agent")
    graph.add_edge("incomplete_code_agent", "pratical_doc_agent")
    graph.add_edge("pratical_doc_agent", END)

    graph_compiled = graph.compile()
    
    return graph_compiled

def main(graph_state: GraphState) -> GraphState:
    graph = create_graph()
    final_state = graph.invoke(graph_state)
    return final_state

if __name__ == "__main__":
    initial_graph_state = GraphState(
        materials={
            "title": "Introduction to Python Programming",
            "public_type": "beginner",
            "topics": ["Variables and Data Types", "Control Structures", "Functions"],
            "result": [],  # ← Preenchido pelo search_agent
        },
        theory_class={
            "title": "Python Fundamentals - Variables and Control Flow",
            "content": "This class will cover the basics of Python programming, focusing on variables, data types, and control structures. Students will learn how to declare variables, use different data types, and implement conditional statements and loops.",
            "student_level": "beginner",
            "duration_minutes": 45,
            "references": [
                "https://docs.python.org/3/tutorial/introduction.html",
                "https://realpython.com/python-data-types/"
            ],
            "result": "",  # ← Preenchido pelo theory_agent
        },
        pratical_class={
            "theory_documentation": "",  # ← Preenchido pelo theory_agent (pode ser copiado de theory_class["result"])
            "language": "Python",
            "student_level": "beginner",
            "complete_code": "",  # ← Preenchido pelo complete_code_agent
            "incomplete_code": "",  # ← Preenchido pelo incomplete_code_agent
            "pratical_documentation": "",  # ← Preenchido pelo pratical_doc_agent
        },
    )
    
    final_state = main(initial_graph_state)
    
    materials_result = final_state["materials"]["result"]
    
    materials_result_str = "\n\n".join(
        f"- [{mat['type'].title()}]({mat['link']}): {mat['why']} (Topic: {mat['topic']})"
        for mat in materials_result
    )
    
    materials_result = materials_result_str
    
    theory_result = final_state["theory_class"]["result"]
    pratical_documentation = final_state["pratical_class"]["pratical_documentation"]
    complete_code = final_state["pratical_class"]["compelete_code"]
    incomplete_code = final_state["pratical_class"]["incomplete_code"]

    save_markdown_log("materials_result.md", str(materials_result))
    save_markdown_log("theory_class_result.md", theory_result)
    save_markdown_log("pratical_documentation.md", pratical_documentation)
    save_markdown_log("complete_code.md", complete_code)
    save_markdown_log("incomplete_code.md", incomplete_code)
    
    print("Execution completed. Logs saved in logs_execucao/")