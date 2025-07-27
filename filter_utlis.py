import pandas as pd


def filter_dataframe(data, exercises):
    emg_signal = pd.DataFrame(data["emg"])
    stimulus_signal = pd.DataFrame(data["stimulus"])
    subject = pd.DataFrame(data["subject"])

    df = pd.DataFrame(emg_signal)
    df["stimulus"] = stimulus_signal
    df["subject"] = subject

    trimmed_df = filter_exercise(df,exercises)
    return trimmed_df


def filter_exercise(df, exercises):
    filtered_df = df[df["stimulus"].isin(exercises)].copy()
    last_nonzero_index = filtered_df[filtered_df["stimulus"] != 0].index[-1]
    # Assuming 'filtered_df' is your DataFrame and 'last_nonzero_index' holds the index
    trimmed_df = filtered_df.loc[: last_nonzero_index + 7000].copy()
    return trimmed_df

