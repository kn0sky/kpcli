from kphelper import core


def register(subparsers):
    parser = subparsers.add_parser("run", help="start ./run.sh and upload exp if present")
    parser.set_defaults(handler=handle)
    return parser


def handle(args):
    io = core.local_target()
    core.prepare_target(io)
    core.interact(io)
    return 0
