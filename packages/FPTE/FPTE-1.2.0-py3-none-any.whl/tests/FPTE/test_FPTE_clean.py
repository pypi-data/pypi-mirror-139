from unittest.mock import patch

from FPTE.FPTE_clean import fpte_clean


class TestFPTEClean:
    @patch("builtins.input")
    @patch("os.system")
    def test_fpte_clean(self, patched_system, patched_input):
        fpte_clean()
        patched_input.assert_called_once()
        patched_system.assert_called_once()
