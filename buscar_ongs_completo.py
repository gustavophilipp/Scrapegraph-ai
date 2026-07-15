from scrapegraphai.graphs import SearchGraph, SmartScraperGraph
import json

SUA_API_KEY = "sgai-655ba5f2-6226-469a-9bf1-fc127a633c3b"

graph_config = {
    "llm": {
        "api_key": SUA_API_KEY,
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": False,
}

print("=== Buscando ONGs no Google ===")
search_graph = SearchGraph(
    prompt="Find non-profit organizations in Brazil that work with education, health, or social causes. Extract: name, website, contact information, mission statement.",
    source="google",
    config=graph_config
)

search_result = search_graph.run()
print(json.dumps(search_result, indent=4))

print("\n=== Extraindo informações de um site específico ===")
smart_scraper = SmartScraperGraph(
    prompt="Extract all contact information, subscription opportunities, partnership details, and decision maker contacts from this NGO website.",
    source="https://www.ong-exemplo.com.br",
    config=graph_config
)

site_result = smart_scraper.run()
print(json.dumps(site_result, indent=4))