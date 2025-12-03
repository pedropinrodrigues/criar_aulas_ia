from typing import Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any

def complete_code_agent(graph_state: Dict[str, Any]) -> Dict[str, Any]:
    
    pratical_class = graph_state["pratical_class"]
    
    if pratical_class.get('theory_documentation') is None:
        return graph_state
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    
    pratical_class_prompt = ChatPromptTemplate.from_messages([
        ("system",
        """You are an expert in creating a example code for educational purposes.
        Given the following theory documentation "{theory_documentation}", create a complete code example that illustrates the concepts discussed.
        The language to be used is {language}.
        Your task is to:
            Develop a comprehensive complete code example that includes:
            1. Clear and concise code that covers all necessary aspects of the theory.
            2. Use proper comments for better readability.
            3. Ensure that the code is functional and can be executed without errors.
            4. It should be readable for the student level: {student_level}
        """),
        ])
    
    llm_response = llm.invoke(pratical_class_prompt.format(
        theory_documentation=pratical_class["theory_documentation"],
        language=pratical_class["language"],
        student_level=graph_state["pratical_class"]["student_level"])
    )
    
    llm_output = llm_response.content
    
    graph_state["pratical_class"]["compelete_code"] = llm_output
    
    return graph_state

if __name__ == "__main__":
    
    ## Implement a simple test for the graphstatr["pratical_class"] agent
    
    import os 
    from dotenv import load_dotenv
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    
    graph_state: Dict[str, Any] = {
        "pratical_class": {
            "theory_documentation": "In programming, a function is a block of code that performs a specific task. Functions help in breaking down complex problems into smaller, manageable pieces. They can take inputs, process them, and return outputs. Functions promote code reusability and improve readability.",
            "language": "Python",
            "student_level": "Beginner",
            "compelete_code": "",
            "incomplete_code": "",
            "pratical_documentation": "",
        }
    }
    
    updated_graph_state = complete_code_agent(graph_state)
    print(updated_graph_state["pratical_class"])