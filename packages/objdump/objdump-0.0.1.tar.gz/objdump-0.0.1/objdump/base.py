"""
this module will create a background process (addr2line -g -e filename)
"""


from pathlib import Path
import subprocess


def get_function_assemble(binary_path, function_name, objdump=None):
    if objdump is None:
        objdump = "objdump"
    res = subprocess.run(
        [
            "objdump",
            "-d",
            f"--disassemble={function_name}",
            binary_path,
        ],
        capture_output=True,
        check=True,
    )
    for content in res.stdout.decode("utf-8").split("\n\n")[1:]:
        if content.strip("\n").startswith("Disassembly of section"):
            continue
        return content
