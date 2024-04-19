# ===============================================================================
# Created:        3 Feb 2023
# Updated:
# @author:        Quinlan Eddy
# Description:    Module for generic Python operations
# ===============================================================================


import os
import sys
import logging
import time
import argparse
import json

# === Clear Console ===
def clear_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# === Setup Logger ===
# Dynamically set logfile name based upon current date.
log_file_path = "./"
local_time = time.strftime("%Y%m%d", time.localtime())
log_file = f'{log_file_path}{local_time}-ANAPLAN-RUN.LOG'
log_file_level = logging.INFO  # Options: INFO, WARNING, DEBUG, INFO, ERROR, CRITICAL
logging.basicConfig(filename=log_file,
                    filemode='a',  # Append to Log
                    format='%(asctime)s  :  %(levelname)s  :  %(message)s',
                    level=log_file_level)
logging.info("************** Logger Started ****************")


# === Read in configuration ===
def read_configuration_settings():
    try:
        with open("./settings.json", "r") as settings_file:
            settings = json.load(settings_file)
        logging.info("Configuration read in successfully")
        return settings

    except:
        print("Unable to open the `settings.json` file. Please ensure the file is in the path of this Python module")
        # Exit with a non-zero exit code
        sys.exit(1)


# === Read CLI Arguments ===
def read_cli_arguments(arg_list: list[str] | None = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--auth_flow', action='store_true',
                        help="Use Authorization Code Grant flow")
    parser.add_argument('-r', '--register', action='store_true',
                        help="OAuth device registration")
    parser.add_argument('-c', '--client_id', action='store',
                        type=str, help="OAuth Client ID")
    parser.add_argument('-t', '--token_ttl', action='store',
                        type=str, help="Token time to live value in seconds")
    parser.add_argument('--code', action='store',
                        type=str, help='Authorization Code')
    parser.add_argument('--secret', action='store',
                        type=str, help='Client Secret')
    args = parser.parse_args(arg_list)
    return args
