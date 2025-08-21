# EMG-Based Grasp Classification Analysis

## 1. Overview

This project focuses on the preprocessing and feature extraction of Electromyography (EMG) signals for the purpose of classifying different hand grasp movements. The primary goal is to transform raw, time-series EMG data from the NinaPro database into a structured feature set that can be used to train a machine learning model.

The analysis pipeline involves loading the raw data, filtering for specific grasp exercises, segmenting the continuous signal into individual repetitions, and extracting meaningful time-domain features from each repetition. The final output is a clean, feature-rich CSV file ready for classification tasks.

---

## 2. Dataset

* **Source:** The data is derived from the **NinaPro (Non-Invasive Adaptive Prosthetics) Database**, specifically DB2.
* **Exercises:** The analysis isolates two primary grasp movements along with the resting state:
    * **Large Grasp:** Stimulus label `18`
    * **Small Grasp:** Stimulus label `19`
    * **Rest:** Stimulus label `0`
* **Signal Type:** The data consists of 12-channel surface EMG signals recorded from the forearm.

---

## 3. Methodology

The analysis is conducted in a sequential pipeline, starting from raw data and ending with a feature matrix.

### 3.1. Data Preprocessing (`analysis_v1.ipynb`)

1.  **Loading:** Raw data is loaded from `.mat` files from the NinaPro DB2 directory.
2.  **Filtering:** A utility function (`filter_dataframe` from `filter_utils.py`) is used to filter the data, retaining only the samples corresponding to the large grasp, small grasp, and rest stimuli.
3.  **Trimming:** To remove irrelevant trailing data after the final exercise, the DataFrame is trimmed to a point 7000 samples beyond the last recorded stimulus.
4.  **Consolidation:** The processed data from multiple files is concatenated into a single DataFrame and saved as `large_small_grasp.csv`.

### 3.2. Segmentation & Feature Extraction (`grasp_analysis.ipynb`)

1.  **Segmentation:**
    * The `segment_repetitions` function, imported from `filter_utils.py`, identifies the start and end of each individual grasp repetition by monitoring changes in the 'stimulus' column (e.g., a transition from `0` to `18` marks the start of a large grasp).
    * This process resulted in **240 repetitions** for the large grasp and **240 repetitions** for the small grasp, creating a balanced dataset.

2.  **Feature Extraction:**
    * For each segmented repetition and for each of the 12 EMG channels, the `calculate_features` function (from `filter_utils.py`) computes four standard time-domain features:
        * **Root Mean Square (RMS):** Represents the signal's power and is related to muscle contraction force.
        * **Mean Absolute Value (MAV):** A measure of the signal's amplitude.
        * **Zero Crossings (ZC):** An indicator of the signal's frequency content.
        * **Wavelength (WL):** Measures the cumulative length of the signal waveform, indicating its complexity.

3.  **Feature Matrix Creation:**
    * The extracted features are organized into a final pandas DataFrame where each row corresponds to a single grasp trial, and the columns represent the 48 features (4 features x 12 channels).
    * A 'label' column is added to distinguish between 'large_grasp' and 'small_grasp'.
    * This final matrix is saved as `feature_df.csv`.

---

## 4. File Structure

* `analysis_v1.ipynb`: Jupyter Notebook for initial data loading, filtering, and consolidation.
* `grasp_analysis.ipynb`: Jupyter Notebook that uses utility functions to perform segmentation and feature extraction, creating the final feature matrix.
* `filter_utils.py`: Python script containing all helper functions for data filtering, signal segmentation, and feature calculation.
* `large_small_grasp.csv`: The consolidated, filtered raw EMG data.
* `feature_df.csv`: The final output containing the extracted features for each grasp trial, ready for model training.

---

## 5. How to Run

1.  **Dependencies:** Ensure you have the following Python libraries installed:
    ```
    pip install pandas numpy matplotlib scipy
    ```
2.  **Execution Order:**
    * First, run `analysis_v1.ipynb` to generate the `large_small_grasp.csv` file.
    * Then, run `grasp_analysis.ipynb` to perform the feature extraction and generate the `feature_df.csv` file.

---

## 6. Results

The analysis successfully processed the raw EMG signals into a structured dataset suitable for machine learning. The segmentation process yielded a balanced set of 240 trials for each grasp type.

The plot below visualizes the filtered EMG signal for several channels against the stimulus signal, confirming that the EMG amplitude correctly corresponds to the muscle activation periods.

![Filtered EMG Signals vs. Stimulus](https://i.imgur.com/uW2gY8A.png)

---

## 7. Future Work

The `feature_df.csv` file created in this analysis serves as the input for the next stage of the project: classification. Potential next steps include:

* **Model Training:** Train various machine learning classifiers (e.g., Support Vector Machine, Random Forest, Linear Discriminant Analysis) on the feature set.
* **Performance Evaluation:** Split the data into training and testing sets to evaluate the model's accuracy, precision, and recall in distinguishing between the two grasp types.
* **Feature Engineering:** Explore additional time-domain or frequency-domain features to potentially improve classification performance.
