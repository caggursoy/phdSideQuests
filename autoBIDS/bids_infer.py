import os
import json
import pydicom
from collections import defaultdict

def extract_series_info(dicom_dir):
    series_info = defaultdict(list)
    for root, _, files in os.walk(dicom_dir):
        for file in files:
            if file.endswith('.IMA'):
                dicom_path = os.path.join(root, file)
                try:
                    dicom = pydicom.dcmread(dicom_path)
                    series_desc = dicom.SeriesDescription
                    series_info[series_desc].append(dicom_path)
                except Exception as e:
                    print(f"Could not read {dicom_path}: {e}")
    return series_info

def infer_bids_mapping(series_info):
    config = {"descriptions": []}
    for series_desc in series_info:
        if "T1" in series_desc:
            data_type = "anat"
            modality_label = "T1w"
            custom_labels = "acq-mprage"
        elif "Rest" in series_desc or "rest" in series_desc:
            data_type = "func"
            modality_label = "bold"
            custom_labels = "task-rest"
        else:
            # Add more rules as needed
            continue

        config["descriptions"].append({
            "dataType": data_type,
            "modalityLabel": modality_label,
            "customLabels": custom_labels,
            "criteria": {
                "SeriesDescription": series_desc
            }
        })
    return config

def write_config_file(config, output_path):
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=4)

def main(dicom_dir, output_path):
    series_info = extract_series_info(dicom_dir)
    config = infer_bids_mapping(series_info)
    write_config_file(config, output_path)

# Define paths
dicom_dir = '/zi/flstorage/group_klips/data/data/fMRI_workgroup/data/RAWDATA/TEST_SEMINAR_HD/'
config_output_path = 'config.json'

# Run the script
main(dicom_dir, config_output_path)
