from kphelper import core


def register(subparsers):
    parser = subparsers.add_parser("remote", help="connect remote target")
    parser.add_argument("ip")
    parser.add_argument("port", type=int)
    parser.set_defaults(handler=handle)
    return parser


def handle(args):
    io = core.remote_target(args.ip, args.port)
    core.prepare_target(io)
    core.interact(io)
    return 0
