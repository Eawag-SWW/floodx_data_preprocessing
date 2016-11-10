import settings as s
import SettingReader
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import os
import glob
import csv
import re
import pandas as pd


def extract_data(datasource):
    # overall image directory
    working_dir = os.path.join(s.input['raw_sorted_data_dir'], datasource['directory'])
    output_dir = s.proc['ocr_results_path']

    # regex for checking values
    regex = re.compile(datasource['validation_expression'])
    def validate_val(text):
        return regex.match(text)

    # date parser function
    date_parser = lambda date: pd.datetime.strptime(date.strip(), datasource['datetime_format'])


    for image_dir in os.listdir(working_dir):

        if not os.path.isdir(os.path.join(working_dir, image_dir)):
            continue

        dir_name = os.path.basename(image_dir)

        print dir_name

        settings_displays = SettingReader.SettingReader(os.path.join(
            working_dir,
            image_dir,
            '_displays.ini'))

        # Create a file for each display contained
        for displayID in settings_displays.values:
            # File to write in
            file_name = settings_displays.values[displayID]['sensor'] +\
                        "@" + dir_name + '.' + s.proc['ocr_results_extension']
            settings_displays.values[displayID]['file'] = open(
                os.path.join(
                    output_dir,
                    file_name),
                'wb')
            # CSV writer function
            settings_displays.values[displayID]['writer'] = csv.writer(
                settings_displays.values[displayID]['file'],
                delimiter=s.proc['ocr_results_separator'])
            # Write header
            settings_displays.values[displayID]['writer'].writerow(
                [s.proc['ocr_results_datecol'],
                 s.proc['ocr_results_valcol'],
                 s.proc['ocr_results_sensorcol']])

        # loop through pictures
        # select for images
        count = 0
        for fn in glob.glob(os.path.join(working_dir, image_dir, '*.jpg')):
            # for testing
            count += 1
            if count > 10:
                break

            if os.path.isfile(fn):
                # For each text section in image, extract information
                for displayID in settings_displays.values:
                    original = Image.open(fn)
                    cropped = original.crop((
                        int(settings_displays.values[displayID]['left']),
                        int(settings_displays.values[displayID]['top']),
                        int(settings_displays.values[displayID]['right']),
                        int(settings_displays.values[displayID]['bottom'])
                    ))
                    rotated = cropped.rotate(float(settings_displays.values[displayID]['rotation']), expand=True)
                    grayscale = rotated.convert('L')
                    # extract value from image
                    ocr_value = pytesseract.image_to_string(
                        grayscale,
                        lang=datasource['language'],
                        # config="-psm 7 -l digital")
                        config="-psm 7 --tessdata-dir tesseract_training/digital -l digital")
                    # get datetime
                    datetime_raw, extension = os.path.splitext(os.path.basename(fn))
                    # write text to csv file
                    if validate_val(ocr_value):
                        settings_displays.values[displayID]['writer'].writerow(
                            [date_parser(datetime_raw).strftime(s.proc['ocr_results_date_format']),
                             ocr_value,
                             settings_displays.values[displayID]['sensor']])

                    # grayscale.save(os.path.join(output_dir, 'images', datetime+settings_displays.values[displayID]['sensor']+'.jpg'))

        # Close all files
        for displayID in settings_displays.values:
            settings_displays.values[displayID]['file'].close()
