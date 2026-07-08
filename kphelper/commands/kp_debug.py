from kphelper import core


def register(subparsers):
    parser = subparsers.add_parser(
        "debug",
        help="start ./run.sh, upload exp if present, then connect kgdb",
    )
    parser.add_argument(
        "symbol",
        nargs="?",
        default="vmlinux",
        help="debug symbol file passed to gdb, default: vmlinux",
    )
    parser.set_defaults(handler=handle)
    return parser


def handle(args):
    io = core.local_target()
    core.prepare_target(io)
    core.kgdb(args.symbol)
    core.interact(io)
    return 0
