import json
from pathlib import Path


class JobExeception(Exception):
    pass


class ValueNotDefined(JobExeception):
    def __init__(self, label: str):
        self.message = f"Value for {label} is required but got nothing or empty"
        super().__init__(self.message)


class ValueTypeError(JobExeception):
    def __init__(self, label: str, value: str, expectedType: str):
        self.message = f"Invalid type found for {label}. Expected type is {expectedType}, but found {type(value)}"
        super().__init__(self.message)


class ValueError(JobExeception):
    def __init__(self, message="Invalid value"):
        self.message = message
        super().__init__(self.message)


class JobDataVerificationWrapper:
    def __init__(self, verfied: bool, data, message):
        self.verfied = verfied
        self.data = data
        self.message = message


class DescriptionVerifier:
    def __init__(self, path: str, readFromSrcDataDefualtLocation=False):
        try:
            self.path = path
            self.readFromSrcDataDefualtLocation = readFromSrcDataDefualtLocation
            with open(path, "r") as f:
                self.config = json.load(f)
        except FileNotFoundError as e:
            e.strerror = "Job Description file not found"
            raise e
        except json.decoder.JSONDecodeError as e:
            self.config = None

    def verify(self) -> bool:
        try:
            self.verifyName(self.config['name'])
            self.verifyInstruction(self.config['instruction'])
            self.verifyQaInstruction(self.config['qa_instruction'])
            self.verifyRedoThreshold(self.config['redo_threshold'])
            self.verifyQaPct(self.config['qa_pct'])
            self.verifyComments(self.config['qa_comments'])
            self.verifyQuota(self.config['quota'])
            self.verifyQaQuota(self.config['qa_quota'])
            if self.readFromSrcDataDefualtLocation:
                srcDataPath = "src_data.csv"
            else:
                srcDataPath = self.config['src_data']

            self.verifyFilePath(srcDataPath)
            self.config['src_data'] = self.actualPathOfSrcData(srcDataPath)

            return True

        except KeyError as e:
            raise ValueNotDefined(e.args[0])
            return False

    def actualPathOfSrcData(self, value):
        actualPath = "./" + str(Path(self.path).parent) + "/" + value
        return actualPath

    def getDescConfig(self) -> JobDataVerificationWrapper:
        if (self.config == None):
            return JobDataVerificationWrapper(False, None, "Job description file is not a valid JSON data")
        try:
            self.verify()
            return JobDataVerificationWrapper(True, self.config, "")
        except JobExeception as e:
            return JobDataVerificationWrapper(False, None, e.message)
            return {"verfied": False, "data": None, "message": e.message}

    def verifyName(self, value) -> bool:
        if not value or not value.strip():
            raise ValueNotDefined("Name ('name')")
        if type(value) != str:
            raise ValueTypeError("Name ('name')", value, "String")
        return True

    def verifyInstruction(self, value) -> bool:
        if not value or not value.strip():
            raise ValueNotDefined("Instruction ('instruction')")
        if type(value) != str:
            raise ValueTypeError(
                "Instruction ('instruction')", value, "String")
        return True

    def verifyQaInstruction(self, value) -> bool:
        if not value or not value.strip():
            raise ValueNotDefined("QA Instruction ('qa_instruction')")
        if type(value) != str:
            raise ValueTypeError(value, "String")
        return True

    def verifyRedoThreshold(self, value) -> bool:
        if not value:
            raise ValueNotDefined("Redo threshold ('redo_threshold')")
        if type(value) != float and type(value) != int:
            raise ValueTypeError(
                "Redo threshold ('redo_threshold')", value, "Integer or float")
        return True

    def verifyQaPct(self, value) -> bool:
        if not value:
            raise ValueNotDefined("QA percentage ('qa_pct')")

        if type(value) != float and type(value) != int:
            raise ValueTypeError("QA percentage ('qa_pct')",
                                 value, "Integer or float")

        if value < 0 or value > 100:
            raise ValueError(
                "QA percentage ('qa_pct') must be in range b/n 0 and 100")

        return True

    def verifyComments(self, value) -> bool:
        if type(value) != list:
            raise ValueTypeError("Comments ('comments')", value, "List")
        for item in value:
            if (type(item) != str or not item.strip()):
                raise ValueTypeError('comment', item, "String")
        return True

    def verifyFilePath(self, value) -> bool:
        if not value:
            raise ValueNotDefined("Dataset path ('src_data')")
        if type(value) != str or not value.strip():
            raise ValueTypeError("Dataset path ('src_data')", value, "String")

        actualPath = self.actualPathOfSrcData(value)
        path = Path(actualPath)
        if path and path.is_file():
            return True
        else:
            raise ValueError("Dataset path ('src_data') is not a valid path")

    def verifyQuota(self, value) -> bool:
        if not value:
            raise ValueNotDefined("Quota ('quota')")
        if type(value) != int:
            raise ValueTypeError("Quota ('quota')", value, "Integer or float")
        if value < 0:
            raise ValueError(
                "Quota ('quota') cant be negative")

    def verifyQaQuota(self, value) -> bool:
        if not value:
            raise ValueNotDefined("QA Quota ('qa_quota')")
        if type(value) != int:
            raise ValueTypeError("QA Quota ('qa_quota')",
                                 value, "Integer or float")
        if value < 0:
            raise ValueError(
                "QA Quota ('qa_quota') cant be negative")


if __name__ == "__main__":
    dv = DescriptionVerifier("../job-desc-files/desc.json")
    print(dv.getDescConfig())
