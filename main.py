# ===============================================================================
# Created:        2 Feb 2023
# Updated:        30 Jan 2024
# @author:        Quinlan Eddy
# Description:    Main module for invocation of Anaplan operations
# ===============================================================================

import sys
import logging

import utils
import anaplan_oauth
import globals
import anaplan_ops
import threading


def main():
        
        # Clear the console
        utils.clear_console()

        # Enable logging
        logger = logging.getLogger(__name__)

        # Get configurations & set variables
        settings = utils.read_configuration_settings()
        oauth_service_uri = settings["uris"]["oauthService"]
        auth_code_uri = settings["uris"]["authenticationCode"]
        database = settings["database"]
        rotatable_token = settings["rotatableToken"]

        # Get configurations from the CLI
        args = utils.read_cli_arguments()
        register = args.register

        # Set the client_id and token_ttl from the CLI arguments
        globals.Auth.client_id = args.client_id
        if args.token_ttl == "":
                globals.Auth.token_ttl = int(args.token_ttl)
        globals.Auth.authorization_code = args.code
        globals.Auth.secret = args.secret

        if not args.auth_flow:
                # DEVICE AUTHORIZATION CODE GRANT FLOW
                # If register flag is set, then request the user to authenticate with Anaplan to create device code
                if register:
                        logger.info(f'Registering the device with Client ID: {globals.Auth.client_id}')
                        anaplan_oauth.get_device_id(uri=f'{oauth_service_uri}/device/code')
                        anaplan_oauth.get_tokens(uri=f'{oauth_service_uri}/token', database=database)
                
                else:
                        print('Skipping device registration and refreshing the access_token')
                        logger.info('Skipping device registration and refreshing the access_token')
                        anaplan_oauth.refresh_tokens(uri=f'{oauth_service_uri}/token', database=database, delay=0, rotatable_token=rotatable_token)

        else:
                # AUTHORIZATION CODE FLOW
                if args.client_id and not args.code:
                        logger.info(f'Obtain Authenticaion Code for Client ID: {globals.Auth.client_id}')
                        anaplan_oauth.get_auth_code(auth_code_uri)
                elif args.code and args.secret:
                        logger.info ('Getting an authorization token using Authorization Code Flow')
                        anaplan_oauth.get_auth_tokens(uri=f'{oauth_service_uri}/token', database=database)
                elif args.secret:
                        logger.info('Skipping device registration and refreshing the access_token')
                        anaplan_oauth.refresh_auth_tokens(uri=f'{oauth_service_uri}/token', database=database, delay=0)
                else:
                        print ("""For Authentication code provide:
Step 1: Client ID (optional Secret) required to fetch code
Step 2: Code and Secret are required to fetch tokens
Step 3: Secret must be supplied to refresh tokens
""")
                        logger.info ('Invalid Authorization Code request')
                        sys.exit(0)

                t2_get_workspaces = anaplan_ops.get_workspaces_thread(2, name="Get Workspaces", counter=3, delay=10)
                t2_get_workspaces.start()

                # Exit with return code 0
                sys.exit(0)


        # Configure multithreading 
        t1_refresh_token = anaplan_oauth.refresh_token_thread(1, name="Refresh Token", delay=5, uri=f'{oauth_service_uri}/token', database=database, rotatable_token=settings["rotatableToken"])
        t2_get_workspaces = anaplan_ops.get_workspaces_thread(2, name="Get Workspaces", counter=3, delay=10)

        # Start new Threads
        t1_refresh_token.start()
        t2_get_workspaces.start()

        # Exit with return code 0
        sys.exit(0)


if __name__ == '__main__':
    main()
