from kphelper.core.checksec import run_checksec


def register(subparsers):
    parser = subparsers.add_parser(
        "checksec",
        help="inspect kernel challenge security settings from run.sh and optional cpio",
    )
    parser.add_argument(
        "-r",
        "--run",
        default="run.sh",
        help="qemu startup script to analyze, default: run.sh",
    )
    parser.add_argument(
        "cpio",
        nargs="?",
        help="optional initramfs cpio archive, default: auto-detect from run.sh or current tree",
    )
    parser.add_argument(
        "--root",
        default="root",
        help="directory used for unpacked cpio, default: root",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable ANSI color output",
    )
    parser.set_defaults(handler=handle)
    return parser


def handle(args):
    print(run_checksec(args.run, args.cpio, args.root, color=not args.no_color))
    return 0
