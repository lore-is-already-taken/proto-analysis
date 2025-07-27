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
    print(last_nonzero_index)
    # Assuming 'filtered_df' is your DataFrame and 'last_nonzero_index' holds the index
    trimmed_df = filtered_df.loc[:last_nonzero_index + 7000].copy()
    return trimmed_df

def segment_repetitions(df, grasp_label):
    """Segments a time-series DataFrame into a list of individual repetitions.

    This function identifies periods of a specific activity based on a stimulus
    label. It works by finding the start of each repetition, defined as the
    point where the stimulus changes from a rest state (0) to the target
    grasp label, and its end, defined as the first subsequent return to the
    rest state.

    Args:
        df (pd.DataFrame): The input DataFrame containing time-series data and
                           a 'stimulus' column.
        grasp_label (int): The integer label in the 'stimulus' column that
                           identifies the specific grasp to be segmented.

    Returns:
        list: A list of pandas DataFrames, where each DataFrame contains the
              data for a single, complete repetition from start to end.
    """
    # Initialize a list to store each segmented repetition (as a DataFrame).
    repetitions = []

    # Identify the start of each grasp repetition. This is achieved by finding
    # all indices where the current stimulus equals the target `grasp_label` AND
    # the stimulus of the immediately preceding sample (`shift(1)`) was 0 (rest).
    # This robustly detects the "rising edge" of the stimulus event.
    start_indices = df[(df['stimulus'].shift(1) == 0) & (df['stimulus'] == grasp_label)].index

    # Iterate through each identified start index to find its corresponding end.
    for start in start_indices:
        # Find all potential end indices for the current repetition. An end is defined
        # as any point after the 'start' index where the stimulus returns to 0.
        end_index_series = df.index[(df.index > start) & (df['stimulus'] == 0)]

        # Ensure that at least one end index was found to avoid errors with
        # incomplete repetitions at the end of the recording.
        if not end_index_series.empty:
            # Select the *first* index where the stimulus returns to 0 as the
            # definitive end of this specific repetition.
            end = end_index_series[0]

            # Slice the DataFrame from the start to the end index (inclusive)
            # to create a DataFrame for this single repetition.
            repetition_df = df.loc[start:end]

            # Add the segmented repetition to the master list.
            repetitions.append(repetition_df)

    return repetitions

def calculate_features(window):
    """Computes a set of standard time-domain features for a given signal window.

    This function is designed to extract key characteristics from a segment of
    a time-series signal, such as an EMG recording. The calculated features
    are commonly used in pattern recognition and machine learning applications.

    Args:
        window (np.ndarray): A 1D NumPy array representing a single window
                             of signal data for one channel.

    Returns:
        dict: A dictionary where keys are the feature names (str) and
              values are their corresponding computed values (float or int).
              The features are:
              - 'rms': Root Mean Square
              - 'mav': Mean Absolute Value
              - 'zc':  Zero Crossing count
              - 'wl':  Waveform Length
    """
    features = {
        # Root Mean Square (RMS): A measure of the signal's power and amplitude.
        'rms': np.sqrt(np.mean(window**2)),

        # Mean Absolute Value (MAV): The average of the rectified signal,
        # providing a measure of its average amplitude.
        'mav': np.mean(np.abs(window)),

        # Zero Crossing (ZC): The number of times the signal crosses the
        # zero-axis. This is an indicator of the signal's frequency.
        # The product of adjacent samples will be negative if a zero-crossing occurred.
        'zc': ((window[:-1] * window[1:]) < 0).sum(),

        # Waveform Length (WL): The cumulative length of the waveform over the
        # time segment, indicating a measure of signal complexity.
        'wl': np.sum(np.abs(np.diff(window)))
    }
    return features

