import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from kphelper.cli import build_parser
from kphelper.commands.kp_debug import handle as handle_debug
from kphelper.commands.kp_symbols import handle as handle_symbols
from kphelper.core.errors import KphelperError
from kphelper.core.session import local_target, remote_target


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_only_registered_commands_are_exposed(self):
        parser = build_parser()
        subparsers = next(
            action for action in parser._actions if hasattr(action, "choices") and action.choices
        )

        self.assertNotIn("example", subparsers.choices)
        self.assertIn("checksec", subparsers.choices)

    def test_static_checksec_runs_without_site_packages(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "run.sh").write_text(
                "qemu-system-x86_64 -append 'console=ttyS0 nokaslr nopti'\n"
            )
            env = os.environ.copy()
            env["PYTHONPATH"] = str(PROJECT_ROOT)
            result = subprocess.run(
                [sys.executable, "-S", "-m", "kphelper", "checksec", "--no-color"],
                cwd=tmp,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Kernel checksec", result.stdout)
        self.assertIn("KASLR", result.stdout)

    @patch("kphelper.core.session.process")
    def test_local_target_rejects_missing_run_script(self, process):
        with self.assertRaisesRegex(KphelperError, "startup script not found"):
            local_target("/definitely/missing/run.sh")

        process.assert_not_called()

    @patch("kphelper.core.session.remote", side_effect=RuntimeError("connection refused"))
    def test_remote_connection_errors_are_user_facing(self, _remote):
        with self.assertRaisesRegex(KphelperError, "failed to connect to 127.0.0.1:1"):
            remote_target("127.0.0.1", 1)

    def test_debugger_starts_before_upload_waits_for_paused_guest(self):
        events = []
        io = object()
        with ExitStack() as stack:
            stack.enter_context(patch("kphelper.commands.kp_debug.build_only"))
            stack.enter_context(
                patch("kphelper.commands.kp_debug.create_debug_run_copy", return_value=Path("debug.sh"))
            )
            session = stack.enter_context(patch("kphelper.commands.kp_debug.managed_session"))
            stack.enter_context(
                patch("kphelper.commands.kp_debug.kgdb", side_effect=lambda _symbol: events.append("gdb"))
            )
            stack.enter_context(
                patch("kphelper.commands.kp_debug.upload_and_cd", side_effect=lambda _io: events.append("upload"))
            )
            stack.enter_context(patch("kphelper.commands.kp_debug.interact"))
            session.return_value.__enter__.return_value = io
            handle_debug(SimpleNamespace(symbol="vmlinux", nokaslr=False))

        self.assertEqual(events, ["gdb", "upload"])

    @patch("kphelper.commands.kp_symbols._runtime_symbols")
    @patch("kphelper.commands.kp_symbols._cached_symbols", return_value="cached symbols")
    @patch("builtins.print")
    def test_symbols_uses_cache_unless_refresh_is_requested(self, print_output, cached, runtime):
        args = SimpleNamespace(
            symbols=None,
            analysis=False,
            remote=None,
            file=None,
            refresh=False,
            run="run.sh",
            json=False,
            format="macro",
        )

        handle_symbols(args)

        cached.assert_called_once()
        runtime.assert_not_called()
        print_output.assert_called_once_with("cached symbols")


if __name__ == "__main__":
    unittest.main()
