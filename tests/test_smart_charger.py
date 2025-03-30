from victron_ble.devices.base import ChargerError, OperationMode
from victron_ble.devices.smart_charger import SmartCharger, SmartChargerData


class TestDcDcConverter:
    def test_end_to_end_parse(self) -> None:
        data = "10003ca308f029dda2353d66d55c511ba83393f6f6"
        actual = SmartCharger("dded259f2e2323330d118cc7d99ccd9d").parse(
            bytes.fromhex(data)
        )
        assert isinstance(actual, SmartChargerData)

        assert actual.get_charge_state() == OperationMode.BULK
        assert actual.get_charger_error() == ChargerError.NO_ERROR
        assert actual.get_battery_voltage() == 13.57
        assert actual.get_battery_charging_current() == 5.0
        assert actual.get_model_name() == "Blue Smart IP65 Charger 12|5"

    def parse_decrypted(self, decrypted: str) -> SmartChargerData:
        parsed = SmartCharger(None).parse_decrypted(bytes.fromhex(decrypted))
        return SmartChargerData(None, parsed)

    def test_parse(self) -> None:
        actual = self.parse_decrypted("03004d4506ffffffffffffffff2b4f02")
        assert actual.get_charge_state() == OperationMode.BULK
        assert actual.get_charger_error() == ChargerError.NO_ERROR
        assert actual.get_battery_voltage() == 13.57
        assert actual.get_battery_charging_current() == 5.0
