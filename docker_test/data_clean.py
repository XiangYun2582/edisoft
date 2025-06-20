from data_reader import query_table
import pandas as pd


def load_ana_table():

    ana_table = query_table("ana_table")
    if ana_table is None:
        return None

    categorical_cols = [
        "company",
        "is_live",
        "score_type",
        "market_type",
        "choice",
        "league_name",
        "home_team",
        "away_team",
        "line_type",
        "result_type",
    ]
    ana_table[categorical_cols] = ana_table[categorical_cols].astype("category")
    ana_table["order_date"] = pd.to_datetime(ana_table["order_date"], format="%Y-%m-%d")

    numeric_cols = ["line", "price", "exec_stake", "real_win_loss", "real_price"]
    for col in numeric_cols:
        ana_table[col] = pd.to_numeric(ana_table[col], errors="coerce")

    return ana_table


def load_sponsor_view():

    sponsor_table = query_table("sponsor_view")
    if sponsor_table is None:
        return None

    return sponsor_table


if __name__ == "__main__":
    ana_data = load_ana_table()
    sponsor_data = load_sponsor_view()

    if ana_data is not None:
        print("[ana_table]")
        print(ana_data.head())

    if sponsor_data is not None:
        print("[sponsor_view]")
        print(sponsor_data.head())
