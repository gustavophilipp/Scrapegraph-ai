from scrapegraph_py import ScrapeGraphClient

client = ScrapeGraphClient(api_key="sgai-655ba5f2-6226-469a-9bf1-fc127a633c3b")

print("=== Buscando ONGs no Google ===")
search_result = client.search(
    query="ONGs organizações não governamentais Brasil educação saúde causas sociais",
    prompt="Extract: NGO name, website, contact email, phone, area of focus, location, and brief description",
    num_results=5
)

print(json.dumps(search_result, indent=4))

if search_result.get('results'):
    first_url = search_result['results'][0].get('url')
    if first_url:
        print(f"\n=== Extraindo detalhes de {first_url} ===")
        scrape_result = client.scrape(
            url=first_url,
            prompt="Extract: organization name, contact email, phone number, address, mission statement, current projects, decision maker contacts, partnership opportunities, and any existing subscription or donation programs.",
            output_format="json"
        )
        print(json.dumps(scrape_result, indent=4))