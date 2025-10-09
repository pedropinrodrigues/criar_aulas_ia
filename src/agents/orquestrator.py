import os, dotenv
from typing import Annotated
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from schemas.state_classes import GraphState

# TypedDicts are just type annotations for dict shapes — you don't call them.
# Create a dict that matches the GraphState shape and annotate it for type checkers.
graph_state: GraphState = {
	"materials": {
		"title": "",
		"topics": [],
		"results": [],
		"result": [],
	}
}