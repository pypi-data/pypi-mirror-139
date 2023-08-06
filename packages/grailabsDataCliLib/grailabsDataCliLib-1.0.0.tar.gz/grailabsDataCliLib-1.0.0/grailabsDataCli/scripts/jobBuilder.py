import os
import sys
sys.path.append(os.path.abspath(os.path.join('./grailabsDataCli/scripts')))
import json
from .apiHandler import ApiException, AccessDeniedException, JobCreationException
from .descriptionVerifier import DescriptionVerifier, ValueError, ValueNotDefined, ValueTypeError, JobExeception
from .apiHandler import ApiHandler
from .authHandler import AuthHandler
from pathlib import Path
from datetime import datetime




class JobBuilder:
    def __init__(self, BasePath="http://localhost:4000"):
        self.basePath = BasePath
        self.authHandler = AuthHandler(self.basePath)
        self.apiHandler = ApiHandler(self.basePath)

    def getCredentials(self):
        print("Admin credentials is required")
        email = input("Email: ")
        password = input("Password: ")
        return email, password

    def verifyFilePath(self, value) -> bool:
        if not value:
            raise ValueNotDefined("Dataset path ('src_data')")
        if type(value) != str or not value.strip():
            raise ValueError("Dataset path ('src_data')", value, "String")
        path = Path(value)
        if path and path.is_file():
            return True
        else:
            raise ValueError("Dataset path ('src_data') is not a valid path")

    def addDataToJob(self, name: str, dataPath: str, email=None, password=None, trail=1):
        credentialProvided = email != None and password != None
        if credentialProvided:
            status, message = self.authHandler.authenticate(
                email, password, rememberToken=False)
            if (not status):
                return False, message
            authToken = message
        elif not self.authHandler.isAuthenticated():
            _email, _password = self.getCredentials()
            status, message = self.authHandler.authenticate(_email, _password)
            if (not status):
                return False, message
            authToken = message
        else:
            authToken = self.authHandler.getTokenObj()['auth-token']

        if (not name):
            return False, "Name of the job is required"
        try:
            self.verifyFilePath(dataPath)
            try:
                result = self.apiHandler.extendJob(authToken, name, dataPath)
                return True, result['message']
            except AccessDeniedException as e:
                if (trail == 1 and not credentialProvided):
                    email, password = self.getCredentials()
                    status, message = self.authHandler.authenticate(
                        email, password)
                    if (not status):
                        return False, message
                    return self.addDataToJob(name, dataPath, trail=0)
                else:
                    return False, e.message

            except ApiException as e:
                return False, e.message

        except JobExeception as e:
            return False, e.message

    def createJob(self, desc_path, email=None, password=None, trail=1, automation=False):
        descJobDescHandler = DescriptionVerifier(
            desc_path, readFromSrcDataDefualtLocation=automation)
        credentialProvided = email != None and password != None
        if credentialProvided:
            status, message = self.authHandler.authenticate(
                email, password, rememberToken=False)
            if (not status):
                return False, message
            authToken = message
        elif not self.authHandler.isAuthenticated():
            _email, _password = self.getCredentials()
            status, message = self.authHandler.authenticate(_email, _password)
            if (not status):
                return False, message
            authToken = message
        else:
            authToken = self.authHandler.getTokenObj()['auth-token']

        jobDataObj = descJobDescHandler.getDescConfig()
        if automation:
            timstamp = datetime.timestamp(datetime.now())
            timstampStr = str(timstamp).replace(".", "_")
            jobDataObj.data['name'] = jobDataObj.data['name'] + \
                "_" + timstampStr
        if jobDataObj.verfied:
            try:
                return True, self.apiHandler.createJob(
                    jobDataObj.data, authToken)['message']
            except AccessDeniedException as e:
                if (trail == 1 and not credentialProvided):
                    email, password = self.getCredentials()
                    status, message = self.authHandler.authenticate(
                        email, password)
                    if (not status):
                        return False, message
                    return self.createJob(desc_path, trail=0)
                else:
                    return False, e.message

            except ApiException as e:
                return False, e.message

        else:
            return False, jobDataObj.message


if __name__ == "__main__":
    jd = JobCreator("../job-desc-files/desc.json")
    print(jd.createJob())
