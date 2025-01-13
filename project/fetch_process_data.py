import pandas as pd
import click



class Extract():
    def __init__(self) -> None:
        self.airbnb_df = pd.read_csv('airbnb_data/AB_US_2023.csv', low_memory=False)
        self.cities_df = pd.read_csv('uscities/uscities.csv', low_memory=False)
        self.is_data = False
        self.merged_df = pd.DataFrame()
        self.check_data()

    def get_airbnb_data(self) -> pd.DataFrame:
        return self.airbnb_df
    
    def get_cities_df(self) -> pd.DataFrame:
        return self.cities_df
    
    def check_data(self):
        if len(self.airbnb_df) > 0 and len(self.cities_df) > 0:
            self.is_data = True


class Transform():
    def __init__(self, airbnb, cities) -> None:
        self.airbnb_df = airbnb
        self.cities_df = cities
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

class load():
    def __init__(self, data):
        self.final_df = data

    def dump_data(self):
        click.secho(f"Saving final data...", bg='yellow')
        self.final_df.to_csv("Final_data.csv", index=False)

def main():
    EXTRACT = Extract()
    if EXTRACT.is_data:
        airbnb_data = EXTRACT.get_airbnb_data()
        cities_data = EXTRACT.get_cities_df()
        TRANSFORM = Transform(airbnb_data, cities_data)
        TRANSFORM.process()
        final_data = TRANSFORM.get_merged_data()
        LOAD = load(final_data)
        LOAD.dump_data()
    else:
        click.secho(f"No Data to Transform...", bg='red')

if __name__ == "__main__":
    main()