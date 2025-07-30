# MAD2-SM
Repositorio para proyecto de la Unidad 2 de Minería y Aprendizaje de Datos. Proyecto sobre el análisis de noticias de salud mental.

Este repositorio incluye el código necesario para recrear los gráficos y tablas utlizadas, además de instrucciones para utilizar el código.

# Instrucciones
- Todos los archivos referidos a continuación se encuentran en la carpeta CODIGO de este repositorio.
- Para correr todos estos códigos, se usó el entorno contenido en "saludmental-gpu.yml". Se puede importar este entorno para ejecutar el código.
- Descargar datos de [Sophia Search](https://search.sophia2.org). Las columnas requeridas por el código son: date, text, title, country, url.
- Para este trabajo se utilizó el siguiente seach string: "salud mental" OR "depresión" OR "ansiedad" OR "suicidio" OR "estrés" OR "psiquiatría" OR "psicología" OR "trastorno mental" OR "enfermedad mental".
- Por limitaciones de Sophia Search, puede ser dificilt descargar muchos datos simultaneamente. Es posible subdividirlos en multiples descargas y unirlos con el "combine_csvs.py" incluido en el repositorio.
- Una vez se tengan las noticias en un archivo, se puede utilizar en notebook "MAD2-BERT.ipynb" para realizar en análisis de sentimiento y generar el archivo "sentiment_analysis_results_clean.csv" que contiene los resultados de este análisis.
- Como un paso intermedio, se utiliza un simple script "star_country_year.py" para generar CSVs resumen con la cantidad de estrellas por país, año y tema.
- Posteriormente se utiliza el notebook "graphs.ipynb" para generar los gráficos y resumenes de datos utilizados en el informe. Notar que para generar los gráficos de proporción de noticias, el notebook requiere también del archivo "news_counts_by_country.csv" que contiene el numero total de noticias por país y año disponibles en Sophia Search (a partir del 2016).

# Ejemplos
- En la carpeta EJEMPLOS se puede encontrar ejemplos de la ejecución de ambos notebooks, guardados en formato HTML. Esto permite ver el código con los resultados de ejecución sin necesidad de ejecutar el código personalmente.
