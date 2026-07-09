"""
开发示例模板

这个文件的用途：
- 给新手提供一个可以直接复制的命令模板
- 演示 commands/ 目录里一个命令文件应该如何组织
- 说明哪些内容应该写在 commands/，哪些内容应该下沉到 core/

使用建议：
- 如果你要新增一个真正的命令，可以复制这个文件后改名
- 把命令名、参数名、帮助信息换成你的实际功能
- 把 handle() 里的占位逻辑替换成 core 层函数调用

约定：
- commands/ 目录只负责命令入口、参数定义、调用 core
- 不要把复杂业务逻辑直接堆在这里
- 成功时返回 0
- 用户可修正的错误，优先抛 KphelperError
"""

from kphelper.core.errors import KphelperError


def register(subparsers):
    """注册子命令。

    新命令通常只需要：
    1. 给命令起名字
    2. 定义参数
    3. 绑定 handler
    """
    parser = subparsers.add_parser(
        "example",
        help="developer template command",
    )
    parser.add_argument(
        "input_path",
        help="example input path",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print extra debug information",
    )
    parser.set_defaults(handler=handle)
    return parser


def handle(args):
    """执行命令。

    推荐写法：
    1. 读取参数
    2. 调用 core 层函数
    3. 打印结果
    4. 返回 0

    这个模板里只保留了占位逻辑，方便你复制后直接改。
    """
    try:
        input_path = args.input_path
        verbose = args.verbose

        # 把真正的业务逻辑放到 core/ 里，例如：
        # from kphelper.core.example import do_example
        # result = do_example(input_path, verbose=verbose)

        # 这里先用占位输出演示命令如何返回结果。
        if verbose:
            print(f"[example] input_path={input_path!r}, verbose={verbose}")
        else:
            print(f"[example] input_path={input_path!r}")

        return 0
    except KphelperError:
        # 如果 core 层已经抛了业务异常，直接继续向上抛给 cli.py 统一处理。
        raise
