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