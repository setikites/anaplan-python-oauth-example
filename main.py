# ===============================================================================
# Created:        2 Feb 2023
# Updated:
# @author:        Quinlan Eddy
# Description:    Main module for invocation of Anaplan operations
# ===============================================================================

import sys
import logging

import utils
import anaplan_oauth
import globals
import anaplan_ops


def main():
	
	# Clear the console
	utils.clear_console()

	# Enable logging
	logger = logging.getLogger(__name__)

	# Get configurations
	settings = utils.read_configuration_settings()

	# Get configurations from the CLI
	args = utils.read_cli_arguments()
	register = args.register

	# Set the client_id and token_ttl from the CLI arguments
	globals.Auth.client_id = args.client_id
	if args.token_ttl == "":
		globals.Auth.token_ttl = int(args.token_ttl)

	# Get the URIs from the settings
	device_id_uri = settings['get_device_id_uri']
	tokens_uri = settings['get_tokens_uri']


	# If register flag is set, then request the user to authenticate with Anaplan to create device code
	if register:
		logger.info(f'Registering the device with Client ID: {globals.Auth.client_id}')
		anaplan_oauth.get_device_id(device_id_uri)
		anaplan_oauth.get_tokens(tokens_uri)
		
	else:
		print('Skipping device registration and refreshing the access_token')
		logger.info('Skipping device registration and refreshing the access_token')
		anaplan_oauth.refresh_tokens(tokens_uri, 0)

	# Configure multithreading 
	t1_refresh_token = anaplan_oauth.refresh_token_thread(1, name="Refresh Token", delay=5, uri=tokens_uri)
	t2_get_workspaces = anaplan_ops.get_workspaces_thread(2, name="Get Workspaces", counter=3, delay=10)

	# Start new Threads
	t1_refresh_token.start()
	t2_get_workspaces.start()

	# Exit with return code 0
	sys.exit(0)


if __name__ == '__main__':
    main()
