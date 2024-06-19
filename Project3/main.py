import pandas as pd
import os

if __name__ == "__main__":
    current_directory = os.path.dirname(__file__)
    data_directory = os.path.join(current_directory, "data")

    for file in os.listdir(data_directory):
        file_path = os.path.join(data_directory, file)

        data = pd.read_csv(file_path)

        columns = data.columns
        for column in columns:
            unique_values_with_percentage = data[column].value_counts(normalize=True)
            unique_values_with_percentage = unique_values_with_percentage.to_dict()
            unique_values_with_percentage = {
                key: f"{value:.2%}"
                for key, value in unique_values_with_percentage.items()
            }
            print(f"Column: {column}")
            print(f"Unique values:")
            if len(unique_values_with_percentage.keys()) > 20:
                print(len(unique_values_with_percentage.keys()))
                print(
                    min(unique_values_with_percentage.keys()),
                    max(unique_values_with_percentage.keys()),
                )
            else:
                for key, value in unique_values_with_percentage.items():
                    print(f"{key}: {value}")
