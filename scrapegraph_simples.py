from scrapegraph_py import ScrapeGraphAI
import sys

client = ScrapeGraphAI(api_key="sgai-655ba5f2-6226-469a-9bf1-fc127a633c3b")

print("=== Buscando ONGs no Google ===")
try:
    search_result = client.search(
        query="ONGs organizações não governamentais Brasil educação saúde causas sociais",
        prompt="Extract: NGO name, website, contact email, phone, area of focus, location, and brief description",
        num_results=3
    )
    
    sys.stdout.reconfigure(encoding='utf-8')
    
    if hasattr(search_result, 'data') and hasattr(search_result.data, 'results'):
        results = search_result.data.results
        print(f"\nResultados encontrados: {len(results)}")
        
        for i, result in enumerate(results):
            print(f"\n--- Resultado {i+1} ---")
            print(f"URL: {result.url}")
            print(f"Title: {result.title}")
            
            if result.url and i == 0:
                print(f"\n=== Extraindo detalhes de {result.url} ===")
                try:
                    scrape_result = client.scrape(url=result.url)
                    
                    if hasattr(scrape_result, 'data'):
                        print(f"Conteúdo extraído (primeiros 800 caracteres):")
                        print(str(scrape_result.data)[:800])
                    else:
                        print(f"Resultado scrape: {scrape_result}")
                        
                except Exception as e:
                    print(f"Erro no scrape: {e}")
                break
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()