#!/run/current-system/sw/bin/bash
# A script to download the NinaPro DB1 preprocessed dataset (s1.zip to s27.zip)

# The base URL for the files
BASE_URL="https://ninapro.hevs.ch/files/DB2_Preproc/"

# The directory where files will be saved
OUTPUT_DIR="ninapro_db2_data"

# Create the output directory if it doesn't exist
echo "Creating directory: $OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

echo "--- Starting Download ---"

# Loop from 1 to 27 to download each file
# DB2_s1.zip
for i in {1..40}; do
    # Construct the full filename and URL
    FILENAME="DB2_s${i}.zip"
    FULL_URL="${BASE_URL}${FILENAME}"

    # Print which file is being downloaded
    echo "Downloading: $FILENAME"

    # Use wget to download the file into the specified directory
    # -q: quiet mode (less output)
    # --show-progress: shows a clean progress bar
    # -P: specifies the directory to save files to
    wget -q --show-progress -P "$OUTPUT_DIR" "$FULL_URL"
done

echo "--- Download Complete ---"
echo "All files have been saved to the '$OUTPUT_DIR' directory."
