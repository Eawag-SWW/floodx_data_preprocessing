from crate import client
import glob
import os
import subprocess
import dbconfig

# This script was tested with the following configuration:
# Local machine: Windows 7
# Remote machine: Ubuntu 16.04.1 LTS (GNU/Linux 4.4.0-59-generic x86_64)
# Database on remote machine: CrateDB 1.0.2

# the following table was created on the remote machine:
# CRATE TABLE
# create table floodx (
#   sensor string,
#   datetime timestamp,
#   value double,
#   primary key (sensor, datetime)
# );

input_data_dir = ""



def main():

    print 'starting...'

    # print 'deleting old data from remote machine'
    # subprocess.call(["ssh", dbconfig.username+"@"+dbconfig.address, "rmdir", "somedir" ]) # NOT WORKING YET
    
    print 'copying data to remote machine'
    subprocess.call(["pscp", "-pw", dbconfig.password, os.path.join(input_data_dir, "*"), dbconfig.username+"@"+dbconfig.address+":"+dbconfig.data_dir])

    print 'loading data into database'
    crate_host = dbconfig.address + ":" + dbconfig.port
    connection = client.connect(crate_host, error_trace=True)

    print 'connected.'

    for fn in glob.glob(os.path.join(input_data_dir, '*.json')):
        sensor_name, extension = os.path.splitext(os.path.basename(fn))
        print 'Uploading', sensor_name
        copy_file(connection=connection, file_name=dbconfig.data_dir + "/" + sensor_name+extension)

    connection.close()

    print 'done.'


def copy_file(connection, file_name):
    cursor = connection.cursor()
    sql_command = 'COPY floodx FROM \'%s\' with (overwrite_duplicates = TRUE)' % file_name
    print sql_command
    cursor.execute(sql=sql_command)
    cursor.close()

main()
