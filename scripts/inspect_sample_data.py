import pandas as pd

FILE_PATH = "data/sample/sample_auction_lots.csv"


def load_sample_data():
    return pd.read_csv(FILE_PATH)


def print_dataset_summary(df):
    print("File loaded successfully")
    print("------------------------")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumn names:")
    for column in df.columns:
        print(f"- {column}")

    print("\nFirst 3 rows:")
    print(df.head(3))


def main():
    df = load_sample_data()
    print_dataset_summary(df)


if __name__ == "__main__":
    main()