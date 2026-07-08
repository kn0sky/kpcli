from kphelper import core
from kphelper.core.pwn import log


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

    core.build_only()
    debug_run = core.create_debug_run_copy()
    log.success("generated debug run script: %s", debug_run)

    io = None
    debugger = None
    try:
        io = core.local_target("./" + str(debug_run))
        core.upload_and_cd(io)
        debugger = core.kgdb(symbol)
        core.interact(io)
    finally:
        core.close_debugger(debugger)
        core.close_session(io)
    return 0
