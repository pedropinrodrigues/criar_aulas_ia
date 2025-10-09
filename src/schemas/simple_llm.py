from langchain_openai import ChatOpenAI
import os
import dotenv

class SimpleLLM():
    def __init__(self, model_name: str, temperature: float):
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)

    def generate(self, prompt: str) -> str:
        response = self.llm.invoke(prompt).content
        return response
    