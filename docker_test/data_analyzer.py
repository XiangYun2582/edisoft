import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer


def filter_unknown_results(ana_table: pd.DataFrame) -> pd.DataFrame:
    """
    過濾掉 result_type 為 'unknown' 的資料，並選取特定欄位。

    參數：
    - ana_table: 原始資料表 DataFrame

    回傳：
    - 篩選後的 DataFrame
    """
    df_filtered = ana_table[ana_table["result_type"] != "unknown"][
        [
            "company",
            "order_date",
            "order_month",
            "order_week",
            "cycle_3day",
            "cycle_4day",
            "cycle_5day",
            "win_count",
            "tie_count",
            "loss_count",
        ]
    ].copy()

    df_filtered = df_filtered.reset_index(drop=True)
    return df_filtered


def summarize_counts(df: pd.DataFrame, group_col: str = "order_date") -> pd.DataFrame:
    """
    依照 company 和 group_col 分組，加總 win/tie/loss 欄位，並計算 loss_rate。

    參數：
    - df: pandas DataFrame
    - group_col: 欲分組的欄位名稱，預設為 'order_date'

    回傳：
    - 分組統計後的 DataFrame（包含 loss_rate 欄位）
    """
    summary = (
        df.groupby(["company", group_col], observed=True)[
            ["win_count", "tie_count", "loss_count"]
        ]
        .sum()
        .reset_index()
    )

    summary["loss_rate"] = (
        summary["loss_count"]
        / (summary["win_count"] + summary["tie_count"] + summary["loss_count"])
    ).round(2)

    return summary


def plot_loss_rate(df, goal_col="order_date"):
    """
    根據指定的日期欄位，繪製多類別時間折線區域圖（不疊加），
    並設定背景與網格顏色。

    參數：
    - df: 已包含 'company', 'win_count', 'tie_count', 'loss_count' 等欄位的 DataFrame
    - goal_col: 要用來分組與繪圖的日期欄位名稱，預設為 'order_date'

    回傳：
    - Plotly Figure 物件
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    font_path = 'C:/Windows/Fonts/msjh.ttc'  # 微軟正黑體
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    """
    # 呼叫已定義的 summarize_counts 函數進行分組與加總
    df_summary = summarize_counts(df, group_col=goal_col)

    fig = px.line(
        df_summary,
        x=goal_col,
        y="loss_rate",
        color="company",
        title=f"多類別時間折線圖（不疊加區域圖），分組欄位：{goal_col}",
        labels={goal_col: "日期", "loss_rate": "loss_rate"},
    )

    for trace in fig.data:
        trace.update(fill="tozeroy")

    fig.update_layout(
        plot_bgcolor="whitesmoke",
        paper_bgcolor="white",
        xaxis=dict(gridcolor="white", zerolinecolor="lightgray"),
        yaxis=dict(gridcolor="white", zerolinecolor="lightgray"),
    )

    fig.show()
    return fig


def plot_result_type_distribution(df: pd.DataFrame) -> px.bar:
    """
    繪製每個 company 的 result_type（win/tie/loss）百分比堆疊圖（水平長條圖）。

    參數：
    - df: 包含 'company'、'result_type' 欄位的 DataFrame

    回傳：
    - Plotly 圖表物件
    """
    # 過濾與清理
    filtered = df[df["result_type"] != "unknown"].copy()
    filtered["result_type"] = filtered["result_type"].cat.remove_unused_categories()

    # 統計計數與百分比
    df_counts = (
        filtered.groupby(["company", "result_type"], observed=True)
        .size()
        .reset_index(name="count")
    )

    df_total = df_counts.groupby("company", observed=True)[
        "count"].transform("sum")

    df_counts["percent"] = df_counts["count"] / df_total * 100
    df_counts["text"] = (
        df_counts["percent"].round(2).astype(str)
        + "% ("
        + df_counts["count"].astype(str)
        + ")"
    )

    # 自訂色彩
    custom_color_map = {"win": "#F0A04B", "tie": "#B1C29E", "loss": "#FCE7C8"}

    # 繪圖
    fig = px.bar(
        df_counts,
        y="company",
        x="percent",
        color="result_type",
        title="每個 Company 各 Result Type 比例 (%)",
        labels={"percent": "百分比", "result_type": "比賽結果"},
        text="text",
        color_discrete_map=custom_color_map,
        orientation="h",
    )

    fig.update_traces(
        texttemplate="%{text}", textposition="inside", textfont_size=14, width=0.6
    )
    fig.update_layout(
        xaxis=dict(ticksuffix="%", range=[0, 100]),
        plot_bgcolor="whitesmoke",
        barmode="stack",
        bargap=0.3,
        bargroupgap=0.1,
    )
    fig.show()
    return fig


