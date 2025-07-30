import pandas as pd
import glob
import os
from datetime import datetime

def parse_custom_date(date_string):
    try:
        if pd.isna(date_string) or date_string == '':
            return None

        cleaned_date = str(date_string).replace(' @ ', ' ').split('.')[0]
        return pd.to_datetime(cleaned_date, format='%b %d, %Y %H:%M:%S')
    except:
        try:
            return pd.to_datetime(date_string, errors='coerce')
        except:
            return None

def combine_csv_files():
    
    # Encontrar CSVs en carpeta
    csv_files = glob.glob("*.csv")
    
    if not csv_files:
        print("No CSV files found in the current directory.")
        return
    
    print(f"Found {len(csv_files)} CSV files:")
    for file in csv_files:
        print(f"  - {file}")
    
    dataframes = []
    total_rows = 0
    debug_info = []
    
    for file in csv_files:
        try:
            print(f"\nProcessing {file}...")
            
            df = pd.read_csv(file, 
                           quoting=1,
                           escapechar='\\',
                           encoding='utf-8',
                           on_bad_lines='warn')
            
            print(f"  Initial shape: {df.shape}")
            
            expected_columns = ['text', 'title', 'country', 'date', 'url']
            missing_columns = [col for col in expected_columns if col not in df.columns]
            
            if missing_columns:
                print(f"Warning: {file} is missing columns: {missing_columns}")
                debug_info.append(f"File {file}: Missing columns {missing_columns}")
                continue
            
            # Eliminar nulls
            initial_count = len(df)
            df_clean = df.dropna(subset=['title', 'url'])
            dropped_null = initial_count - len(df_clean)
            if dropped_null > 0:
                print(f"  Dropped {dropped_null} rows with null title/url")
            
            df_clean['date_original'] = df_clean['date']  
            df_clean['date_parsed'] = df_clean['date'].apply(parse_custom_date)  
            
            valid_dates = df_clean['date_parsed'].notna().sum()
            total_dates = len(df_clean)
            print(f"  Date parsing: {valid_dates}/{total_dates} valid dates")
            
            if valid_dates < total_dates:
                invalid_samples = df_clean[df_clean['date_parsed'].isna()]['date_original'].head(3).tolist()
                print(f"    Sample invalid dates: {invalid_samples}")
                debug_info.append(f"File {file}: {total_dates - valid_dates} invalid dates")
            
            text_lengths = df_clean['text'].str.len()
            print(f"  Text length stats - Min: {text_lengths.min()}, Max: {text_lengths.max()}, Mean: {text_lengths.mean():.0f}")
            
            very_short_text = df_clean[text_lengths < 10]
            if len(very_short_text) > 0:
                print(f"  Found {len(very_short_text)} rows with very short text (<10 chars)")
                debug_info.append(f"File {file}: {len(very_short_text)} rows with very short text")
            
            df_clean['source_file'] = file
            df_clean['id'] = range(total_rows + 1, total_rows + len(df_clean) + 1)
            
            dataframes.append(df_clean)
            total_rows += len(df_clean)
            print(f"  Final rows added: {len(df_clean)}")
            
        except Exception as e:
            print(f"Error reading {file}: {str(e)}")
            debug_info.append(f"File {file}: Critical error - {str(e)}")
            continue
    
    if not dataframes:
        print("No valid CSV files could be processed.")
        return
    
    # Combinar dataframes
    print(f"\nCombining {len(dataframes)} files...")
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # Guardar CSV
    output_filename = "combined_news_data.csv"
    print(f"Saving combined data to {output_filename}...")
    combined_df.to_csv(output_filename, 
                      index=False,
                      quoting=1,
                      escapechar='\\')
    
    print(f"\nCombination complete!")
    print(f"Total rows processed: {total_rows}")
    print(f"Final combined rows: {len(combined_df)}")
    print(f"Output saved as: {output_filename}")
    
    print(f"\nBasic statistics:")
    print(f"Countries represented: {combined_df['country'].nunique()}")
    print(f"Unique countries: {sorted(combined_df['country'].unique())}")
    
    valid_dates_total = combined_df['date_parsed'].notna().sum()
    print(f"Valid dates: {valid_dates_total}/{len(combined_df)} ({valid_dates_total/len(combined_df)*100:.1f}%)")
    
    if valid_dates_total > 0:
        date_range = combined_df['date_parsed'].dropna()
        print(f"Date range: {date_range.min()} to {date_range.max()}")
    
    if debug_info:
        print(f"\n=== DEBUG INFORMATION ===")
        for info in debug_info:
            print(info)
        print("=== END DEBUG INFO ===")
    
    print(f"\n=== DATE COMPARISON SAMPLE ===")
    sample_size = min(5, len(combined_df))
    for i in range(sample_size):
        row = combined_df.iloc[i]
        print(f"Row {i+1}: '{row['date_original']}' -> {row['date_parsed']}")
    
    return combined_df

if __name__ == "__main__":
    combined_data = combine_csv_files()
