import settings as s
import process_ocr
import process_csv
import pandas as pd
import os
# The script launches the following actions
# - OCR data stored in images
# - Process into readable csv files

def main():
    # Check that input paths are ok.
    for path in [
        s.input['raw_sorted_data_dir'],
        s.input['sensor_metadata_path'],
        s.input['ocr_metadata_path']
    ]:
        if not os.path.exists(path):
            print "CRITICAL: %s not found. Stopping script." % path
            exit()

    # Check that output paths are ok. Create directories if missing
    for path in [
        s.proc['ocr_results_path'],
        os.path.join(s.output['data_dir'], 'csv'),
        os.path.join(s.output['data_dir'], 'json')
    ]:
        if not os.path.exists(path):
            print "INFO: %s not found. Creating directory." % path
            os.makedirs(path)

    # PROCESS IMAGES WITH OCR
    if s.proc['do_ocr']:
        print '## DOING OCR ##'
        datasources = pd.read_csv(
            filepath_or_buffer=s.input['ocr_metadata_path'],
            sep=s.input['separator']
        )
        for index, datasource in datasources.iterrows():
            # print '- OCR for %s' % datasource['']
            if datasource['do_ocr']:
                process_ocr.extract_data(datasource)

    # raw_input("Please make sure the metadata file \n"
    #           "  %s\nis updated (and saved!) so that the OCR results can be found \n"
    #           "  Enter to continue..." % s.input['sensor_metadata_path'])

    # PROCESS TO CSV
    print '## FORMATTING DATA ##'
    process_csv.start_gui()

    print 'Done. Find results in %s' % s.output['data_dir']

main()
