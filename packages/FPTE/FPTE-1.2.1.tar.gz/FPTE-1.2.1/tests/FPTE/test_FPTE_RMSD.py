from unittest.mock import patch

import pytest

from FPTE.FPTE_RMSD import fpte_rmsd


class TestFPTERMSD:
    @patch("os.path.exists", return_value=False)
    def test_contcar_not_exist(self, patched_exist):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            fpte_rmsd()

        assert pytest_wrapped_e.type == SystemExit
        patched_exist.assert_called()
        patched_exist.assert_called_with("CONTCAR")

