from kphelper.core.checksec import run_checksec
from kphelper.core.probe import probe_guest_runtime, render_probe_report
from kphelper.core.probe_report import render_live_report


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
    parser.add_argument(
        "--live",
        action="store_true",
        help="run live runtime probe only",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="run static checksec and live probe together",
    )
    parser.set_defaults(handler=handle)
    return parser


def handle(args):
    if args.all:
        probe_result = probe_guest_runtime(args.run, timeout=8)
        print(render_probe_report(probe_result, root_dir=args.root, color=not args.no_color))
        return 0
    if args.live:
        live_result = probe_guest_runtime(args.run, timeout=8)
        print(render_live_report(live_result, color=not args.no_color))
        return 0
    print(run_checksec(args.run, args.cpio, args.root, color=not args.no_color))
    return 0
