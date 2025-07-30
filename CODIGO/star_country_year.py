import pandas as pd
from datetime import datetime

def generate_comprehensive_analysis(input_file, cutoff_year=2016):
    
    # Temas
    current_terms = [
        "salud mental",
        "depresión", 
        "ansiedad",
        "suicidio",
        "estrés",
        "psiquiatría",
        "psicología",
        "trastorno mental",
        "enfermedad mental"
    ]
    
    try:
        # Leer CSV
        df = pd.read_csv(input_file)
        print(f"Original dataset: {len(df)} records")
        
        # Formato Fecha
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        
        # Año limite
        df = df[df['year'] >= cutoff_year]
        print(f"After {cutoff_year} cutoff: {len(df)} records")
        
        # Generar Tablas
        generate_country_year_pivot(df)
        generate_topic_analysis(df, current_terms, cutoff_year)
        generate_extreme_ratings(df)
        
        print(f"\nAll files generated successfully!")
        print(f"Years covered: {df['year'].min()} - {df['year'].max()}")
        print(f"Countries: {df['country'].nunique()}")
        print(f"Unique countries: {sorted(df['country'].unique())}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return None
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None

def generate_country_year_pivot(df):
    try:
        # GROUP BY year,country,stars
        star_counts = df.groupby(['year', 'country', 'stars']).size().reset_index(name='count')
        
        # Crear Tabla
        pivot_table = star_counts.pivot_table(
            index=['year', 'country'], 
            columns='stars', 
            values='count', 
            fill_value=0
        ).reset_index()
        
        pivot_table.columns.name = None
        pivot_columns = ['year', 'country'] + [f'stars_{i}' for i in range(1, 6)]
        pivot_table.columns = pivot_columns
        
        # Guardar Tabla
        pivot_filename = "star_counts_by_country_year_pivot.csv"
        pivot_table.to_csv(pivot_filename, index=False)
        print(f"Generated: {pivot_filename}")
        
    except Exception as e:
        print(f"Error creating country-year pivot: {str(e)}")

def generate_topic_analysis(df, terms, cutoff_year):
    try:
        topic_records = []
        
        for _, row in df.iterrows():
            text_lower = str(row['text']).lower() if pd.notna(row['text']) else ""
            
            # Revisar temas
            found_topics = []
            for term in terms:
                if term.lower() in text_lower:
                    found_topics.append(term)
            
            if not found_topics:
                continue
                
            for topic in found_topics:
                topic_records.append({
                    'year': row['year'],
                    'country': row['country'],
                    'topic': topic,
                    'stars': row['stars']
                })
        
        if not topic_records:
            print("No records found containing the specified topics.")
            return
            
        # DataFrame
        topic_df = pd.DataFrame(topic_records)
        
        # GROUP BY year, country, topic,stars
        topic_counts = topic_df.groupby(['year', 'country', 'topic', 'stars']).size().reset_index(name='count')
        
        # Crear Tabla
        topic_pivot = topic_counts.pivot_table(
            index=['year', 'country', 'topic'], 
            columns='stars', 
            values='count', 
            fill_value=0
        ).reset_index()
        
        topic_pivot.columns.name = None
        topic_pivot_columns = ['year', 'country', 'topic'] + [f'stars_{i}' for i in range(1, 6)]
        topic_pivot.columns = topic_pivot_columns
        
        # Guardar Tabla
        topic_filename = "star_counts_by_country_year_topic_pivot.csv"
        topic_pivot.to_csv(topic_filename, index=False)
        print(f"Generated: {topic_filename}")
        print(f"Topic analysis records: {len(topic_pivot)}")
        
    except Exception as e:
        print(f"Error creating topic analysis: {str(e)}")

def clean_text_for_csv(text):
    if pd.isna(text):
        return ""
    
    text = str(text)
    
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\r\n', ' ')
    
    text = ' '.join(text.split())
    
    text = text.replace('\x00', '')
    
    return text

def generate_extreme_ratings(df):
    try:
        # Buscar sentimientos extremos
        extreme_df = df[df['stars'].isin([1, 5])].copy()
        
        extreme_df['title'] = extreme_df['title'].apply(clean_text_for_csv)
        extreme_df['text'] = extreme_df['text'].apply(clean_text_for_csv)
        
        extreme_df = extreme_df[['year', 'country', 'stars', 'title', 'id', 'text', 'url']]
        
        extreme_df = extreme_df.sort_values(['country', 'year', 'stars'])
        
        # Guardar CSV
        extreme_filename = "extreme_ratings_1_and_5_stars.csv"
        extreme_df.to_csv(
            extreme_filename, 
            index=False,
            quoting=1,
            escapechar='\\',
            encoding='utf-8'
        )
        print(f"Generated: {extreme_filename}")
        print(f"Extreme ratings records: {len(extreme_df)}")
        
        # Resumen
        summary = extreme_df.groupby(['country', 'stars']).size().reset_index(name='count')
        print(f"\nExtreme ratings summary:")
        print(summary.to_string(index=False))
        
    except Exception as e:
        print(f"Error creating extreme ratings file: {str(e)}")

def display_sample_results(filename, n=10):
    try:
        df = pd.read_csv(filename)
        print(f"\nFirst {n} rows of {filename}:")
        print(df.head(n).to_string(index=False))
    except Exception as e:
        print(f"Could not display sample from {filename}: {str(e)}")

if __name__ == "__main__":
    input_filename = "sentiment_analysis_results_clean.csv"
    cutoff_year = 2016  # Año Inicio
    
    print(f"Starting analysis with cutoff year: {cutoff_year}")
    print("="*50)
    
    generate_comprehensive_analysis(input_filename, cutoff_year)
    
    print("\n" + "="*50)
    print("Sample outputs:")
    
    display_sample_results("star_counts_by_country_year_pivot.csv", 5)
    display_sample_results("star_counts_by_country_year_topic_pivot.csv", 5)
    display_sample_results("extreme_ratings_1_and_5_stars.csv", 5)
