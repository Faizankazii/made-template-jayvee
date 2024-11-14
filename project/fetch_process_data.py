import os
import requests
import zipfile
import pandas as pd
from io import BytesIO
import click

def download_and_extract(url, extract_to):
    click.secho(f"Downloading {url}...", bg='magenta')
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            z.extractall(extract_to)
        click.secho(f"Extracted contents of {url} to {extract_to}.", bg='green')
    else:
        click.secho(f"Failed to download {url} with status code {response.status_code}.", bg='red')
        exit(1)

def transform_csv(file_path, file):
    try:
        click.secho(f"Processing {file_path}...", bg='magenta')
        df = pd.read_csv(file_path, low_memory=False)
        df.dropna(inplace=True)
        df.to_csv(f"../data/cleaned_{file}", index=False)
        os.remove(file_path)
        click.secho(f"Transformed data saved to cleaned_{file}", bg='green')
    except Exception as e:
        click.secho(f"Error processing {file_path}: {e}", bg='red')

def merge_datas(df_paths):
    if len(df_paths) == 2:
        df_cities = pd.read_csv(df_paths[0])
        df_airbnb = pd.read_csv(df_paths[1])
        merged_df = pd.merge(df_airbnb, df_cities, how='inner', left_on='neighbourhood', right_on='city')
        merged_df = merged_df.drop(columns=['neighbourhood', 'id_x', 'id_y'])
        merged_df.to_csv('../data/merged_data.csv', index=False)
    else:
        click.secho(f"Cleaned data path length not two! Exiting...", bg='red')
        exit(1)

def main():
    data_links = [
        "https://shorturl.at/JCGL2",
        "https://simplemaps.com/static/data/us-cities/1.79/basic/simplemaps_uscities_basicv1.79.zip"
    ]
    data_dir = "../data"
    clean_df_path = []
    for url in data_links:
        download_and_extract(url, data_dir)
    for file in os.listdir(data_dir):
        print(file) #uscities.csv
        if file.endswith(".csv"):
            file_path = os.path.join(data_dir, f"{file}")
            print(file_path)   #../data/uscities.csv
            clean_df_path.append(f"../data/cleaned_{file}")
            transform_csv(file_path, file)
        else:
            file_path = os.path.join(data_dir, file)
            os.remove(file_path)
    if len(clean_df_path) == 2:
        merge_datas(clean_df_path)

if __name__ == "__main__":
    main()
