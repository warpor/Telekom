import re

from rest_framework import serializers

from .models import EquipmentType

regex_map = {
    "N": r"\d",
    "A": r"[A-Z]",
    "a": r"[a-z]",
    "X": r"([A-Z]|\d)",
    "Z": r"[_ - @]"
}


class SerialNumValidator:

    def __call__(self, attrs):
        serial_mask: str = attrs["type_id"].serial_num_mask
        if not self.check_serial_num(serial_mask, attrs["serial_num"]):
            raise serializers.ValidationError("Серийный номер не подходит под маску")

    def check_serial_num(self, serial_mask: str, serial_num: str):
        """
        Проверяет серийный номер на соответствие маске

        Параметры
        ---------
        serial_mask (str): Серийная маска типа оборудования

        serial_num (str): Серийный номер оборудования

        Возвращаемое значение
        ---------------------
        bool: Соответствует ли серийный номер серийной маске
        """

        new_mask = []
        for each_num in serial_mask:
            new_mask.append(regex_map[each_num])
        if re.fullmatch("".join(new_mask), serial_num):
            return True
        return False
