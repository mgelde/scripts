#! /usr/bin/python3

import subprocess
import logging
import yaml
import re
import os
import shutil
from contextlib import ExitStack
from argparse import ArgumentParser
from os.path import abspath, join, basename
from tempfile import TemporaryDirectory
from logging import debug

# Change to DEBUG for more debugging output.
logging.basicConfig(level=logging.ERROR, format="%(levelname)s:%(message)s")

def parseArguments():
    argparser = ArgumentParser(description="A LaTeX letter ftory")
    argparser.add_argument("-t", help="template file", action="store", dest="templateFile")
    argparser.add_argument("substitutionFile", help="The file containing the substitutions", action="store")
    return argparser.parse_args()

KEY_PATTERNS = "patterns"
KEY_PATTERN = "Exp"
KEY_SUBSTITUTION = "Sub"
KEY_NAME = "name"

def readYaml(fileName):
    with open(fileName, "r") as handle:
        content = yaml.load_all(handle)
        contentList = list(content)
    return contentList

class SubFile:
    """A file substitution.

    Specifies how a set of patterns should be substituted to create a give file.
    """

    def __init__(self, subFileDict):
        assert type(subFileDict) is dict
        self._name = subFileDict[KEY_NAME]
        debug("SubFile '%s'", self._name)
        self._patterns = []
        for entry in subFileDict[KEY_PATTERNS]:
            debug("\t%s", entry)
            self._patterns.append((re.compile(entry[KEY_PATTERN]), entry[KEY_SUBSTITUTION]))

    def handle(self, line):
        for pattern, sub in self._patterns:
            return pattern.sub(sub, line)

    def name(self) -> str:
        return self._name

def readSubstitutions(fileName):
    yamlContent = readYaml(fileName)
    assert type(yamlContent) is list
    subs = []
    for fileObject in yamlContent:
        assert type(fileObject) is dict
        subs.append(SubFile(fileObject))
    return subs

def createFiles(outputFileList, tempDir, templateFile):
    with ExitStack() as stack:
        descripors = {x.name() : stack.enter_context(
            open(join(tempDir, x.name()), "w")) for x in outputFileList}
        with open(templateFile) as inputFile:
            for line in inputFile:
                for outputObject in outputFileList:
                    newLine = outputObject.handle(line)
                    descripors[outputObject.name()].write(newLine)

def main():
    arguments = parseArguments()
    substitutionFile = abspath(arguments.substitutionFile)
    outputFileList = readSubstitutions(substitutionFile)
    with TemporaryDirectory() as tempDir:
        createFiles(outputFileList, tempDir, abspath(arguments.templateFile))
        for fileName in [join(tempDir, fileObject.name()) for fileObject in outputFileList]:
            print("[+] Compiling '%s'" % fileName)
            with open(os.devnull, "w") as devNull:
                subprocess.check_call(["pdflatex", "-interaction=nonstopmode", "-output-directory", tempDir, fileName], stdout=devNull)
            print("[+] ... done.")
            shutil.copy2(fileName + ".pdf", os.curdir)

if __name__ == "__main__":
    main()
