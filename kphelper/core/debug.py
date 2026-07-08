from pwnlib.util.misc import run_in_new_terminal


def kgdb(symbol_file="vmlinux"):
    # 连 qemu gdbserver,不是 attach 进程
    cmd = [
        "gdb", symbol_file,
        "-ex", "set architecture i386:x86-64",
        "-ex", "target remote localhost:1234",
        "-ex", f"add-symbol-file {symbol_file} 0xffffffff81000000",
        # "-ex", "b prepare_kernel_cred",   # 按需下断
    ]
    return run_in_new_terminal(cmd)   # 在 tmux 右屏开 gdb
