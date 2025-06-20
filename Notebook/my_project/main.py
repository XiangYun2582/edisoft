from data_clean import load_ana_table, load_sponsor_view
from data_analyzer import (
    filter_unknown_results,
    summarize_counts,
    plot_loss_rate,
    plot_result_type_distribution,
    plot_league_result_type_distribution,
    compute_similarity_matrices,
)


def main():
    print("啟動資料處理流程...")

    # 讀取資料
    ana_table = load_ana_table()
    sponsor_table = load_sponsor_view()

    if ana_table is not None:
        print("成功讀取 ana_table")
        filtered = filter_unknown_results(ana_table)

        # 統計與視覺化（可依需求調整）
        summary = summarize_counts(filtered, group_col="order_date")
        print("\n勝負統計摘要（依日期）:")
        print(summary.head())

        plot_loss_rate(filtered, goal_col="cycle_4day")
        plot_result_type_distribution(ana_table)
        plot_league_result_type_distribution(ana_table, top_n=10)
    else:
        print("無法讀取 ana_table")

    if sponsor_table is not None:
        print("\n成功讀取 sponsor_table，開始計算相似度矩陣...")
        jac_df, cos_df, inter_df = compute_similarity_matrices(
            sponsor_table, "company", "league_name"
        )

        print("Jaccard 相似度矩陣：")
        print(jac_df.round(2))

        print("\nCosine 相似度矩陣：")
        print(cos_df.round(2))

        print("\n共同聯盟數矩陣：")
        print(inter_df.astype(int))
    else:
        print("無法讀取 sponsor_table")


if __name__ == "__main__":
    main()
