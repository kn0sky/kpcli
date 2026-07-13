import unittest

from kphelper.core.findings import Finding
from kphelper.core.probe import HIDDEN, READABLE, _probe_kallsyms


class ProbeTests(unittest.TestCase):
    def test_kallsyms_is_hidden_when_kptr_restrict_blocks_addresses(self):
        finding, symbols = _probe_kallsyms(
            None,
            (),
            Finding(READABLE, value=1),
        )

        self.assertEqual(finding.status, HIDDEN)
        self.assertEqual(finding.detail, "kptr_restrict=1")
        self.assertEqual(symbols, {})


if __name__ == "__main__":
    unittest.main()
