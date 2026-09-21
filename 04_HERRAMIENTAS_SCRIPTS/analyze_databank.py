import pandas as pd
import numpy as np
import argparse
import os
import zipfile
import re
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="StrategyQuant X Expert Databank Analyzer")
    parser.add_argument('--csv', required=True, help='Path to the exported Databank CSV file')
    parser.add_argument('--sqx-dir', default=r"C:\SQX_144_Full\user\projects\NDXM_TMILL_E2_M15PB_DIAGOFF\databanks", help='Path to the folder containing .sqx files')
    parser.add_argument('--top', type=int, default=5, help='Number of top strategies to output')
    return parser.parse_args()

def extract_indicators_from_sqx(sqx_path):
    """
    Reads the strategy_Portfolio.xml inside a .sqx file to extract the names of the indicators used,
    helping to identify 'twins' or highly correlated strategies manually.
    """
    indicators = set()
    try:
        with zipfile.ZipFile(sqx_path, 'r') as z:
            if 'strategy_Portfolio.xml' in z.namelist():
                xml_content = z.read('strategy_Portfolio.xml').decode('utf-8')
                # Extract simple indicator names like name="(ATR) Average True Range"
                matches = re.findall(r'name="([^"]+)"\s+display="', xml_content)
                for m in matches:
                    if m not in ['Trading signals', 'Long entry signal', 'Short entry signal', 'Long exit signal', 'Short exit signal']:
                        indicators.add(m)
    except Exception as e:
        pass
    return sorted(list(indicators))

def main():
    args = parse_args()
    csv_path = Path(args.csv)
    
    if not csv_path.exists():
        print(f"Error: CSV file {csv_path} not found.")
        return

    print(f"Loading Databank metrics from: {csv_path}")
    
    try:
        df = pd.read_csv(csv_path, sep=None, engine='python')
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        return

    col_map = {c: c.strip().lower() for c in df.columns}
    df.rename(columns=col_map, inplace=True)
    
    col_ret_dd = next((c for c in df.columns if 'return/dd' in c or 'ret/dd' in c), None)
    col_pf = next((c for c in df.columns if 'profit factor' in c or 'pf' == c), None)
    col_np = next((c for c in df.columns if 'net profit' in c or 'profit' in c), None)
    col_trades = next((c for c in df.columns if 'trades' in c), None)
    col_name = next((c for c in df.columns if 'strategy' in c or 'name' in c), None)

    if not col_name:
        print("Could not find a 'Strategy' or 'Name' column in the CSV. Available columns:")
        print(df.columns.tolist())
        return

    metrics_to_clean = [col_ret_dd, col_pf, col_np, col_trades]
    for col in metrics_to_clean:
        if col and col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'[^\d\.\-]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    print(f"Total strategies in CSV: {len(df)}")
    
    if col_trades and col_pf:
        df_filtered = df[(df[col_trades] > 50) & (df[col_pf] > 1.1)].copy()
        print(f"Strategies after basic filtering (Trades > 50, PF > 1.1): {len(df_filtered)}")
    else:
        df_filtered = df.copy()

    if col_ret_dd and col_pf:
        # Min-Max Normalize Ret/DD and Profit Factor for composite score
        min_r, max_r = df_filtered[col_ret_dd].min(), df_filtered[col_ret_dd].max()
        min_p, max_p = df_filtered[col_pf].min(), df_filtered[col_pf].max()
        
        norm_ret_dd = (df_filtered[col_ret_dd] - min_r) / (max_r - min_r + 1e-9)
        norm_pf = (df_filtered[col_pf] - min_p) / (max_p - min_p + 1e-9)
        
        # Weighted score: 60% Ret/DD, 40% PF
        df_filtered['composite_score'] = (norm_ret_dd * 0.6) + (norm_pf * 0.4)
        df_sorted = df_filtered.sort_values(by='composite_score', ascending=False)
    else:
        print("Warning: Missing Ret/DD or Profit Factor. Sorting by primary available metric.")
        sort_col = col_np or col_trades or df_filtered.columns[1]
        df_sorted = df_filtered.sort_values(by=sort_col, ascending=False)

    print(f"\n--- TOP {args.top} NON-CORRELATED STRATEGIES ---")
    sqx_dir = Path(args.sqx_dir)
    
    selected_strategies = []
    seen_indicator_signatures = set()

    for idx, row in df_sorted.iterrows():
        strat_name = str(row[col_name])
        strat_file = strat_name if strat_name.endswith('.sqx') else f"{strat_name}.sqx"
            
        sqx_path = None
        if sqx_dir.exists():
            for p in sqx_dir.rglob(strat_file):
                sqx_path = p
                break
                
        indicators = []
        if sqx_path:
            indicators = extract_indicators_from_sqx(sqx_path)
            
        sig = tuple(indicators)
        if sig in seen_indicator_signatures and len(sig) > 0:
            continue
            
        if len(sig) > 0:
            seen_indicator_signatures.add(sig)
            
        selected_strategies.append({
            'name': strat_name,
            'ret_dd': row[col_ret_dd] if col_ret_dd else 'N/A',
            'pf': row[col_pf] if col_pf else 'N/A',
            'trades': row[col_trades] if col_trades else 'N/A',
            'indicators': indicators
        })
        
        if len(selected_strategies) >= args.top:
            break

    for i, strat in enumerate(selected_strategies, 1):
        print(f"\n{i}. {strat['name']}")
        print(f"   Return/DD: {strat['ret_dd']} | PF: {strat['pf']} | Trades: {strat['trades']}")
        print(f"   Indicators: {', '.join(strat['indicators']) if strat['indicators'] else 'N/A (File not found/parsed)'}")

if __name__ == '__main__':
    main()
