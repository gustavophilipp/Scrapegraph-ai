import requests
import json

API_KEY = "sgai-655ba5f2-6226-469a-9bf1-fc127a633c3b"

def scrape_ong_info(url):
    """Extrai informações de contato e oportunidades de parceria de um site de ONG"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": url,
        "prompt": "Extract: organization name, contact email, phone number, address, mission statement, current projects, decision maker contacts, partnership opportunities, and any existing subscription or donation programs.",
        "output_format": "json"
    }
    
    response = requests.post(
        "https://api.scrapegraphai.com/scrape",
        headers=headers,
        json=payload
    )
    
    return response.json()

def search_ongs(query):
    """Busca ONGs baseado em uma query"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": query,
        "prompt": "Extract: NGO name, website, contact email, phone, area of focus, location, and brief description",
        "num_results": 10
    }
    
    response = requests.post(
        "https://api.scrapegraphai.com/search",
        headers=headers,
        json=payload
    )
    
    return response.json()

if __name__ == "__main__":
    print("=== Buscando ONGs ===")
    query = "ONGs organizações não governamentais Brasil educação saúde causas sociais"
    search_results = search_ongs(query)
    
    print(f"Encontrados {len(search_results.get('results', []))} resultados")
    print(json.dumps(search_results, indent=4))
    
    if search_results.get('results'):
        first_ong_url = search_results['results'][0].get('url')
        if first_ong_url:
            print(f"\n=== Extraindo detalhes de {first_ong_url} ===")
            details = scrape_ong_info(first_ong_url)
            print(json.dumps(details, indent=4))