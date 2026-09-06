"""Codex host Admin gets its declared direct-host maintenance authority."""
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".super-coder" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import run

ADMIN_FLAGS = [
    "--sandbox",
    "danger-full-access",
    "--ask-for-approval",
    "never",
]
BYPASS = "--dangerously-bypass-approvals-and-sandbox"


def _codex() -> dict:
    return json.loads((run.ADAPTERS / "codex" / "adapter.json").read_text())


class CodexPermissionFlagsTest(unittest.TestCase):
    def test_host_admin_gets_unrestricted_filesystem_without_bypass_flag(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(
                run.launch_mode_flags(_codex(), headless=False, host_admin=True),
                ADMIN_FLAGS,
            )

    def test_ordinary_host_shell_keeps_codex_defaults(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(run.launch_mode_flags(_codex(), headless=False), [])

    def test_container_keeps_external_sandbox_bypass(self) -> None:
        with mock.patch.dict(os.environ, {"SC_SANDBOX": "1"}, clear=True):
            self.assertEqual(
                run.launch_mode_flags(_codex(), headless=False),
                [BYPASS],
            )


if __name__ == "__main__":
    unittest.main()
