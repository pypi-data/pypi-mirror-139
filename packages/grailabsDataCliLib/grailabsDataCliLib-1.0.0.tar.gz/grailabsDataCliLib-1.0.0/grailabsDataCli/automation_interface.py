import sys
import os
sys.path.append(os.path.abspath(os.path.join('./grailabsDataCli')))
from scripts.automationClient import AutomationClient
import argparse
from colorama import Fore, Back, Style


def createJobInterface():
    try:
        print()
        CLI_DESC = "This is an automation interfcae for communicating with grailabs-data automation service.\
           This tool is used to  for automating new job creation."
        eplilog = "Written by Daniel Zelalem Zewdie.\
    Contact danielzelalemheru@gmail.com"
        argParser = argparse.ArgumentParser(
                description=CLI_DESC, epilog=eplilog, prog="automate")

        
        argParser.add_argument('--desc', required=True, type=str,
                                help="The path to the job description file, Required")
        argParser.add_argument('--src_data', required=True, type=str,
                                help="The path to the source csv dataset, Required")
        argParser.add_argument('--sec_interval', required=True, type=float,
                                help="The Job excution intervals expressed in number of seconds")
        args = argParser.parse_args()

        args = argParser.parse_args()
        desc_path = args.desc
        src_data = args.src_data
        sec_interval = args.sec_interval

        ac = AutomationClient()
       
        status, message = ac.scheduleNewJobAutomation(
            sec_interval, desc_path, src_data)

        # todo actual automation
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


def stopJobCreationInterface():
    try:
        print()
        CLI_DESC = "This is an automation interfcae for communicating with grailabs-data automation service.\
           This tool is used to stop a scheduled job creation opreation."
        eplilog = "Written by Daniel Zelalem Zewdie.\
    Contact danielzelalemheru@gmail.com"
        argParser = argparse.ArgumentParser(
            description=CLI_DESC, epilog=eplilog, prog="automate")

        argParser.add_argument('--name', required=True, type=str,
                               help="The prefix name of the job that is scheduled for job creation, Required")

        args = argParser.parse_args()
        name = args.name

        ac = AutomationClient()

        status, message = ac.stopJobCreation(name)   
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


def rescheduleJobCreationInterface():
    try:
        print()
        CLI_DESC = "This is an automation interfcae for communicating with grailabs-data automation service.\
           This tool is used to reschedule a scheduled job creation opreation."
        eplilog = "Written by Daniel Zelalem Zewdie.\
    Contact danielzelalemheru@gmail.com"
        argParser = argparse.ArgumentParser(
            description=CLI_DESC, epilog=eplilog, prog="automate")

        argParser.add_argument('--name', required=True, type=str,
                               help="The prefix name of the job that is scheduled for job creation, Required")
        
        argParser.add_argument('--sec_interval', required=True, type=float,
                               help="The prefix name of the job that is scheduled for job creation, Required")


        args = argParser.parse_args()
        name = args.name
        sec_interval = args.sec_interval

        ac = AutomationClient()

        status, message = ac.rescheduleJobCreation(name, sec_interval)
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
