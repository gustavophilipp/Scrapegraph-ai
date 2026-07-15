from scrapegraph_py import ScrapeGraphAI
import sys

client = ScrapeGraphAI(api_key="sgai-655ba5f2-6226-469a-9bf1-fc127a633c3b")

def buscar_ongs_e_extrair_info():
    print("=== Buscando ONGs para parcerias de assinatura ===")
    
    # Busca por ONGs com potencial para parcerias
    search_queries = [
        "ONGs Brasil tecnologia inclusão digital parceiras",
        "organizações sem fins lucrativos educação plataforma digital",
        "ONGs saúde telemedicina parcerias comerciais",
        "ONGs meio ambiente sustentabilidade aplicativos móveis"
    ]
    
    all_results = []
    
    for query in search_queries:
        print(f"\n=== Buscando: {query} ===")
        try:
            search_result = client.search(
                query=query,
                prompt="Find non-profit organizations that might be interested in app subscription partnerships",
                num_results=2
            )
            
            if hasattr(search_result, 'data') and hasattr(search_result.data, 'results'):
                results = search_result.data.results
                print(f"Encontrados {len(results)} resultados")
                
                for result in results:
                    print(f"\n--- Analisando: {result.title} ---")
                    print(f"URL: {result.url}")
                    
                    try:
                        scrape_result = client.scrape(url=result.url)
                        
                        if hasattr(scrape_result, 'data') and hasattr(scrape_result.data, 'results'):
                            markdown_content = scrape_result.data.results.get('markdown', {}).get('data', [''])[0]
                            
                            # Salvar informações
                            org_info = {
                                'title': result.title,
                                'url': result.url,
                                'content_preview': markdown_content[:500] if markdown_content else '',
                                'query': query
                            }
                            all_results.append(org_info)
                            
                            print(f"Conteúdo extraído: {len(markdown_content)} caracteres")
                            
                    except Exception as e:
                        print(f"Erro ao extrair: {e}")
                        
        except Exception as e:
            print(f"Erro na busca: {e}")
    
    # Relatório final
    print("\n" + "="*50)
    print("=== RELATÓRIO FINAL ===")
    print(f"Total de ONGs analisadas: {len(all_results)}")
    print("="*50)
    
    for i, org in enumerate(all_results, 1):
        print(f"\n{i}. {org['title']}")
        print(f"   URL: {org['url']}")
        print(f"   Busca: {org['query']}")
        print(f"   Preview: {org['content_preview'][:200]}...")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    buscar_ongs_e_extrair_info()