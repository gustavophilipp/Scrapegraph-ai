from scrapegraph_py import ScrapeGraphAI
import sys
import re
import json
from datetime import datetime

client = ScrapeGraphAI(api_key="sgai-655ba5f2-6226-469a-9bf1-fc127a633c3b")

def extrair_contatos(conteudo):
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', conteudo)
    telefones = re.findall(r'(\(?\d{2,3}\)?[\s-]?\d{4,5}[-\s]?\d{4})', conteudo)
    telefones_validos = []
    for telefone in telefones:
        telefone_limpo = telefone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if len(telefone_limpo) >= 10 and len(telefone_limpo) <= 11:
            telefones_validos.append(telefone)
    return emails[:5], telefones_validos[:5]

def analisar_potencial_vendas(conteudo):
    """Analisa se a ONG tem potencial para vendas de assinaturas"""
    indicadores_positivos = [
        'associação', 'membro', 'associado', 'assinatura', 'mensalidade',
        'doação recorrente', 'parceria', 'plano', 'benefício', 'desconto',
        'programa', 'projeto', 'iniciativa', 'voluntário', 'doador'
    ]
    
    indicadores_tecnologia = [
        'aplicativo', 'plataforma', 'digital', 'tecnologia', 'inovação',
        'app', 'mobile', 'site', 'online', 'sistema', 'software'
    ]
    
    score_positivos = sum(1 for indicador in indicadores_positivos if indicador.lower() in conteudo.lower())
    score_tecnologia = sum(1 for indicador in indicadores_tecnologia if indicador.lower() in conteudo.lower())
    
    return {
        'score_positivos': score_positivos,
        'score_tecnologia': score_tecnologia,
        'score_total': score_positivos + score_tecnologia
    }

def gerar_leads_qualificados():
    print("=== GERANDO LEADS QUALIFICADOS PARA VENDAS DE ASSINATURAS ===")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Buscas focadas em ONGs com potencial de receita recorrente
    search_queries = [
        "\"associação sem fins lucrativos\" membros assinatura Brasil",
        "ONG \"programa de membros\" doação mensal",
        "\"organização social\" benefícios associados plano",
        "ONG Brasil tecnologia digital inovação parceiras",
        "\"instituto sem fins lucrativos\" projetos patrocínio"
    ]
    
    leads_qualificados = []
    
    for query in search_queries:
        print(f"\n=== Buscando: {query} ===")
        try:
            search_result = client.search(
                query=query,
                prompt="Find non-profit organizations with membership programs or partnership opportunities",
                num_results=2
            )
            
            if hasattr(search_result, 'data') and hasattr(search_result.data, 'results'):
                results = search_result.data.results
                print(f"Encontrados {len(results)} resultados")
                
                for result in results:
                    if 'instagram.com' in result.url or 'youtube.com' in result.url:
                        continue
                        
                    print(f"--- Analisando: {result.title[:50]}... ---")
                    
                    try:
                        scrape_result = client.scrape(url=result.url)
                        
                        if hasattr(scrape_result, 'data') and hasattr(scrape_result.data, 'results'):
                            markdown_content = scrape_result.data.results.get('markdown', {}).get('data', [''])[0]
                            
                            emails, telefones = extrair_contatos(markdown_content)
                            potencial = analisar_potencial_vendas(markdown_content)
                            
                            # Classificar lead
                            classificacao = "Frio"
                            if potencial['score_total'] >= 5 and (emails or telefones):
                                classificacao = "Quente"
                            elif potencial['score_total'] >= 3 and (emails or telefones):
                                classificacao = "Morno"
                            
                            lead = {
                                'nome': result.title,
                                'url': result.url,
                                'emails': list(set(emails)),  # Remover duplicatas
                                'telefones': list(set(telefones)),
                                'classificacao': classificacao,
                                'score_potencial': potencial['score_total'],
                                'score_positivos': potencial['score_positivos'],
                                'score_tecnologia': potencial['score_tecnologia'],
                                'tem_contato': len(emails) > 0 or len(telefones) > 0,
                                'tamanho_conteudo': len(markdown_content),
                                'query_origem': query
                            }
                            
                            if lead['classificacao'] in ["Quente", "Morno"]:
                                leads_qualificados.append(lead)
                                print(f"✓ Lead: {classificacao} | Score: {potencial['score_total']} | Emails: {len(emails)} | Tel: {len(telefones)}")
                            
                    except Exception as e:
                        print(f"Erro: {str(e)[:40]}...")
                        
        except Exception as e:
            print(f"Erro na busca: {str(e)[:40]}...")
    
    # Ordenar leads por potencial
    leads_qualificados.sort(key=lambda x: x['score_potencial'], reverse=True)
    
    # Relatório detalhado
    print("\n" + "="*70)
    print("=== LEADS QUALIFICADOS PARA VENDAS ===")
    print("="*70)
    
    leads_quentes = [l for l in leads_qualificados if l['classificacao'] == "Quente"]
    leads_mornos = [l for l in leads_qualificados if l['classificacao'] == "Morno"]
    
    print(f"\n🔥 LEADS QUENTES ({len(leads_quentes)}):")
    for i, lead in enumerate(leads_quentes, 1):
        print(f"\n{i}. {lead['nome'][:60]}...")
        print(f"   Score: {lead['score_potencial']} (Positivos: {lead['score_positivos']}, Tech: {lead['score_tecnologia']})")
        print(f"   Emails: {', '.join(lead['emails']) if lead['emails'] else 'N/A'}")
        print(f"   Telefones: {', '.join(lead['telefones']) if lead['telefones'] else 'N/A'}")
        print(f"   URL: {lead['url']}")
    
    print(f"\n🌡️ LEADS MORNOS ({len(leads_mornos)}):")
    for i, lead in enumerate(leads_mornos, 1):
        print(f"\n{i}. {lead['nome'][:60]}...")
        print(f"   Score: {lead['score_potencial']}")
        print(f"   URL: {lead['url']}")
    
    # Salvar em JSON
    relatorio = {
        'data_geracao': datetime.now().isoformat(),
        'total_leads': len(leads_qualificados),
        'leads_quentes': len(leads_quentes),
        'leads_mornos': len(leads_mornos),
        'leads': leads_qualificados
    }
    
    with open('leads_vendas_assinaturas.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    # Salvar em CSV para fácil importação
    with open('leads_vendas_assinaturas.csv', 'w', encoding='utf-8') as f:
        f.write("Classificacao,Score,Nome,Emails,Telefones,URL\n")
        for lead in leads_qualificados:
            emails_csv = '|'.join(lead['emails']) if lead['emails'] else ''
            telefones_csv = '|'.join(lead['telefones']) if lead['telefones'] else ''
            nome_csv = lead['nome'].replace(',', '')[:50]
            f.write(f"{lead['classificacao']},{lead['score_potencial']},{nome_csv},{emails_csv},{telefones_csv},{lead['url']}\n")
    
    print(f"\n=== RELATÓRIO FINAL ===")
    print(f"Total de leads qualificados: {len(leads_qualificados)}")
    print(f"Leads quentes: {len(leads_quentes)} (prioridade alta)")
    print(f"Leads mornos: {len(leads_mornos)} (prioridade média)")
    print(f"\nArquivos gerados:")
    print(f"- leads_vendas_assinaturas.json (detalhado)")
    print(f"- leads_vendas_assinaturas.csv (para planilhas)")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    gerar_leads_qualificados()