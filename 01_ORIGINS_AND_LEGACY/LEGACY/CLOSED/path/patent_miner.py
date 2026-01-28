import argparse
import json
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import fetch_hf_patents  # Import the verified fetcher

# Mock OpenRouter/LLM interaction for prototype
# In a real scenario, this would import openai and configure the client
def analyze_patent_with_ai(patent_data, api_key=None):
    """
    Analyzes patent data using either real LLM API or mock logic.
    """
    print(f"[*] Analisando patente: {patent_data['title']}...")
    
    # REAL API MODE
    if api_key:
        try:
            import openai
            client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )
            
            prompt = f"""Você é um analista técnico e estratégico.
Avalie esta patente antiga considerando tecnologia atual.

Título: {patent_data['title']}
Descrição: {patent_data.get('description', patent_data.get('abstract', ''))}

Responda APENAS em JSON válido com a seguinte estrutura:
{{
  "problema_ainda_existe": true/false,
  "barreira_original": "tecnica | custo | regulatoria | mercado",
  "o_que_mudou_desde_entao": "...",
  "potencial_com_tecnologia_atual": 0-10,
  "possiveis_mercados_atuais": ["..."],
  "comentario_critico": "..."
}}"""

            response = client.chat.completions.create(
                model="meta-llama/llama-3.2-3b-instruct:free",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                print(f"[!] Failed to parse LLM response, using fallback.")
                return _mock_analysis(patent_data)
                
        except Exception as e:
            print(f"[!] API Error: {e}. Using mock fallback.")
            return _mock_analysis(patent_data)
    
    # MOCK MODE (default)
    return _mock_analysis(patent_data)

def _mock_analysis(patent_data):
    """Internal mock analysis logic."""
    time.sleep(1)
    desc = patent_data.get('description', '').lower()
    score = 5
    if 'energy' in desc or 'power' in desc:
        score += 2
    if 'pharmaceutical' in desc:
        score += 1
        
    return {
        "problema_ainda_existe": True,
        "barreira_original": "custo" if "expensive" in desc else "tecnica",
        "o_que_mudou_desde_entao": "Avanços em novos materiais e IA reduziram custos de simulação.",
        "potencial_com_tecnologia_atual": min(score, 10),
        "possiveis_mercados_atuais": ["Energia Renovável", "Manufatura Avançada"],
        "comentario_critico": "Patente promissora se adaptada com novos compósitos."
    }

def calculate_score(ai_result):
    """
    Calculates the final score based on the formula:
    score = (potencial * 2 + (barreira == "custo") * 2 + (barreira == "regulatoria") * 3)
    """
    potencial = ai_result.get("potencial_com_tecnologia_atual", 0)
    barreira = ai_result.get("barreira_original", "").lower()
    
    score = potencial * 2
    if "custo" in barreira:
        score += 2
    if "regulatoria" in barreira:
        score += 3
        
    return score

def scrape_google_patents(query, limit=5):
    """
    Simulates scraping Google Patents. 
    In a real MVP this might parse HTML, but Google blocks heavy scraping.
    We will mock this for the prototype to ensure reliability during demo.
    """
    print(f"[*] Buscando patentes expiradas para: '{query}'...")
    
    # Mock Data
    mock_patents = [
        {
            "id": "US-1234567-A",
            "title": "Method for efficient solar energy conversion using crystalline silicon",
            "abstract": "A method for converting solar energy...",
            "description": "This invention relates to expensive crystalline structures. The cost of manufacturing is high.",
            "filing_date": "1998-05-12",
            "status": "Expired"
        },
        {
            "id": "US-9876543-B",
            "title": "Autonomous drone delivery system mechanism",
            "abstract": "Unmanned aerial vehicle for package delivery...",
            "description": "Requires advanced processing power not available at the time. Technical barrier due to latency.",
            "filing_date": "2001-08-20",
            "status": "Expired"
        },
        {
            "id": "US-5555555-C",
            "title": "Nuclear battery modular casing",
            "abstract": "Safety casing for small scale nuclear devices...",
            "description": "Regulatory barriers prevent adoption. Safety concerns are paramount.",
            "filing_date": "1995-01-15",
            "status": "Expired"
        }
    ]
    
    return mock_patents[:limit]

    # ... (imports remain)
    import fetch_hf_patents  # Import the verified fetcher

    # ... (analyze_patent_with_ai and calculate_score remain unchanged)

def main():
    parser = argparse.ArgumentParser(description="Patent Miner - Intellectual Property Excavator")
    parser.add_argument("--query", type=str, default="energy storage", help="Search query for patents")
    parser.add_argument("--limit", type=int, default=5, help="Number of patents to analyze")
    parser.add_argument("--apikey", type=str, help="LLM API Key (optional, defaults to Mock mode)")
    parser.add_argument("--output", type=str, default="patent_mining_results.csv", help="Output file path")
    parser.add_argument("--source", type=str, choices=["mock", "hf"], default="mock", help="Data source: 'mock' or 'hf' (Hugging Face)")
    
    args = parser.parse_args()
    
    # 1. Scrape / Ingest
    if args.source == "hf":
        print(f"[*] Switching to REAL DATA from Hugging Face...")
        # Map HF columns to Miner expected format
        df_hf = fetch_hf_patents.fetch_sample(limit=args.limit)
        if df_hf.empty:
            print("[!] No data received from Hugging Face. Exiting.")
            return
            
        patents = []
        for _, row in df_hf.iterrows():
            patents.append({
                "id": "HF-Unknown",
                "title": row.get("Title", "No Title"),
                "abstract": row.get("Abstract", ""),
                "description": row.get("Abstract", ""), # Use abstract as desc for now if full text missing
                "filing_date": row.get("Date", "Unknown"),
                "status": "Unknown (Assumed Expired for Pilot)"
            })
    else:
        # Default Mock
        patents = scrape_google_patents(args.query, args.limit)
    
    results = []
    
    # 2. Analyze & Score
    for patent in patents:
        ai_analysis = analyze_patent_with_ai(patent, args.apikey)
        final_score = calculate_score(ai_analysis)
        
        result_row = {
            "ID": patent["id"],
            "Title": patent["title"],
            "Filing Date": patent["filing_date"],
            "Status": patent["status"],
            "Viability Score": final_score,
            "Potential (0-10)": ai_analysis.get("potencial_com_tecnologia_atual"),
            "Original Barrier": ai_analysis.get("barreira_original"),
            "Modern Market": ", ".join(ai_analysis.get("possiveis_mercados_atuais", [])),
            "Critical Comment": ai_analysis.get("comentario_critico")
        }
        results.append(result_row)
        
    # 3. Export
    df = pd.DataFrame(results)
    
    if not df.empty:
        # Sort by Score descending
        df = df.sort_values(by="Viability Score", ascending=False)
        
        print("\n" + "="*50)
        print("TOP HIDDEN ASSETS FOUND")
        print("="*50)
        print(df[["Title", "Viability Score", "Original Barrier"]].to_string(index=False))
        
        df.to_csv(args.output, index=False)
        print(f"\n[+] Resultados salvos em: {args.output}")
    else:
        print("\n[!] Nenhum resultado gerado.")

if __name__ == "__main__":
    main()
