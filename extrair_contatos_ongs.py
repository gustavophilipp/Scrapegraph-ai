from scrapegraph_py import ScrapeGraphAI
import sys
import re

client = ScrapeGraphAI(api_key="sgai-655ba5f2-6226-469a-9bf1-fc127a633c3b")

def extrair_contatos(conteudo):
    """Extrai emails e telefones do conteúdo"""
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', conteudo)
    telefones = re.findall(r'(\(?\d{2,3}\)?[\s-]?\d{4,5}[-\s]?\d{4})', conteudo)
    
    # Filtrar telefones válidos
    telefones_validos = []
    for telefone in telefones:
        # Remove espaços extras
        telefone_limpo = telefone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if len(telefone_limpo) >= 10 and len(telefone_limpo) <= 11:
            telefones_validos.append(telefone)
    
    return emails[:5], telefones_validos[:5]  # Limitar a 5 cada

def buscar_ongs_com_foco_em_contatos():
    print("=== Buscando ONGs com informações de contato ===")
    
    # Busca direta por sites de ONGs
    search_queries = [
        "site:*.org.br ONG contato email telefone",
        "\"organização não governamental\" contato Brasil",
        "\"associação sem fins lucrativos\" contato email",
        "ONGs Brasil \"fale conosco\" contato"
    ]
    
    all_ongs = []
    
    for query in search_queries:
        print(f"\n=== Buscando: {query} ===")
        try:
            search_result = client.search(
                query=query,
                prompt="Find NGO websites with contact information",
                num_results=2
            )
            
            if hasattr(search_result, 'data') and hasattr(search_result.data, 'results'):
                results = search_result.data.results
                print(f"Encontrados {len(results)} resultados")
                
                for result in results:
                    # Pular sites que não parecem ser de ONGs
                    if 'instagram.com' in result.url or 'youtube.com' in result.url:
                        continue
                        
                    print(f"\n--- Analisando: {result.title[:60]}... ---")
                    print(f"URL: {result.url}")
                    
                    try:
                        scrape_result = client.scrape(url=result.url)
                        
                        if hasattr(scrape_result, 'data') and hasattr(scrape_result.data, 'results'):
                            markdown_content = scrape_result.data.results.get('markdown', {}).get('data', [''])[0]
                            
                            # Extrair contatos
                            emails, telefones = extrair_contatos(markdown_content)
                            
                            # Procurar palavras-chave de contato
                            contato_keywords = ['contato', 'fale conosco', 'email', 'telefone', 'whatsapp', 'parceria']
                            tem_contato = any(keyword in markdown_content.lower() for keyword in contato_keywords)
                            
                            org_data = {
                                'nome': result.title,
                                'url': result.url,
                                'emails': emails,
                                'telefones': telefones,
                                'tem_pagina_contato': tem_contato,
                                'tamanho_conteudo': len(markdown_content),
                                'query_origem': query
                            }
                            
                            # Priorizar ONGs com contatos
                            if emails or telefones or tem_contato:
                                all_ongs.append(org_data)
                                print(f"✓ Emails encontrados: {len(emails)}")
                                print(f"✓ Telefones encontrados: {len(telefones)}")
                                print(f"✓ Página de contato: {tem_contato}")
                            
                    except Exception as e:
                        print(f"Erro ao extrair: {str(e)[:50]}...")
                        
        except Exception as e:
            print(f"Erro na busca: {str(e)[:50]}...")
    
    # Ordenar por potencial de contato
    all_ongs.sort(key=lambda x: (len(x['emails']) + len(x['telefones']) + (1 if x['tem_pagina_contato'] else 0)), reverse=True)
    
    # Relatório final
    print("\n" + "="*60)
    print("=== ONGs COM MAIOR POTENCIAL DE CONTATO ===")
    print("="*60)
    
    for i, org in enumerate(all_ongs[:10], 1):  # Top 10
        print(f"\n{i}. {org['nome'][:70]}...")
        print(f"   URL: {org['url']}")
        print(f"   Emails: {', '.join(org['emails']) if org['emails'] else 'Não encontrados'}")
        print(f"   Telefones: {', '.join(org['telefones']) if org['telefones'] else 'Não encontrados'}")
        print(f"   Tem página de contato: {'Sim' if org['tem_pagina_contato'] else 'Não'}")
        print(f"   Potencial: {len(org['emails']) + len(org['telefones']) + (1 if org['tem_pagina_contato'] else 0)}/3")
    
    # Salvar em arquivo
    print(f"\n=== Total de ONGs analisadas: {len(all_ongs)} ===")
    print("=== Top ONGs salvas em: ongs_contatos.txt ===")
    
    with open('ongs_contatos.txt', 'w', encoding='utf-8') as f:
        f.write("=== ONGs PARA PARCERIAS DE ASSINATURA ===\n\n")
        for org in all_ongs:
            f.write(f"NOME: {org['nome']}\n")
            f.write(f"URL: {org['url']}\n")
            f.write(f"EMAILS: {', '.join(org['emails']) if org['emails'] else 'N/A'}\n")
            f.write(f"TELEFONES: {', '.join(org['telefones']) if org['telefones'] else 'N/A'}\n")
            f.write(f"PÁGINA CONTATO: {'Sim' if org['tem_pagina_contato'] else 'Não'}\n")
            f.write(f"POTENCIAL: {len(org['emails']) + len(org['telefones']) + (1 if org['tem_pagina_contato'] else 0)}/3\n")
            f.write("-" * 60 + "\n\n")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    buscar_ongs_com_foco_em_contatos()