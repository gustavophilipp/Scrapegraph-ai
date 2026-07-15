from scrapegraphai.graphs import SearchGraph

graph_config = {
    "llm": {
        "api_key": "sgai-655ba5f2-6226-469a-9bf1-fc127a633c3b",
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": False,
}

search_graph = SearchGraph(
    prompt="Find non-profit organizations (ONGs/NGOs) that might be interested in selling app subscriptions. Extract: organization name, website, contact email, phone, area of focus, and location.",
    source="google",
    config=graph_config
)

result = search_graph.run()

import json
print(json.dumps(result, indent=4))