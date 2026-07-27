from hermes_clean.malyarka_dialog_commands import MalyarkaDialogCommandSession
from hermes_modules.malyarka.hardening_adapter import get_hardening_status


def test_hermes_clean_dialog_command_is_compatibility_wrapper():
    session = MalyarkaDialogCommandSession()

    result = session.run("/order paint | 2 | bucket")

    assert result.main_module == "hermes_modules.malyarka"
    assert result.confirmed_rows == 1
    assert result.pending_disputes == 0


def test_hardening_adapter_still_keeps_reference_layer():
    status = get_hardening_status()

    assert status.compatibility_layer == "hermes_clean"
    assert status.validation_available is True
    assert status.export_gate_available is True
