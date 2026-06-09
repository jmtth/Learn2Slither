import pandas as pd


class MyStats:

    def __init__(self, path="scores.csv"):
        self.path = path
        self.df = self.load(path)

    def load(self, path: str) -> pd.DataFrame:
        """Load a CSV file from the specified path
        and return it as a pandas DataFrame.
        If the path is not a string, the file is not found,
        the file is not a valid CSV, or the file is empty,
        and an empty DataFrame is returned."""
        if not isinstance(path, str):
            print("Error: the path should be a string.")
            return pd.DataFrame()
        try:
            data = pd.read_csv(path)
        except FileNotFoundError:
            print("Error: the file is not found.")
            return pd.DataFrame()
        except UnicodeDecodeError:
            print("Error: the file is not a valid CSV.")
            return pd.DataFrame()
        if data.empty:
            print("Error: the file is empty.")
            return pd.DataFrame()
        return data

    def get_sessions_stat(self):
        max_length = self.df[self.df["Player"] == "Agent"]["Length"].max()
        return max_length
