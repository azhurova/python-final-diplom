import json
from http import HTTPStatus
from os import path

import pytest

from tests import *


def create_basket_order(user, order_factory, order_item_factory, products_info_factory):
    products_info = products_info_factory()

    order = order_factory(_quantity=1, user=user, state='basket')[0]
    for product_info in products_info:
        order_item_factory(_quantity=1, order=order, product_info=product_info)

    return order


@pytest.mark.django_db
def test_basket_get(client, user_authorization_header, order_factory, order_item_factory, products_info_factory):
    request_url = '/api/v1/basket'
    user, headers = user_authorization_header

    # проверяем неавторизованный вызов
    assert_fault_status(client.get(request_url), HTTPStatus.FORBIDDEN)

    # проверяем успешный вызов
    order = create_basket_order(user, order_factory, order_item_factory, products_info_factory)

    data = assert_success_response(client.get(request_url, headers=headers))
    assert len(data) == 1
    assert data[0]['id'] == order.id


@pytest.mark.django_db
def test_basket_post(client, user_authorization_header, products_info_factory):
    request_url = '/api/v1/basket'
    user, headers = user_authorization_header

    # проверяем неавторизованный вызов
    assert_fault_status(client.post(request_url), HTTPStatus.FORBIDDEN)

    # проверяем обязательные аргументы
    data = {
        "params": ""
    }
    assert_fault_status(client.post(request_url, data=data, headers=headers))

    # проверяем формат запроса
    file_dir = 'D:/Programming/WEB/Projects/netology/Diplom/python-final-diplom/data/'
    yaml_file_name = path.join(file_dir, 'shop1.yaml')
    if path.exists(yaml_file_name):
        with open(yaml_file_name, 'rb') as yaml_file:
            assert_fault_status(
                client.post(request_url, data={'items': yaml_file}, format='multipart', headers=headers))

    # проверяем валидацию
    json_file_name = path.join(file_dir, 'basket2_fault.json')
    if path.exists(json_file_name):
        with open(json_file_name, 'rb') as json_file:
            assert_fault_status(
                client.post(request_url, data={'items': json_file}, format='multipart', headers=headers))

    # проверяем успешный вызов
    products_info = products_info_factory()
    json_file_name = path.join(file_dir, 'basket1.json')
    if path.exists(json_file_name):
        with open(json_file_name, 'rb') as json_file:
            data = assert_success_status(
                client.post(request_url, data={'items': json_file}, format='multipart', headers=headers))
            json_file.seek(0)
            products_info = json.load(json_file)
        assert data['Создано объектов'] == len(products_info)


@pytest.mark.django_db
def test_basket_put(client, user_authorization_header, order_factory, order_item_factory, products_info_factory):
    request_url = '/api/v1/basket'
    user, headers = user_authorization_header

    # проверяем неавторизованный вызов
    assert_fault_status(client.put(request_url), HTTPStatus.FORBIDDEN)

    # проверяем обязательные аргументы
    data = {
        "params": ""
    }
    assert_fault_status(client.put(request_url, data=data, headers=headers))

    # проверяем формат запроса
    file_dir = 'D:/Programming/WEB/Projects/netology/Diplom/python-final-diplom/data/'
    yaml_file_name = path.join(file_dir, 'shop1.yaml')
    if path.exists(yaml_file_name):
        with open(yaml_file_name, 'rb') as yaml_file:
            assert_fault_status(
                client.put(request_url, data={'items': yaml_file}, format='multipart', headers=headers))

    # проверяем успешный вызов
    create_basket_order(user, order_factory, order_item_factory, products_info_factory)
    json_file_name = path.join(file_dir, 'basket2.json')
    if path.exists(json_file_name):
        with open(json_file_name, 'rb') as json_file:
            data = assert_success_status(
                client.put(request_url, data={'items': json_file}, format='multipart', headers=headers))
            json_file.seek(0)
            order_items = json.load(json_file)
        assert data['Обновлено объектов'] == len(order_items)


@pytest.mark.django_db
def test_basket_delete(client, user_authorization_header, order_factory, order_item_factory, products_info_factory):
    request_url = '/api/v1/basket'
    user, headers = user_authorization_header

    # проверяем неавторизованный вызов
    assert_fault_status(client.delete(request_url), HTTPStatus.FORBIDDEN)

    # проверяем обязательные аргументы
    data = {
        "params": ""
    }
    assert_fault_status(client.delete(request_url, data=data, headers=headers))

    # проверяем успешный вызов
    create_basket_order(user, order_factory, order_item_factory, products_info_factory)
    data = {
        "items": "1, 2, 3"
    }

    data = assert_success_status(client.delete(request_url, data=data, headers=headers))
    assert data['Удалено объектов'] == 3
