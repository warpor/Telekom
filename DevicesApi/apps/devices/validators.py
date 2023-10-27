import re

from rest_framework import serializers

from .models import DeviceType

regex_map = {
    "N": r"\d",
    "A": r"[A-Z]",
    "a": r"[a-z]",
    "X": r"([A-Z]|\d)",
    "Z": r"[_ - @]"
}


class SerialNumValidator:

    def get_serial_mask(self, device_type: DeviceType) -> str:
        """
        Возвращает маску серийного номера
        """

        return device_type.serial_num_mask

    def __call__(self, attrs):
        serial_mask = self.get_serial_mask(attrs["type_id"])
        if not self.check_serial_num(serial_mask, attrs["serial_num"]):
            raise serializers.ValidationError("Серийный номер не подходит под маску")

    def check_serial_num(self, serial_mask, serial_num):
        """
        Проверяет серийный номер на соотвеетствие маске
        """

        new_mask: list[str] = []
        for each_num in serial_mask:
            new_mask.append(regex_map[each_num])
        if re.fullmatch("".join(new_mask), serial_num):
            return True
        return False
