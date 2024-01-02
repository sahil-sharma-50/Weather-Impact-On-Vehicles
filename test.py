import os
import pandas as pd
import data_pipeline


# Test Data Extraction for both Accident and Weather data:
def test_data_extraction(accident_path, weather_url):
    accidents_df = data_pipeline.load_accident_df(accident_path)
    assert not accidents_df.empty, "Accident Data Extraction Failed"
    print("Accident Data Extraction: Test Passed")

    weather_df = data_pipeline.load_weather_df(weather_url)
    assert not weather_df.empty, "Weather Data Extraction Failed"
    print("Weather Data Extraction: Test Passed")


# Test Data Preprocess for both Accident data:
def preprocess_accidents(accidents_df, column_names, months_mapping, road_conditions_mapping):
    accidents_df.rename(columns=column_names, inplace=True)
    accidents_df['month'] = accidents_df['month'].map(months_mapping)
    accidents_df['road condition'] = accidents_df['road condition'].replace(road_conditions_mapping)
    return accidents_df


def test_preprocessing():
    # Test data for accidents
    test_accidents = pd.DataFrame({
        'UMONAT': [1, 2, 3],
        'IstRad': [0, 1, 0],
        'IstPKW': [1, 0, 1],
        'IstFuss': [0, 1, 0],
        'IstKrad': [0, 0, 1],
        'IstGkfz': [1, 1, 0],
        'USTRZUSTAND': ['0', '1', '2']
    })

    # Test data for weather
    test_weather = pd.DataFrame({
        'Month': ["Jan", "Feb", "Mar"],
        'Precision': [10.5, 20.0, 15.5],
        'AirPressure': [1010, 1005, 1020],
        'SunshineDuration': [5.0, 6.5, 4.0]
    })

    # Preprocess test accident data
    processed_accident_df = preprocess_accidents(
        test_accidents, column_names=columns_rename,
        months_mapping=months_rename, road_conditions_mapping=road_conditions_rename
    )

    columns_for_merging = ["month", "bicycle", "car", "pedestrian", "motorbike", "truck", "road condition"]
    assert not processed_accident_df.empty, "Accident Data Preprocessing Failed"
    print("Accident Data Preprocessing: Test Passed")

    merged_df = data_pipeline.merge_data(processed_accident_df[columns_for_merging], test_weather)
    assert not merged_df.empty, "Data Merging Failed"
    print("Data Merging: Test Passed")


# Test Save Dataset after Extraction and Transformation:
def test_saved_file():
    data_pipeline.main()
    assert os.path.isfile('data/processed_database.sqlite'), "Output database file does not exist."
    print("Data Saved: Test Passed")


if __name__ == "__main__":
    accident_data_path = 'data/accident_data.csv'
    weather_data_url = 'https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/monthly'
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

    test_data_extraction(accident_data_path, weather_data_url)
    test_preprocessing()
    test_saved_file()
