import subprocess
from pathlib import Path

from .errors import KphelperError


def sh_quote(value):
    return "'" + value.replace("'", "'\"'\"'") + "'"


def cpio_command(cpio_path):
    name = str(cpio_path)
    if name.endswith(".gz"):
        return f"gzip -dc {sh_quote(name)} | cpio -idm --quiet"
    if name.endswith(".xz"):
        return f"xz -dc {sh_quote(name)} | cpio -idm --quiet"
    if name.endswith(".bz2"):
        return f"bzip2 -dc {sh_quote(name)} | cpio -idm --quiet"
    if name.endswith(".lz4"):
        return f"lz4 -dc {sh_quote(name)} | cpio -idm --quiet"
    return f"cpio -idm --quiet < {sh_quote(name)}"


def unpack_cpio(cpio_path, root_dir="root"):
    cpio_path = Path(cpio_path).resolve()
    root_dir = Path(root_dir)
    root_dir.mkdir(exist_ok=True)
    cmd = cpio_command(cpio_path)
    try:
        subprocess.run(cmd, shell=True, cwd=root_dir, check=True)
    except subprocess.CalledProcessError as e:
        raise KphelperError("failed to unpack %s, exit code: %d" % (cpio_path, e.returncode)) from e
    return root_dir
