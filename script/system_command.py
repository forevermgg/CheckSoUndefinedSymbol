import subprocess
from typing import List


def runSystemCommand(cmd: List[str]) -> str:
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    o, e = proc.communicate()  # pylint: disable=unused-variable
    output: str = o.decode("utf8")
    # error = e.decode('utf8')
    return output
