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

    def get_sessions_stat(self, player="Agent") -> tuple[int, int]:
        max_length = self.df[self.df["Player"] == player]["Length"].max()
        max_moves = self.df[self.df["Player"] == player]["Moves"].max()
        return max_length, max_moves

    def get_top_scores(self) -> list[tuple[str, int, int, int]]:
        """ Returns the top 17 scores sorted by length (descending)
        and moves (ascending).

        returns:
            pd.DataFrame: A List containing the top 17 scores with columns
            "Player", "Moves", "Length", "Green Apples".
        """
        df_filtered = self.df[["Player", "Moves", "Length", "Green Apples"]]
        df_sorted = df_filtered.sort_values(
            by=["Length", "Moves"], ascending=[False, True])
        top17 = df_sorted.head(17)
        return [tuple(row) for row in top17.values]

    def get_player_count(self) -> int:
        """Returns the number of unique players in the stats."""
        return self.df["Player"].nunique()

    def get_game_count(self) -> int:
        """Returns the total number of games recorded in the stats."""
        return len(self.df)
