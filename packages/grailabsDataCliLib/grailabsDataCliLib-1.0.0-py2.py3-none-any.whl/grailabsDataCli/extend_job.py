import os
import sys
sys.path.append(os.path.abspath(os.path.join('./grailabsDataCli')))
from scripts.jobBuilder import JobBuilder
import argparse
from colorama import Fore, Back, Style

def main():
    try:
        print()
        CLI_DESC = "This tool is needed to extened tasks for an existing job in grailabs-data.com\
      using a command line interface. To extend tasks means to add new data (new tasks)  \
      to an existing job. The CLI tool accepts name of the job to be extended and path to the data file to be added.\n\
      "
        eplilog = "Written by Daniel Zelalem Zewdie.\
    Contact danielzelalemheru@gmail.com"
        argParser = argparse.ArgumentParser(
            description=CLI_DESC, epilog=eplilog, prog="extend_job")
        argParser.add_argument('--name', required=True, type=str,
                               help="The name of the job to be extended, Required")

        argParser.add_argument('--src_data', required=True, type=str,
                               help="Path to a csv dataset to be added, Required")
       
        argParser.add_argument('--email', required=False, type=str,
                               help="Admin email address for grailabs-data account. Optional unless password arg is provided")

        argParser.add_argument('--password', required=False, type=str,
                               help="Admin password for grailabs-data account,  Optional unless email arg is provided")
        
        args = argParser.parse_args()
        name = args.name
        dataPath = args.src_data
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
        status, message = jc.addDataToJob(name, dataPath, email, password)
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
