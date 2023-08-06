import json
import re


class ReportBuilder:

    issues_all = {"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [], "size": 0}

    def __init__(self):
        self.issues_all = {"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [], "size": 0}

    # def extract_basename(self, path):
    #     """Extracts basename of a given path (either dir or file). Should Work with any OS Path on any OS"""
    #     basename = re.search(r'[^\\/]+(?=[\\/]?$)', path)
    #     if basename:
    #         return basename.group(0)

    def extract_basename_file(self, path):
        """Extracts basename of a given path (only files). Should Work with any OS Path on any OS"""
        basename = re.search(r"[^\\/]+(?![\\/])$", path)
        if basename:
            return basename.group(0)

    def addIssue(self, path, severity, message, lineStart=-1, lineEnd=-1, columnStart=-1, columnEnd=-1, category=None, type=None, description=None, packageName=None, moduleName=None, additionalProperties=None):

        lineStart = int(lineStart)
        lineEnd = int(lineEnd)
        columnStart = int(columnStart)
        columnEnd = int(columnEnd)

        filename = self.extract_basename_file(path)
        severity = severity.upper()
        if filename is None or filename == "":
            raise Exception("Path is not a file path!")
        if severity not in ["LOW", "NORMAL", "HIGH", "CRITICAL", "ERROR"]:
            raise Exception("Path is not a file path!")
        if message is None or message == "":
            raise Exception("Message must not be empty!")
        dirname = path.replace(filename, "")

        issue = {"fileName": path, "directory": dirname, "severity": severity, "message": message}

        if lineStart > -1:
            issue.update({"lineStart": lineStart})

        if lineStart > -1 and lineEnd > -1:  # requires start to have end
            issue.update({"lineEnd": lineEnd})

        if columnStart > -1:
            issue.update({"columnStart": columnStart})

        if columnStart > -1 and columnEnd > -1:  # requires start to have end
            issue.update({"columnEnd": columnEnd})

        if category is not None:
            issue.update({"category": category})

        if type is not None:
            issue.update({"type": type})

        if description is not None:
            issue.update({"description": description})

        if packageName is not None:
            issue.update({"packageName": packageName})

        if moduleName is not None:
            issue.update({"moduleName": moduleName})

        if additionalProperties is not None:
            issue.update({"additionalProperties": additionalProperties})

        if issue not in self.issues_all["issues"]:
            self.issues_all["issues"].append(issue)

    def generateReport(self):
        self.issues_all["size"] = len(self.issues_all["issues"])
        return json.dumps(self.issues_all)
