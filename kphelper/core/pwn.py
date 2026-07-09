from pwn import context, process, remote, log

context.terminal = ["tmux", "splitw", "-h"]   # tmux 横向分屏
