from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def incomplete_code_agent(graph_state: Dict[str, Any]) -> Dict[str, Any]:
    
    pratical_class = graph_state["pratical_class"]
    
    if pratical_class.get('compelete_code') is None:
        return graph_state
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system",
        """Your are a agent focused in generating an incomplete code example based on the provided complete code and in other factors.
        This code function should be used in educational context, so the incomplete code should have parts missing for the student to fill in.
        Given the following complete code example "{compelete_code}", create an incomplete code example by using this complete code as base.
        This code should be done so the student can understant the concepts implemented in the complete code and practice them by filling the gaps in the incomplete code.
        The language to be used is {language}.
        The student level for this class is {student_level}.
        
        Your task is to:
            Develop a comprehensive incomplete code example that includes:
            1. Clear and concise code that covers all necessary aspects inplemented in the complete code.
            2. Remove or mask certain parts of the code to create gaps for students to fill in.
            3. Use proper comments for better readability.
            4. Ensure that the incomplete code is functional and can be executed without errors once completed by the student.
        """),
        ])
    
    llm_response = llm.invoke(prompt.format(
        compelete_code=pratical_class["compelete_code"],
        language=pratical_class["language"],
        student_level=graph_state["pratical_class"]["student_level"])
    )
    
    llm_output = llm_response.content
    graph_state["pratical_class"]["incomplete_code"] = llm_output
    
    return graph_state