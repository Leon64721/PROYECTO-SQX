import pandas as pd
import numpy as np
import os
import zipfile
import re
from pathlib import Path

def extract_indicators_from_sqx(sqx_path):
    indicators = set()
    try:
        with zipfile.ZipFile(sqx_path, 'r') as z:
            if 'strategy_Portfolio.xml' in z.namelist():
                xml_content = z.read('strategy_Portfolio.xml').decode('utf-8')
                matches = re.findall(r'name="([^"]+)"\s+display="', xml_content)
                for m in matches:
                    if m not in ['Trading signals', 'Long entry signal', 'Short entry signal', 'Long exit signal', 'Short exit signal']:
                        indicators.add(m)
    except Exception as e:
        pass
    return sorted(list(indicators))

def main():
    csv_path = Path(r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\Resultados Databank\NDXM TMILL E2 M15PB DIAGOFF\DatabankExportWFAMATRIX.csv")
    sqx_dir = Path(r"C:\SQX_144_Full\user\projects\NDXM_TMILL_E2_M15PB_DIAGOFF\databanks")
    
    if not csv_path.exists():
        print(f"Error: CSV file {csv_path} not found.")
        return

    print(f"Loading Databank metrics from: {csv_path}")
    
    try:
        df = pd.read_csv(csv_path, sep=';', engine='python')
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        return

    # Clean the necessary IS columns
    df['Net profit (IS)'] = pd.to_numeric(df['Net profit (IS)'], errors='coerce')
    df['Ret/DD Ratio (IS)'] = pd.to_numeric(df['Ret/DD Ratio (IS)'], errors='coerce')
    df['Profit factor (IS)'] = pd.to_numeric(df['Profit factor (IS)'], errors='coerce')
    df['# of trades (IS)'] = pd.to_numeric(df['# of trades (IS)'], errors='coerce')

    print(f"Total strategies in CSV: {len(df)}")
    
    # Filter strategies
    df_filtered = df[(df['# of trades (IS)'] > 50) & (df['Profit factor (IS)'] > 1.1)].copy()
    print(f"Strategies after basic filtering (Trades > 50, PF > 1.1): {len(df_filtered)}")

    # Min-Max normalization
    min_r, max_r = df_filtered['Ret/DD Ratio (IS)'].min(), df_filtered['Ret/DD Ratio (IS)'].max()
    min_p, max_p = df_filtered['Profit factor (IS)'].min(), df_filtered['Profit factor (IS)'].max()
    
    norm_ret_dd = (df_filtered['Ret/DD Ratio (IS)'] - min_r) / (max_r - min_r + 1e-9)
    norm_pf = (df_filtered['Profit factor (IS)'] - min_p) / (max_p - min_p + 1e-9)
    
    df_filtered['composite_score'] = (norm_ret_dd * 0.6) + (norm_pf * 0.4)
    df_sorted = df_filtered.sort_values(by='composite_score', ascending=False)

    print(f"\n--- TOP 5 NON-CORRELATED STRATEGIES ---")
    
    selected_strategies = []
    seen_indicator_signatures = set()

    for idx, row in df_sorted.iterrows():
        strat_name = str(row['Strategy Name']).strip()
        
        # Some CSVs contain (1) or (2) if exported multiple times, clean it to match file:
        strat_base_name = re.sub(r'\(\d+\)$', '', strat_name)
        strat_file = f"{strat_base_name}.sqx"
            
        sqx_path = None
        if sqx_dir.exists():
            for p in sqx_dir.rglob(strat_file):
                sqx_path = p
                break
                
        indicators = []
        if sqx_path:
            indicators = extract_indicators_from_sqx(sqx_path)
            
        sig = tuple(indicators)
        # Skip if we've seen this exact indicator combination before (it's a twin)
        if sig in seen_indicator_signatures and len(sig) > 0:
            continue
            
        if len(sig) > 0:
            seen_indicator_signatures.add(sig)
            
        selected_strategies.append({
            'name': strat_name,
            'ret_dd': row['Ret/DD Ratio (IS)'],
            'pf': row['Profit factor (IS)'],
            'trades': row['# of trades (IS)'],
            'np': row['Net profit (IS)'],
            'indicators': indicators,
            'composite_score': row['composite_score']
        })
        
        if len(selected_strategies) >= 5:
            break

    for i, strat in enumerate(selected_strategies, 1):
        print(f"\n{i}. {strat['name']}")
        print(f"   Net Profit: ${strat['np']} | Return/DD: {strat['ret_dd']} | PF: {strat['pf']} | Trades: {strat['trades']} | Comp. Score: {strat['composite_score']:.3f}")
        print(f"   Indicators: {', '.join(strat['indicators']) if strat['indicators'] else 'N/A'}")

if __name__ == '__main__':
    main()