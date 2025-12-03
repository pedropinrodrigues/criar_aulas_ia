from schemas.state_classes import GraphState
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def pratical_doc_agent(graph_state: GraphState) -> GraphState:
    """
    Agent that creates practical documentation for students.
    Compares complete and incomplete code to generate step-by-step instructions.
    """
    
    pratical_class = graph_state["pratical_class"]
    
    if pratical_class.get('complete_code') is None or pratical_class.get('incomplete_code') is None:
        return graph_state
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert programming instructor creating practical exercises for students.

        You have two versions of code:

        **COMPLETE CODE** (reference solution):
        ```
        {complete_code}
        ```

        **INCOMPLETE CODE** (what students will work with):
        ```
        {incomplete_code}
        ```

        Your task is to analyze the differences between these two code versions and create comprehensive practical documentation that:

        1. **Introduction**: Brief overview of what the student will build and why it's important (infer from the code purpose)
        2. **Learning Objectives**: Clear list of what the student will learn by completing the missing parts
        3. **Setup Instructions**: Any required setup or imports needed
        4. **Step-by-Step Guide**: 
        - Identify each missing part in the incomplete code
        - Explain what functionality is missing
        - Give hints and guide the student's thinking without revealing the complete solution
        - Explain the logic and reasoning behind each step
        - Include best practices and common pitfalls
        5. **Expected Output**: What the program should do when complete
        6. **Challenges** (optional): Extra tasks to extend learning
        7. **Testing Tips**: How to verify their solution works correctly

        Use proper Markdown formatting with:
        - Clear headings (##, ###)
        - Code blocks with syntax highlighting
        - Bullet points and numbered lists
        - Bold and italic for emphasis
        - Blockquotes for important tips

        Keep the tone encouraging and educational. Adapt your explanation complexity based on the code's difficulty level.""")
    ])
    
    response = llm.invoke(
        prompt.format_messages(
            complete_code=pratical_class.get("complete_code", ""),
            incomplete_code=pratical_class.get("incomplete_code", "")
        )
    )
    
    pratical_class["pratical_documentation"] = response.content.strip()
    
    return graph_state