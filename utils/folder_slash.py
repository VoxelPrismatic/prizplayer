import sys

global folder_slash
if sys.executable.startswith("/"):
    folder_slash = "/"
else:
    folder_slash = "\\"

def s(dr):
    return dr.replace("/", folder_slash)
