import numpy as np
import seaborn as sns


def plot_daily_frame(data, col="", year_n=250):
    sns.set(rc={"figure.figsize": (12, 8)})
    # sns.set_style("white")
    if not col:
        col = data.columns[0]
    sets = data.index.get_level_values(0).unique()
    profit_max = data[col].max()
    profit_mean = data[col].mean()
    profit_std = data[col].std()
    year_rolling = data.rolling(year_n)[col].mean()
    for i, s in enumerate(sets):
        df_set = data.loc[s]
        df_set_mean = df_set[col].mean()
        df_set_std = df_set[col].std()
        p = sns.lineplot(data=df_set, style="white")
        p.plot(year_rolling.loc[s], color="black")
        p.axvline(df_set.index.max(), color="g")
        p.axhline(0, color="r")
        p.axhline(profit_mean, color="w")
        p.text(
                df_set.index[-1],
                profit_max,
                f"{s}\n\nmean:{df_set_mean: .05f}\nstd:{df_set_std: .05f}",
                ha="right",
                va="center",
                color="r",
            )
        if i == 0:
            p.set_title(f"mean: {profit_mean: 0.4f} std: {profit_std: 0.4f}")
            p.text(
                df_set.index[0],
                profit_mean,
                f"{profit_mean: .04f}",
                ha="right",
                va="center",
                color="b",
            )


def plot_daily_frame_cum(data, col="", year_n=250):
    sns.set(rc={"figure.figsize": (12, 8)})
    # sns.set_style("white")
    if not col:
        col = data.columns[0]
    sets = data.index.get_level_values(0).unique()
    data_ = data
    data = data.cumsum()
    profit_max = data[col].max()
    year_rolling = data.rolling(year_n)[col].mean()
    sets_mean_arr = []
    sets_std_arr = []
    for i, s in enumerate(sets):
        df_set = data.loc[s]
        df_set_ = data_.loc[s]
        df_set_mean = df_set_[col].cumsum().mean()
        df_set_std = df_set_[col].cumsum().std()
        sets_mean_arr.append(df_set_mean)
        sets_std_arr.append(df_set_std)
        p = sns.lineplot(data=df_set, style="white")
        p.plot(year_rolling.loc[s], color="black")
        p.axvline(df_set.index.max(), color="g")
        p.axhline(0, color="r")
        #p.axhline(df_set_mean, color="w")
        p.text(
                df_set.index[-1],
                profit_max,
                f"{s}\n\nmean:{df_set_mean: .05f}\nstd:{df_set_std: .05f}",
                ha="right",
                va="center",
                color="r",
            )
    
    profit_mean = np.mean(sets_mean_arr)
    profit_std = np.mean(sets_std_arr)
    p.set_title(f"mean: {profit_mean: 0.4f} std: {profit_std: 0.4f}")