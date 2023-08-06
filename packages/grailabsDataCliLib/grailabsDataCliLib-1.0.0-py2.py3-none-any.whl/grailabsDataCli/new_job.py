import sys
import os
sys.path.append(os.path.abspath(os.path.join('./grailabsDataCli')))
from scripts.jobBuilder import JobBuilder
import argparse
from colorama import Fore, Back, Style

def main():
    try:
        print()
        CLI_DESC = "This tool is needed to create a new job in grailabs-data.com\
      using a command line interface.  the CLI tool accepts a job description file for creating new job.\n\
      "
        eplilog = "Written by Daniel Zelalem Zewdie.\
    Contact danielzelalemheru@gmail.com"
        argParser = argparse.ArgumentParser(
            description=CLI_DESC, epilog=eplilog, prog="create_job")
        argParser.add_argument('--desc', required=True, type=str,
                               help="The path to the job description file, Required")

        argParser.add_argument('--email', required=False, type=str,
                               help="Admin email address for grailabs-data account. Optional unless password arg is provided")
        argParser.add_argument('--password', required=False, type=str,
                               help="Admin password for grailabs-data account,  Optional unless email arg is provided")

        args = argParser.parse_args()
        desc_path = args.desc
        email = args.email
        password = args.password
        if (email):
            if not password:
                print(
                    "--email is provided the following arguments are required: --password")
                sys.exit(0)
        if (password):
            if not email:
                print(
                    "--password is provided the following arguments are required: --email")
                sys.exit(0)

        jc = JobBuilder()
        status, message = jc.createJob(desc_path, email, password)
        if (not status):
            logColor = Fore.RED
            prefix = "FAIL"
        else:
            logColor = Fore.GREEN
            prefix = "SUCCESS"
        print(logColor + f"{prefix}: {message}", logColor)
        print("Opreation finished!")
        print()

    except KeyboardInterrupt as e:
        print("Opreation interrupted")
