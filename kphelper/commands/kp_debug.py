from kphelper import core


def register(subparsers):
    parser = subparsers.add_parser(
        "debug",
        help="start ./run.sh, upload exp if present, then connect kgdb",
    )
    parser.add_argument(
        "symbol",
        nargs="?",
        help="debug symbol file passed to gdb, default: auto-detect vmlinux",
    )
    parser.set_defaults(handler=handle)
    return parser


def handle(args):
    symbol = args.symbol
    if symbol is None:
        found = core.find_vmlinux()
        symbol = str(found) if found else "vmlinux"

    io = core.local_target()
    core.prepare_target(io)
    core.kgdb(symbol)
    core.interact(io)
    return 0
