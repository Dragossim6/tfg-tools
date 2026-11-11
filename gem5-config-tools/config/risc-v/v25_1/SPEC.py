from SPEC_CMDS import *
import re

def getSpecAppList():
    return [name for name in spec_app_binaries.keys()]

def getSpecBinary(app_num):
    return spec_app_binaries[app_num]

def getSpecArgs(app_num):
    return spec_app_arguments.get(app_num, [])

def getSpecInput(app_num):
    return spec_app_input_files.get(app_num, None)

def getSpecOutput(app_num):
    return spec_app_output_files.get(app_num, None)