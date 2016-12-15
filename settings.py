# INSTRUCTIONS


import os

# -- INPUT DATA -- #
input = dict(
    # Raw sorted data directory
    raw_data_dir="../data_raw",

    # Metadata directory
    metadata_dir="../metadata",

    # Datalogger image directory (the one containing m1&m2&m3_h_p_waterpilot_logi and p1_q_mid_promag_logi)
    datalogger_image_dir="PATH_TO_FLOODX_DATALOGGER_IMAGES",

    # separator for metadata files
    separator=";",

)

# Update paths for metadata
input['sensor_list_path'] = os.path.join(input['metadata_dir'], "sensor_list.csv")
input['sensor_metadata_path'] = os.path.join(input['metadata_dir'], "metadata.csv")
input['ocr_metadata_path'] = os.path.join(input['metadata_dir'], "metadata_OCR.csv")
input['experiment_list_path'] = os.path.join(input['metadata_dir'], "experiment_list.csv")


# -- PROCESSING SETTINGS -- #
proc = dict(
    # Do ocr or not?
    do_ocr=False,
    save_ocr_crops=False,

    # Temporary OCR results
    ocr_results_path=os.path.join("../data_ocr_result_new"),  # Only change this if you know what you are doing!
    ocr_results_date_format="%d.%m.%Y %H:%M:%S",
    ocr_results_extension="txt",
    ocr_results_valcol="value",
    ocr_results_datecol="datetime",
    ocr_results_sensorcol="sensor",
    ocr_results_separator=";"
)

# -- OUTPUT SETTINGS -- #
output = dict(

    # What experiments should be exported
    export_selection="experiments_good",  # Other options are "experiments_extended"
                                          # and "all_data" (see experiment_list.csv in metadata)

    # Directory for storing preprocessed data
    data_dir="../data_preprocessed",

    # Date format for output files
    date_format="%d/%m/%Y %H:%M:%S",

    # Separator  for output files
    separator=";",

    # Extension for output files
    extension="txt",

    # Write CrateDB json files?
    write_crateDB=True
)
