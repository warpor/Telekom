from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response


def multiple_objects_add(model_object: viewsets.ModelViewSet, request: Request) -> Response:
    """
    Пробует добавить массив объектов из запроса.
    """

    serializer = model_object.get_serializer(data=request.data, many=True)
    if not check_for_unique_value_in_request(request):
        return Response(data={"non_field_errors": ["В запросе не уникальные серийные номера"]},
                        status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        model_object.perform_create(serializer)
        headers = model_object.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    return Response(list(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


def check_for_unique_value_in_request(request: Request) -> bool:
    """
    Проверяет серийные номера в запросе на уникальность.
    """

    type_ids: dict[int, set[str]] = dict()
    for each_value in request.data:
        type_id: int = each_value["type_id"]
        serial_num: str = each_value["serial_num"]

        if not type_ids.get(type_id):
            type_ids[type_id] = {serial_num}
            continue

        if serial_num in type_ids[type_id]:
            return False

        type_ids[type_id].add(serial_num)
    return True
