# INSTRUCTIONS


import os

# -- INPUT DATA -- #
input = dict(
    # Raw sorted data directory
    raw_data_dir="../data_raw",

    # Metadata directory
    metadata_dir="../metadata",

    # Datalogger image directory (the one containing m1&m2&m3_h_p_endress_logi and p1_q_mid_endress_logi data)
    datalogger_image_dir="../../floodX Datalogger Images",

    # separator for datasource_files files
    separator=";",

)

# Update paths for metadata files
input['sensor_list_path'] = os.path.join(input['metadata_dir'], "datasource_list.csv")
input['datasource_files_path'] = os.path.join(input['metadata_dir'], "datasource_files.csv")
input['ocr_datasource_files_path'] = os.path.join(input['metadata_dir'], "datasource_files_ocr.csv")
input['experiment_list_path'] = os.path.join(input['metadata_dir'], "experiment_list.csv")


# -- PROCESSING SETTINGS -- #
proc = dict(
    # Do ocr or not?
    do_ocr=False,  #True,
    save_ocr_crops=False,

    # Temporary OCR results
    ocr_results_path="../data_ocr_result",  # Only change this if you know what you are doing!
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
    export_selection="all_data",
    # export_selection="experiments_good",  # Options are "experiments_good", "experiments_extended",
                                          # and "all_data" (see experiment_list.csv in datasource_files)

    # Directory for storing preprocessed data
    data_dir="../data_preprocessed",

    # Date format for output files
    date_format="%d/%m/%Y %H:%M:%S",

    # Separator  for output files
    separator=";",

    # Extension for output files
    extension="txt",

    # Write json files that can be imported into CrateDB?
    write_crateDB=True
)
