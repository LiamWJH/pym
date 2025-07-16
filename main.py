import argparse
import re as regex

parser = argparse.ArgumentParser()
parser.add_argument("--run", type=str, default="main.pys")
args = parser.parse_args()

with open(args.run, "r") as f:
    file = f.read()

usercode = """
class Typeddata:
    def __init__(self, varname):
        self.varname = varname
    
    def initdata(self, datatype, value):
        self.datatype = datatype
        self.value = value

    def reassigndata(self, value):
        if isinstance(value, str):
            thisdatatype = "str64" if len(value) <= 64 else "str~"
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
        print(f"wrong data type for variable '{self.varname}' value '{self.value}' is not '{self.datatype}'💀")
"""

VAR_DECLARE_PATTERN = regex.compile(
    r"^(\w+)\s*:\s*((i8|int8)|(i16|int16)|(i32|int32)|(i64|int64)|(i~|int~)|(s64|str64)|(s~|str~)|(f8|float8)|(f16|float16)|(f32|float32)|(f64|float64)|(f~|float~))\s*=\s*(.+)$"
)

declared_vars = []
indent_level = 0
usercode_lines = []

for line in file.split("\n"):
    stripped = line.strip()

    if stripped == "{":
        indent_level += 1
        continue
    elif stripped == "}":
        indent_level -= 1
        continue

    if VAR_DECLARE_PATTERN.match(stripped):
        var_match = regex.match(r"^(\w+)", stripped)
        type_match = regex.match(r"^\w+\s*:\s*(\w+)", stripped)
        value_match = regex.search(r"=\s*(.+)", stripped)

        if var_match and type_match and value_match:
            varname = var_match.group(1)
            typename = type_match.group(1)
            value = value_match.group(1)
            evaled_val = eval(value)

            if varname in declared_vars:
                usercode_lines.append("    " * indent_level + f"{varname}.reassigndata({repr(evaled_val)})")
            else:
                declared_vars.append(varname)
                usercode_lines.append("    " * indent_level + f"{varname} = Typeddata('{varname}')")
                usercode_lines.append("    " * indent_level + f"{varname}.initdata('{typename}', {repr(evaled_val)})")
        continue

    if regex.match(r"^(if|elif|else|while|for)\b.*", stripped) and not stripped.endswith(":"):
        stripped += ":"

    usercode_lines.append("    " * indent_level + stripped)

usercode += "\n" + "\n".join(usercode_lines)


exec(usercode)
