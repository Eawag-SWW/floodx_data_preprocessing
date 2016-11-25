# This script manages the pre-processing of floodX data to make it easily readable, by humans and machines
#
# Steps:
#  - read settings
#  - read sensor list
#  - for each sensor, check if output file was already generated
#  - only reprocess the data if the overwrite setting is set to True
#  - for reprocessing a sensor X's data
#    - find all data sources for sensor X
#    - create a temporary table T in which to store data
#    - for each data source, read the data into T, at the same time reformatting datetime and nodata
#    - shift the data to realign
#    - sort the table by datetime
#    - write the table as a csv


# PACKAGES
import pandas as pd
import os
import glob
import re
import datetime
import settings as s


def process():
    # READ LIST OF SENSORS
    sensorlist = pd.read_csv(
        filepath_or_buffer=s.input['sensor_list_path'],
        sep=s.input['separator']
    )

    # READ METADATA
    metadata = pd.read_csv(
        filepath_or_buffer=s.input['sensor_metadata_path'],
        sep=s.input['separator'],
        keep_default_na=False
    )

    # LOOP THROUGH SENSORS
    # only sensors for which status is 'ok'
    for index, row in sensorlist.iterrows():

        current_sensor = row['device code']

        # check if metadata is ok
        if row['metadata'] == 'ok':

            output_file_csv = os.path.join(s.output['data_dir'], 'csv', current_sensor + '.txt')
            output_file_json_temp = os.path.join(s.output['data_dir'], 'json', current_sensor + '.json_temp')
            output_file_json = os.path.join(s.output['data_dir'], 'json', current_sensor + '.json')

            # check if csv data was already processed
            if os.path.isfile(output_file_csv):
                if s.proc['overwrite_csv']:
                    os.remove(output_file_csv)
                else:
                    continue

            print current_sensor
            # # check if json data was already processed
            # if os.path.isfile(output_file_json):
            #     if settings['overwrite'] == True:
            #         os.remove(output_file_json)
            #     else:
            #         continue

            # create temporary table
            temp_dataframe = pd.DataFrame({
                'datetime': [],
                'value': []
            })

            # find datasources
            datasources = metadata[metadata['sensor'] == current_sensor]
            if len(datasources.index) == 0:
                print 'WARNING: No rows in metadata found'
            for index2, datasource in datasources.iterrows():
                print '  ' + datasource['filename_pattern']
                newdata = read_csv_to_dataframe(datasource)
                temp_dataframe = pd.concat([temp_dataframe, newdata])

            # SORT THE DATAFRAME BY DATETIME
            temp_dataframe.sort_values(by='datetime', ascending=True)

            # ADD COLUMN WITH SENSOR NAME
            temp_dataframe['sensor'] = current_sensor

            # SAVE TO CSV
            temp_dataframe.to_csv(
                path_or_buf=output_file_csv,
                sep=';',
                index=False
            )

            if s.output['write_crateDB']:
                # SAVE TO JSON
                temp_dataframe.to_json(
                    path_or_buf=output_file_json_temp,
                    orient='records'
                )

                # Change JSON format to match https://crate.io/docs/reference/sql/reference/copy_from.html
                with open(output_file_json, "wt") as fout:
                    with open(output_file_json_temp, "rt") as fin:
                        for line in fin:
                            fout.write(line.replace('[', '').replace(']', '').replace('},{', '}\n{'))

                # Delete temporary JSON
                os.remove(output_file_json_temp)


def read_csv_to_dataframe(datasource):
    # read csv(s) into temporary table
    temp_dataframe = pd.DataFrame({
        'datetime': [],
        'value': []
    })

    # list of matching files
    files = glob.glob(os.path.join(s.input['raw_sorted_data_dir'], datasource['filename_pattern']))

    datetime_col_names = filter(bool, [
        datasource['date_col'],
        datasource['time_col'],
        datasource['datetime_col']
    ])

    if len(files) == 0:
        print 'WARNING: No files found that match metadata pattern'

    # for each file, load data into dataframe
    for fn in files:

        # read data into temp
        temp = pd.read_csv(
            sep=datasource['separator'],
            filepath_or_buffer=fn,
            usecols=datetime_col_names + [datasource['data_col']],
            parse_dates={'dt': datetime_col_names},  # list of lists --> combine columns
            date_parser=lambda date: pd.datetime.strptime(date.strip(), datasource['datetime_format']),
            na_values=datasource['nodata_vals'].split(),
            engine='python'
        )
        # rename columns
        temp.columns = ['datetime', 'value']

        # drop lines with na
        temp = temp.dropna()

        # Remove data greater than maximum value
        if not datasource['max_valid_value'] == '':
            temp = temp[temp.value <= float(datasource['max_valid_value'])]

        # Apply floor value when relevant (e.g. replace anything below 3 with 3)
        if not datasource['floor_value'] == '':
            temp.loc[temp.value < datasource['floor_value'], 'value'] = datasource['floor_value']

        # For ultrasonic sensors that contain raw values, use ground level to compute water level
        if not datasource['ground_level'] == '':
            temp.value = float(datasource['ground_level']) - temp.value

        # SHIFT TIME
        # the minus sign is important
        temp['datetime'] = temp['datetime'] - parse_timedelta(datasource['time_shift'])

        # concatenate it to dataframe
        temp_dataframe = pd.concat([temp_dataframe, temp])

    return temp_dataframe


def parse_timedelta(time_str):
    regex = re.compile(r'(?P<sign>[-]?)(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)')
    parts = regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    parts = {
        'hours': parts['sign'] + parts['hours'],
        'minutes': parts['sign'] + parts['minutes'],
        'seconds': parts['sign'] + parts['seconds']
    }
    time_params = {}
    for (name, param) in parts.iteritems():
        if param:
            time_params[name] = int(param)
    return datetime.timedelta(**time_params)
