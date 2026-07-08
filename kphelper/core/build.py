import subprocess
import sys
from pathlib import Path

from .constants import LOCAL_EXP, LOCAL_EXP_C
from .pwn import log


def build_exp(source=LOCAL_EXP_C, output=LOCAL_EXP):
    source = Path(source)
    output = Path(output)
    if not source.exists():
        return False

    log.info("found %s, compiling static exp with musl-gcc", source)
    try:
        subprocess.run(
            ["musl-gcc", "-static", "-o", str(output), str(source)],
            check=True,
        )
    except FileNotFoundError:
        log.failure("musl-gcc not found")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        log.failure("failed to compile %s, exit code: %d", source, e.returncode)
        sys.exit(e.returncode)

    log.success("compiled %s -> %s", source, output)
    return True
