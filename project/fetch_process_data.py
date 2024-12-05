import pandas as pd
import click

class MakeData():
    def __init__(self) -> None:
        self.airbnb_df = pd.read_csv('../data/airbnb_data/AB_US_2023.csv', low_memory=False)
        self.cities_df = pd.read_csv('../data/uscities/uscities.csv', low_memory=False)
        self.merged_df = pd.DataFrame()

    def clean_airbnb(self):
        click.secho(f"Cleaning airbnb data", bg='magenta')
        city_replacements = {
        'Twin Cities MSA': 'Minneapolis',
        'Washington D.C.': 'Washington',
        'New York City': 'New York',
        'Santa Clara County': 'Santa Clara',
        'Santa Cruz County' : 'Santa Cruz',
        'San Mateo County' : 'San Mateo',
        'Broward County' : 'Florida city',
        'Clark County' : 'Las Vegas'
        }
        try:
            self.airbnb_df['city'] = self.airbnb_df['city'].replace(city_replacements)
            self.airbnb_df = self.airbnb_df[["room_type", "price", "city"]]
            self.airbnb_df = pd.get_dummies(self.airbnb_df, dtype='int', columns=['room_type'], prefix=['room_type'])
            self.airbnb_df.dropna(inplace=True)
            click.secho(f"Task successful", bg='green')
        except Exception as e:
            click.secho(f"Failed processing airbnb data due to {e}", bg='red')

    def agg_airbnb(self):
        click.secho(f"Aggregating airbnb data", bg='magenta')
        self.airbnb_df = self.airbnb_df.groupby('city').agg(
        price_mean=('price', 'mean'),
        entire_home_apt_sum=('room_type_Entire home/apt', 'sum'),
        hotel_room_sum=('room_type_Hotel room', 'sum'),
        private_room_sum=('room_type_Private room', 'sum'),
        shared_room_sum=('room_type_Shared room', 'sum'),
        listing_count=('city', 'size')
        )
        self.airbnb_df = self.airbnb_df.reset_index(drop = False)
        click.secho(f"Task successful", bg='green')

    def clean_cities(self):
        click.secho(f"Cleaning cities data", bg='magenta')
        self.cities_df = self.cities_df[["population", "density", "city"]]
        self.cities_df.dropna(inplace = True)
        click.secho(f"Task successful", bg='green')

    def agg_cities(self):
        click.secho(f"Aggregating cities data", bg='magenta')
        self.cities_df = self.cities_df.loc[self.cities_df.groupby('city')['population'].idxmax()]
        self.cities_df = self.cities_df.reset_index(drop=True)
        click.secho(f"Task successful", bg='green')

    def merge_data(self):
        click.secho(f"Merging datas...", bg='magenta')
        try:
            self.merged_df = pd.merge(
                self.airbnb_df, 
                self.cities_df, 
                how='inner', 
                on=['city']
            )
            self.merged_df.dropna(inplace=True)
            click.secho(f"Task successful", bg='green')
        except Exception as e:
            click.secho(f"Failed in merging due to {e}", bg='red')

    def get_merged_data(self):
        return self.merged_df
    
    def process(self):
        self.clean_airbnb()
        self.agg_airbnb()
        self.clean_cities()
        self.agg_cities()
        self.merge_data()

def main():
    MAKE = MakeData()
    MAKE.process()
    data = MAKE.get_merged_data()
    data.to_csv("../data/Final_data.csv", index=False)

if __name__ == "__main__":
    main()