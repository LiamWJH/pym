"""
adding

data types
braces
;

arch:
gets file. see type
do shit
convert the pypp into a program string
so the shit using eval
"""

usercode = """
class Typedata:
    def __init__(self):
        pass
    
    def initdata(self,datatype,value):
        self.datatype = datatype
        self.value = value
    
    def reassigndata(self, value):
        
        if isinstance(value, str):
            if len(value) <= 64:
                thisdatatype = "str64"
            else:
                thisdatatype = "str~"
        
        elif isinstance(value, int):
            if -128 <= value <= 127:
                thisdatatype = "int8"
            elif -32768 <= value <= 32767:
                thisdatatype = "int16"
            elif -2147483648 <= value <= 2147483647:
                thisdatatype = "int32"
            elif -9223372036854775808 <= value <= 9223372036854775807:
                thisdatatype = "int64"
            else:
                thisdatatype = "int~"
        
        elif isinstance(value, float):
            if abs(value) <= 3.4e38:
                thisdatatype = "float32"
            elif abs(value) <= 1.8e308:
                thisdatatype = "float64"
            else:
                thisdatatype = "float~"
        
        else:
            thisdatatype = "unknown"

        if thisdatatype == self.datatype:
            self.value = value
            return True
        else:
            return False

"""


            

import argparse
import re as  regex


parser = argparse.ArgumentParser()

parser.add_argument("--run", type=str, default="main.pys")

args = parser.parse_args()

with open(args.run , "r") as f:
    file = f.read()

VAR_DECLARE_PATTERN = regex.compile(r"^\w*:\s*((i8|int8)|(i16|int16)|(i32|int32)|(i64|int64)|(i~|int~)|(s64|str64)|(s~|str~)|(f8|float8)|(f16|float16)|(f32|float32)|(f64|float64)|(f~|float~))\s*=\s*.*")


for line in file.split("\n"):
    line = line.strip()
    if regex.match(r"^if\s+.*:", line) or regex.match(r"^elif\s+.*:", line) or regex.match(r"^else:", line):
        print(line)
    else:
        if VAR_DECLARE_PATTERN.match(line):
            regex.search(r"")
