import os
import sys
sys.path.append(os.path.abspath(os.path.join('./grailabsDataCli/scripts')))
from datetime import datetime
from pathlib import Path
from .authHandler import AuthHandler
from .apiHandler import ApiHandler
from .descriptionVerifier import DescriptionVerifier, ValueError, ValueNotDefined, ValueTypeError, JobExeception
from .apiHandler import ApiException, AccessDeniedException



class AutomationClient:
    def __init__(self, BASE_PATH="http://localhost:8000"
                 ):
        self.basePath = BASE_PATH
        self.authHandler = AuthHandler(self.basePath)
        self.apiHandler = ApiHandler(self.basePath)

    def getCredentials(self):
        print("Admin credentials is required")
        email = input("Email: ")
        password = input("Password: ")
        return email, password

    def verifyFilePath(self, value, label) -> bool:
        if not value:
            raise ValueNotDefined(label)
        if type(value) != str or not value.strip():
            raise ValueError(label, value, "String")
        path = Path(value)
        if path and path.is_file():
            return True
        else:
            raise ValueError(f"{label}is not a valid path")

    def scheduleNewJobAutomation(self, sec_interval: float, descPath: str, srcDataPath: str,
                                 email=None, password=None):
        _email, _password = self.getCredentials()
        status, message = self.authHandler.authenticate(
            _email, _password, rememberToken=False)
        if (not status):
            return False, message
        if (not descPath):
            return False, "Path to job description json file is requierd!"
        if (not srcDataPath):
            return False, "Path to csv dataset ('src_data'), that holds the tasks (data) is required"
        if not sec_interval:
            return False, "Duration interval expressed in seconds is required for the automation"

        try:
            self.verifyFilePath(descPath, "Description json file ('desc')")
            self.verifyFilePath(srcDataPath, "Dataset ('src_data')")
            try:
                sec_interval = eval(str(sec_interval))
                if (sec_interval < 0):
                    return False, "Duration interval should be a postive number"
            except Exception as e:
                return False, "Duration interval should be a postive number"

            try:
                result = self.apiHandler.scheduleNewJobAutomation(
                    _email, _password, sec_interval, srcDataPath, descPath)
                return True, result['message']
            except ApiException as e:
                return False, e.message

        except JobExeception as e:
            return False, e.message

    def stopJobCreation(self, name: str, email=None, password=None):
        _email, _password = self.getCredentials()
        status, message = self.authHandler.authenticate(
            _email, _password, rememberToken=False)
        if (not status):
            return False, message
    
        try:
            try:
                result = self.apiHandler.stopJobCreationAutomation(name)
                return True, result['message']
            except ApiException as e:
                return False, e.message

        except JobExeception as e:
            return False, e.message

    def rescheduleJobCreation(self, name: str, sec_interval: float, email=None, password=None):
        _email, _password = self.getCredentials()
        status, message = self.authHandler.authenticate(
            _email, _password, rememberToken=False)
        if (not status):
              return False, message
        
        try:
            sec_interval = eval(str(sec_interval))
            if (sec_interval < 0):
                return False, "Duration interval should be a postive number"
        except Exception as e:
            return False, "Duration interval should be a postive number"

        try:
            try:
                result = self.apiHandler.rescheduleJobCreationAutomation(name, sec_interval)
                return True, result['message']
            except ApiException as e:
                return False, e.message

        except JobExeception as e:
            return False, e.message
