import pandas as pd
import sqlite3
import os


def load_accident_df(accident):
    accident = pd.read_csv(accident, delimiter=';', encoding='ISO-8859-1')
    return accident


def fetch_monthly_data(weather, data_type, prefix):
    month_dict = {}
    for i in range(12):
        if i < 9:
            url = f'{weather}/{data_type}/{prefix}_0{i + 1}.txt'
        else:
            url = f'{weather}/{data_type}/{prefix}_{i + 1}.txt'

        dataset = pd.read_csv(url, sep=';', skiprows=0, header=1)
        filtered_data = dataset[dataset['Jahr'] == 2019]
        month_dict.update(dict(zip(filtered_data['Monat'].tolist(), filtered_data['Brandenburg/Berlin'].tolist())))
    return month_dict


def load_weather_df(weather):
    # Fetch data for each type
    month_precision_dict = fetch_monthly_data(weather, 'precipitation', 'regional_averages_rr')
    month_airpressure_dict = fetch_monthly_data(weather, 'air_temperature_mean', 'regional_averages_tm')
    month_sunshine_dict = fetch_monthly_data(weather, 'sunshine_duration', 'regional_averages_sd')

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    weather = pd.DataFrame({
        'Month': months,
        'Precision': list(month_precision_dict.values()),
        'AirPressure': list(month_airpressure_dict.values()),
        'SunshineDuration': list(month_sunshine_dict.values())
    })
    weather['Month'] = pd.Categorical(weather['Month'], categories=months, ordered=True)
    return weather


def preprocess_accidents(accidents_raw_df, drop_columns, column_names, months_mapping, road_conditions_mapping, condition_value):
    accidents_df = accidents_raw_df.drop(columns=drop_columns)
    accidents_df.rename(columns=column_names, inplace=True)
    accidents_df['month'] = accidents_df['month'].map(months_mapping)
    accidents_df[['month', 'road condition']] = accidents_df[['month','road condition']].astype(str)
    accidents_df['road condition'] = accidents_df['road condition'].replace(road_conditions_mapping)
    accidents_df.drop(index=accidents_df[accidents_df['road condition'] == condition_value].index, inplace=True)
    return accidents_df


def merge_data(accidents_df, weather_df):
    final_df = pd.merge(accidents_df, weather_df, left_on='month', right_on='Month', how='left')
    df = final_df.drop(columns=['Month'])
    # Order the 'month' column
    months_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df['month'] = pd.Categorical(df['month'], categories=months_order, ordered=True)
    return df


def save_to_sqlite(data_df, table_name, db_path='../data/processed_database.sqlite'):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        data_df.to_sql(table_name, conn, index=False, if_exists='replace')


def main():
    accidents = load_accident_df('../data/accident_data.csv')
    weather_df = load_weather_df('https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/monthly')
    drop_columns = ['LAND', 'LOR', 'UJAHR', 'XGCSWGS84', 'YGCSWGS84', 'BEZ', 'OBJECTID', 'STRASSE',
                    'USTUNDE', 'UWOCHENTAG', 'UKATEGORIE', 'UART', 'UTYP1', 'ULICHTVERH', 'IstSonstige','LINREFX','LINREFY']
    columns_rename = {
        'UMONAT': 'month',
        'IstRad': 'bicycle',
        'IstPKW': 'car',
        'IstFuss': 'pedestrian',
        'IstKrad': 'motorbike',
        'IstGkfz': 'truck',
        'USTRZUSTAND': 'road condition'
    }
    months_rename = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }
    road_conditions_rename = {'0': 'dry', '1': 'wet', '2': 'icy'}
    accidents_df = preprocess_accidents(accidents, drop_columns, columns_rename, months_rename, road_conditions_rename, 'Hellersdorfer Promenade')
    final_df = merge_data(accidents_df, weather_df)
    save_to_sqlite(final_df, 'final_data_table')


if __name__ == "__main__":
    main()
