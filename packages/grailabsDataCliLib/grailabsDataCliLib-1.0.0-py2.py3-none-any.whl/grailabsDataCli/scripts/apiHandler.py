import requests
import json


class ApiException(Exception):
    pass


class AuthFailedException(ApiException):
    def __init__(self, message="Incorrect email or password"):
        self.message = message
        super().__init__(self.message)


class JobCreationException(ApiException):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class JobCreationSchedulingException(ApiException):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class AccessDeniedException(ApiException):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class NetWorkException(ApiException):
    def __init__(self, message="Network error"):
        self.message = message
        super().__init__(self.message)


class ApiHandler:
    def __init__(self, basePath: str):
        self.basePath = basePath

    def loginAsAdmin(self, email, password, endpoint="/auth/login"):
        payload = {'email': email, 'password': password}
        api_call = self.basePath + endpoint
        try:
            response = requests.post(api_call, json=payload)
            ret = response.json()
            if (not ret['success']):
                raise AuthFailedException(ret['message'])
            return {'message': ret['message'], 'token': ret['data']['token']}
        except requests.exceptions.ConnectionError:
            raise NetWorkException()

    def extendJob(self, authToken: str, jobName: str, dataPath: str, endpoint="/jobs/add_data"):
        try:

            api_call = self.basePath + endpoint

            headers = {"auth-token": authToken}
            files = {'data': ('data.csv', open(dataPath, 'rb'), 'text/csv')}
            payload = {'name': jobName}

            response = requests.post(api_call, headers=headers,
                                     files=files, data=payload)
            ret = response.json()
            if (not ret['success']):
                if (ret['code'] == 403):
                    raise AccessDeniedException(ret['message'])
                    return
                raise JobCreationException(ret['message'])
                return
            return {'message': ret['message']}
            return ret

        except requests.exceptions.ConnectionError:
            raise NetWorkException()

    def scheduleNewJobAutomation(self, email: str, password: str, sec_interval: float, srcData: str,
                                 descPath: str, endpoint="/test"):

        try:

            api_call = self.basePath + endpoint

            files = {
                'desc_file': ('desc.json;', open(descPath, 'rb'), 'application/json;'),
                'src_file': ('src_data.csv;', open(srcData, 'rb'), 'text/csv;'),

            }
            headers = {'content-Type': 'multipart/form-data;boundary=******',
                       'accept': 'application/json'}

            payload = {'email': email,  'password': password, 'sec_interval': sec_interval,
                       }

            response = requests.post(
                api_call, files=files, data=payload)
            ret = response.json()
            if (response.status_code == 422):
                message = getMessageFromError422(ret)
                raise JobCreationSchedulingException(message)
                return
            if (not ret['success']):
                raise JobCreationSchedulingException(ret['message'])
                return
            return {'message': ret['message']}
            return ret

        except requests.exceptions.ConnectionError:
            raise NetWorkException()

    def stopJobCreationAutomation(self, name: str, endpoint="/stopJobCreation"):

        try:
            api_call = self.basePath + endpoint
            payload = {'name': name}

            response = requests.post(
                api_call, json=payload)
            ret = response.json()
            if (response.status_code == 422):
                message = getMessageFromError422(ret)
                raise JobCreationSchedulingException(message)
                return
            if (not ret['success']):
                raise JobCreationSchedulingException(ret['message'])
                return
            return {'message': ret['message']}
            return ret

        except requests.exceptions.ConnectionError:
            raise NetWorkException()
    #

    def rescheduleJobCreationAutomation(self, name: str,  sec_interval: float, endpoint="/reschedule"):

        try:
            api_call = self.basePath + endpoint
            payload = {'name': name, 'sec_interval': sec_interval}

            response = requests.post(
                api_call, json=payload)
            ret = response.json()
            if (response.status_code == 422):
                message = getMessageFromError422(ret)
                raise JobCreationSchedulingException(message)
                return

            if (not ret['success']):
                raise JobCreationSchedulingException(ret['message'])
                return
            return {'message': ret['message']}
            return ret

        except requests.exceptions.ConnectionError:
            raise NetWorkException()

    def createJob(self, jobData, authToken,  endpoint="/jobs/create"):
        try:
            headers = {"auth-token": authToken}
            jobData = jobData
            dataPath = jobData['src_data']
            payload = jobData.copy()
            payload['qa_comments'] = json.dumps(payload['qa_comments'])
            payload.pop('src_data')

            api_call = self.basePath + endpoint

            files = {'data': ('data.csv', open(dataPath, 'rb'), 'text/csv')}
            response = requests.post(
                api_call, headers=headers, files=files, data=payload)
            ret = response.json()
            if (not ret['success']):
                if (ret['code'] == 403):
                    raise AccessDeniedException(ret['message'])
                    return
                raise JobCreationException(ret['message'])
                return
            return {'message': ret['message']}
        except requests.exceptions.ConnectionError:
            raise NetWorkException()

    def getAllJobs(self):
        pass


def getMessageFromError422(errorObj) -> str:
    errorList = errorObj['detail']
    msg = "The following arguments have error\n"
    for error in errorList:
        errorLbl = error['loc'][1]
        errorMsg = error['msg']
        msg += f"  - {errorLbl}: {errorMsg}"
    return msg


if __name__ == "__main__":
    basePath = "http://localhost:4000"
    ah = apiHandler(basePath)
    email = "danielzelalemheru@gmail.com"
    password = "Abc123.."
    print(ah.loginAsAdmin(email, password))
