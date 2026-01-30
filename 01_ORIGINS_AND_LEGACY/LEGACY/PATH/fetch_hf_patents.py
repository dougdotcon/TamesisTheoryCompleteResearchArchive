from datasets import load_dataset
import pandas as pd
import argparse

def fetch_sample(dataset_name="HUPD/hupd", config="sample", limit=5):
    """
    Fetches a sample from a Hugging Face patent dataset.
    Note: HUPD might require specific configs or authentication.
    We default to a known accessible logic or a fallback if HUPD is gated.
    """
    print(f"[*] Connecting to Hugging Face: {dataset_name}...")
    
    try:
        # HUPD often requires year/month configuration
        # If HUPD fails (often gated/requires approval), we fallback to 'big_patent'
        if "hupd" in dataset_name.lower():
            # Try loading a specific smaller config if possible, or stream
            # Using 'sample' config if available, otherwise defaulting to year-specific
            ds = load_dataset(dataset_name, name="sample", split="train", streaming=True)
        else:
            ds = load_dataset(dataset_name, split="train", streaming=True)
        
        print(f"[*] Streaming first {limit} records...")
        
        records = []
        for i, item in enumerate(ds):
            if i >= limit:
                break
            
            # Normalize fields based on dataset structure
            title = item.get("title", item.get("abstract", "No Title")[:50])
            abstract = item.get("abstract", "")
            date = item.get("filling_date", item.get("publication_date", "Unknown"))
            
            records.append({
                "Title": title,
                "Abstract": abstract[:100] + "...",
                "Date": date
            })
            
        return pd.DataFrame(records)

    except Exception as e:
        print(f"[!] Primary dataset failed: {e}")
        print("[*] Attempting fallback to 'big_patent'...")
        try:
            ds = load_dataset("big_patent", "a", split="train", streaming=True)
            records = []
            for i, item in enumerate(ds):
                if i >= limit:
                    break
                records.append({
                    "Title": "BigPatent Record (No Title Field)", 
                    "Abstract": item.get("description", "")[:100] + "...",
                    "Date": "Unknown"
                })
            return pd.DataFrame(records)
        except Exception as e2:
            print(f"[!] Fallback failed: {e2}")
            return pd.DataFrame()

def main():
    parser = argparse.ArgumentParser(description="Hugging Face Patent Fetcher")
    parser.add_argument("--dataset", type=str, default="HUPD/hupd", help="Dataset ID (e.g., HUPD/hupd, big_patent)")
    parser.add_argument("--limit", type=int, default=5, help="Number of records to fetch")
    
    args = parser.parse_args()
    
    df = fetch_sample(args.dataset, limit=args.limit)
    
    if not df.empty:
        print("\n" + "="*50)
        print(f"SUCCESS: Fetched {len(df)} records")
        print("="*50)
        print(df.to_string())
    else:
        print("\n[!] Failed to fetch any data.")

if __name__ == "__main__":
    main()
