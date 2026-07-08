# kphelper

`kphelper` is a small CLI helper for local kernel pwn challenge workflows. It can start a local QEMU script, upload a statically compiled exploit, connect KGDB, connect remote shells, and inspect common kernel challenge security settings.

The intended runtime environment is Linux/WSL.

## Install

From this repository:

```bash
pip3 install -e .
```

After installation, use:

```bash
kphelper
```

Running without arguments prints the help text.

## Directory Requirements

For `run` and `debug` modes, run `kphelper` inside a challenge directory containing:

```text
run.sh
```

For `debug`, the directory should also contain the symbol file you pass to the command. If omitted, it defaults to:

```text
vmlinux
```

Exploit upload is optional:

```text
exp.c    # compiled with musl-gcc -static -o exp exp.c
exp      # uploaded to /tmp/exp
```

If `exp.c` exists, it is compiled first. If neither `exp.c` nor `exp` exists, upload is skipped.

The target shell prompt may be either:

```text
$ 
# 
```

After upload, `kphelper` only switches to `/tmp`; it does not execute `/tmp/exp` automatically.

## Commands

### `kphelper run`

Start local `./run.sh`, compile/upload `exp` if available, switch to `/tmp`, then enter interactive mode.

```bash
kphelper run
```

### `kphelper debug [symbol]`

Start local `./run.sh`, prepare the target, then open KGDB in a tmux split.

```bash
kphelper debug
kphelper debug ./vmlinux
kphelper debug ./module.ko
```

The default symbol file is `vmlinux`.

### `kphelper remote <ip> <port>`

Connect to a remote shell, compile/upload `exp` if available, switch to `/tmp`, then enter interactive mode.

```bash
kphelper remote 127.0.0.1 1337
```

### `kphelper checksec [cpio]`

Inspect common kernel challenge security settings from `run.sh`. Optionally unpack an initramfs cpio into `./root` and scan its `init`.

```bash
kphelper checksec
kphelper checksec rootfs.cpio
kphelper checksec rootfs.cpio.gz --root root
kphelper checksec -r ./run.sh rootfs.cpio --no-color
```

The output uses color by default:

- Green: enabled or favorable status
- Red: disabled, missing, or risky status
- Yellow: unknown
- Cyan: paths and informational values

## Command Extension

Commands are loaded dynamically from:

```text
kphelper/commands/
```

Command files must use the prefix:

```text
kp_<command>.py
```

Each command module exports:

```python
def register(subparsers):
    parser = subparsers.add_parser("name", help="...")
    parser.set_defaults(handler=handle)
    return parser


def handle(args):
    ...
    return 0
```

For example, `kphelper/commands/kp_pack.py` automatically becomes:

```bash
kphelper pack
```

Shared reusable logic lives under:

```text
kphelper/core/
```
