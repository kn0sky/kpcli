import base64
import gzip
from pathlib import Path

from .constants import LOCAL_EXP, PROMPTS, REMOTE_EXP
from .pwn import log


def upload(io, local=LOCAL_EXP, remote=REMOTE_EXP, p=PROMPTS):
    local = Path(local)
    if not local.exists():
        log.info("local exp not found, skip upload: %s", local)
        return False

    b = base64.b64encode(gzip.compress(local.read_bytes()))
    io.sendlineafter(p, b": > /tmp/e.b64")
    for i in range(0, len(b), 512):
        io.sendlineafter(p, b"echo -n '%s' >> /tmp/e.b64" % b[i:i + 512])
    io.sendlineafter(
        p,
        b"base64 -d /tmp/e.b64|gzip -d>%s;chmod +x %s"
        % (remote.encode(), remote.encode()),
    )
    log.success("uploaded %s -> %s", local, remote)
    return True
