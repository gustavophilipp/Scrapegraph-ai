from scrapegraph_py import ScrapeGraphAI

client = ScrapeGraphAI(api_key="sgai-655ba5f2-6226-469a-9bf1-fc127a633c3b")

print("=== Buscando ONGs no Google ===")
try:
    search_result = client.search(
        query="ONGs organizações não governamentais Brasil educação saúde causas sociais",
        prompt="Extract: NGO name, website, contact email, phone, area of focus, location, and brief description",
        num_results=5
    )
    
    print(f"Tipo: {type(search_result)}")
    print(f"Resultado: {search_result}")
    
    if hasattr(search_result, 'results'):
        print(f"\nResultados encontrados: {len(search_result.results)}")
        for i, result in enumerate(search_result.results):
            print(f"\n--- Resultado {i+1} ---")
            print(f"URL: {result.url}")
            print(f"Title: {result.title}")
            
            if result.url:
                print(f"\n=== Extraindo detalhes de {result.url} ===")
                scrape_result = client.scrape(
                    url=result.url,
                    extract="organization name, contact email, phone number, address, mission statement, current projects, decision maker contacts, partnership opportunities"
                )
                print(f"Tipo: {type(scrape_result)}")
                print(f"Resultado: {scrape_result}")
                break
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()