def plot_league_result_type_distribution(df: pd.DataFrame, top_n: int = 10) -> px.bar:
    """
    繪製前 N 個 league_name 的 result_type（win/tie/loss）堆疊圖。

    參數：
    - df: 包含 'league_name' 和 'result_type' 欄位的 DataFrame
    - top_n: 要顯示的前 N 個聯盟名稱，預設為 10

    回傳：
    - Plotly 圖表物件
    """

    # 過濾 unknown 並移除未使用類別
    filtered_df = df[df["result_type"] != "unknown"].copy()
    if isinstance(filtered_df["result_type"].dtype, pd.CategoricalDtype):
        filtered_df["result_type"] = filtered_df[
            "result_type"
        ].cat.remove_unused_categories()

    # 統計每個 league_name 各 result_type 的筆數
    df_counts = (
        filtered_df.groupby(["league_name", "result_type"], observed=True)
        .size()
        .reset_index(name="count")
    )

    # 計算每個 league 的總數，排序取前 N 名
    league_totals = (
        df_counts.groupby("league_name", observed=True)[
            "count"].sum().reset_index()
    )
    league_totals["count"] = pd.to_numeric(league_totals["count"])
    league_totals = league_totals.sort_values(by="count", ascending=False).reset_index(
        drop=True
    )

    top_leagues = league_totals.head(top_n)["league_name"].tolist()
    df_counts_top = df_counts[df_counts["league_name"].isin(
        top_leagues)].copy()

    # 顯示數字文字
    df_counts_top["text"] = df_counts_top["count"].astype(str)

    # 自訂顏色
    custom_color_map = {"win": "#F0A04B", "tie": "#B1C29E", "loss": "#FCE7C8"}

    # 繪製長條圖
    fig = px.bar(
        df_counts_top,
        y="league_name",
        x="count",
        color="result_type",
        title=f"前 {top_n} 個 League 各 Result Type 計數",
        labels={"count": "計數", "result_type": "比賽結果"},
        text="text",
        color_discrete_map=custom_color_map,
        orientation="h",
    )

    fig.update_traces(
        texttemplate="%{text}", textposition="inside", textfont_size=14, width=0.6
    )
    fig.update_layout(
        xaxis=dict(range=[0, df_counts_top["count"].max() * 1.1]),
        plot_bgcolor="whitesmoke",
        barmode="stack",
        bargap=0.3,
        bargroupgap=0.1,
    )

    fig.show()
    return fig


def compute_similarity_matrices(df: pd.DataFrame, company_col: str, league_col: str):
    """
    計算每家公司在指定 league_col 上的相似度，包括：
    - Cosine Similarity
    - Jaccard Index
    - 交集次數 (Intersection Count)

    參數：
    - df: 包含公司與聯盟欄位的 DataFrame
    - company_col: 公司欄位名稱（如 'company'）
    - league_col: 聯盟欄位名稱（如 'league_name'）

    回傳：
    - jac_df: Jaccard Index 相似度矩陣 DataFrame
    - cos_df: Cosine Similarity 相似度矩陣 DataFrame
    - inter_df: 交集個數矩陣 DataFrame
    """

    # 對每家公司彙總其聯盟列表
    grouped = df.groupby(company_col)[league_col].apply(list).reset_index()

    # One-hot 編碼
    mlb = MultiLabelBinarizer()
    league_matrix = mlb.fit_transform(grouped[league_col])

    # Cosine 相似度
    # pivot table：公司 × 聯盟，值是 sponsor_count sum
    pivot = df.pivot_table(
        index="company",
        columns="league_name",
        values="sponsor_count",
        aggfunc="sum",
        fill_value=0,
    )

    # 顯示公司對聯盟的加總向量
    # print("Sponsor count pivot table:")
    # print(pivot)

    # 計算 Cosine Similarity 函數
    def cosine_similarity_manual(vec1, vec2):
        dot = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    # 計算所有公司兩兩間的 cosine similarity 矩陣
    companies = pivot.index.tolist()
    vectors = pivot.values

    n = len(vectors)
    cos_sim_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            cos_sim_matrix[i, j] = cosine_similarity_manual(
                vectors[i], vectors[j])

    # Jaccard Index 與 Intersection Count
    n = league_matrix.shape[0]
    jac_sim = np.zeros((n, n))
    inter_count = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            u, v = league_matrix[i], league_matrix[j]
            inter = np.logical_and(u, v).sum()
            union = np.logical_or(u, v).sum()
            jac_sim[i, j] = inter / union if union != 0 else 0
            inter_count[i, j] = inter

    company_ids = grouped[company_col].values

    jac_df = pd.DataFrame(jac_sim, index=company_ids, columns=company_ids)
    cos_df = pd.DataFrame(cos_sim_matrix, index=companies, columns=companies)
    inter_df = pd.DataFrame(
        inter_count, index=company_ids, columns=company_ids)

    return jac_df, cos_df, inter_df


# 測試區塊（非必要，可保留也可移除）
if __name__ == "__main__":
    from data_clean import load_ana_table, load_sponsor_view

    ana_table = load_ana_table()
    sponsor_table = load_sponsor_view()

    if ana_table is not None:
        filtered = filter_unknown_results(ana_table)
        # summary = summarize_counts(filtered, group_col="order_date")
        # print(summary.head())
        # plot_loss_rate(filtered, goal_col="cycle_4day")
        plot_result_type_distribution(ana_table)
        # plot_league_result_type_distribution(ana_table, top_n=10)
    else:
        print("讀取 ana_table 失敗")

    if sponsor_table is not None:
        jac_df, cos_df, inter_df = compute_similarity_matrices(
            sponsor_table, "company", "league_name"
        )
        # 顯示結果
        # print("🔹 Jaccard Index Matrix:")
        # print(jac_df.round(2))

        # print("\n🔹 Cosine Similarity Matrix:")
        # print(cos_df.round(2))

        # print("\n🔹 Common league_name Count Matrix:")
        # print(inter_df.astype(int))

    else:
        print("讀取 sponsor_table 失敗")
