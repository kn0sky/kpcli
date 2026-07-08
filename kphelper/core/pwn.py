from pwn import *

context.terminal = ["tmux", "splitw", "-h"]   # tmux 横向分屏
