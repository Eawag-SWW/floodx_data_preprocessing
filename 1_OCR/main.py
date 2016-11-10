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
# import cv2
# import numpy as np
from matplotlib import pyplot as plt

# read settings. No file passed implies default settings
# settings_general = SettingReader.SettingReader('settings_mid_161006_2015.ini')


# overall image directory
# working_dir = "Q:/Abteilungsprojekte/eng/SWWData/Matthew/PhD_DATA/core_2016_floodX/6_Data/2_Sorted/m1&m2&m3_h_p_waterpilot/test"
# output_dir = "Q:/Abteilungsprojekte/eng/SWWData/Matthew/PhD_DATA/core_2016_floodX/6_Data/2_Sorted/m1&m2&m3_h_p_waterpilot/logitech_c920_data"
working_dir = "Q:/Abteilungsprojekte/eng/SWWData/Matthew/PhD_DATA/core_2016_floodX/6_Data/2_Sorted/p1_q_mid_promag/logitech_c920_grouped"
output_dir = "Q:/Abteilungsprojekte/eng/SWWData/Matthew/PhD_DATA/core_2016_floodX/6_Data/2_Sorted/p1_q_mid_promag/logitech_c920_data"

# regex for checking values
regex = re.compile(r'^[+-]\d?\d?\d\.\d\d$')  # For MID
# regex = re.compile(r'^[0-9][0-9][0-9][0-9]$')  # For pressure
def validate_val(text):
    return regex.match(text)


# make directory to save ocr'd data
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


for image_dir in os.listdir(working_dir):

    if not os.path.isdir(os.path.join(working_dir, image_dir)):
        continue

    dir_name = os.path.basename(image_dir)

    print dir_name

    settings_displays = SettingReader.SettingReader(os.path.join(
        working_dir,
        image_dir,
        '_displays.ini'))
    # crop and naming settings

    # left = int(settings_displays.values['1']['left'])
    # top = int(settings_displays.values['1']['top'])
    # right = int(settings_displays.values['1']['right'])
    # bottom = int(settings_displays.values['1']['bottom'])
    # angle = float(settings_displays.values['1']['rotation'])

    # loop through pictures
    # select for images
    with open(os.path.join(output_dir, dir_name + '.txt'), 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        # write header
        writer.writerow(['datetime', 'value', 'sensor'])
        for fn in glob.glob(os.path.join(working_dir, image_dir, '*.jpg')):
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
                    # convert to opencv image for thresholding
                    # open_cv_image = np.array(grayscale)
                    # blur = cv2.GaussianBlur(img, (5, 5), 0)
                    # ret3, thresh_cv2 = cv2.threshold(open_cv_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    # convert back to pil format
                    # thresh_pil = Image.fromarray(thresh_cv2)
                    #
                    # get datetime
                    datetime, extension = os.path.splitext(os.path.basename(fn))
                    # datetime = datetime.split('_', 1)[1]  # required for MID
                    text = pytesseract.image_to_string(
                        grayscale,
                        lang='eng',
                        # config="-psm 7 -l digital ocrconfig")
                        config="-psm 7 --tessdata-dir tesseract_training/digital -l digital ocrconfig")  # for MID
                    # print text
                    if validate_val(text):
                        writer.writerow([datetime, text, settings_displays.values[displayID]['sensor']])

                    # grayscale.save(os.path.join(output_dir, 'images', datetime+settings_displays.values[displayID]['sensor']+'.jpg'))

