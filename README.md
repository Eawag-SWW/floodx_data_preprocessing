# floodx_data_preprocessing
Python script for preprocessing floodx data into uniform and readable format. Learn more about the project here: http://www.eawag.ch/en/department/sww/projects/floodx/.

## Dependencies
### Tesseract OCR
**tesseract-ocr** executable. Optical character recognition (OCR) is used to read sensor values from images. The **pytesseract** (https://pypi.python.org/pypi/pytesseract) package used requires that you install **tesseract-ocr**. The following Wiki for  **tesseract-ocr** provides useful information: https://github.com/tesseract-ocr/tesseract/wiki. You must be able to invoke the tesseract command as "tesseract". If this isn't the case, for example because tesseract isn't in your PATH, you will have to change the "tesseract_cmd" variable at the top of 'tesseract.py'.
### Python
**Python 2.7X** is recommended. We recommend installing the Anaconda package: https://www.continuum.io/downloads
### Python packages
The following Python packages are required:
 - **pandas** for working with time series
 - **os** for working with filesystem
 - **Image or PIL** for working with images
 - **pytesseract** is a Python wrapper for tesseract-ocr
 - **glob** for selecting files with wildcards
 - **csv** for writing csv files
 - **re** for using regular expressions
 - **datetime** for working with datetime stamps
 - **tkinter** for creating GUIs
  
## Executing the script
 - Make sure the dependencies mentioned above are installed. 
 - Download and extract the following packages from the Zenodo data repository:
  - `floodX Datasets` (doi: ...)
  - `floodX Datalogger Images` (doi: ...)
 - The `floodX Datasets` package contains the default version of this script in the `code` folder.
 - If you wish to update the files in the `code` folder, you can replace them with the files of this Github repository.
 - Open `settings.py`, and update the paths in `metadata/metadata_ocr.csv` to point to where you unpacked the `floodX Datalogger Images` package.
