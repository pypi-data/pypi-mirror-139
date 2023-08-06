#!/bin/bash
import os
import sys
sys.path.append(os.path.abspath(os.path.join('./grailabsDataCli/scripts')))
from .apiHandler import ApiException
from .apiHandler import ApiHandler
import pickle




class AuthHandler:

    def __init__(self, base, BASE_PATH="http://localhost:4000"
                 ):
        self.apiHandler = ApiHandler(BASE_PATH)
        pass

    def isAuthenticated(self):
        authTokenObj = self.getTokenObj()
        if (not authTokenObj):
            return False
        try:
            if (not authTokenObj['auth-token']):
                return False
            return True
        except KeyError as e:
            return False
        return False

    def getTokenObj(self, fileName: str = 'tokCache'):
        try:
            with open(f"../.{fileName}.pkl", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None

    def saveToken(self, token: str, fileName: str = 'tokCache'):
        with open(f"../.{fileName}.pkl", "wb") as f:
            pickle.dump({"auth-token": token}, f)

    def authenticate(self, email, password, rememberToken=True):
        try:
            res = self.apiHandler.loginAsAdmin(email, password)
            token = res['token']
            if (token and rememberToken):
                self.saveToken(token)
            return True, token
        except ApiException as e:
            return False, e.message


if __name__ == "__main__":
    ah = AuthHandler()
    email = "danielzelalemheru@gmail.com"
    password = "Abc123.."
    # print(ah.authenticate(email, password))
    print("val ", ah.isAuthenticated())
    print("val ", ah.getTokenObj())
