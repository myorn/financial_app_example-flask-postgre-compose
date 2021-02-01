"""python3 -m pytest -sv"""
import requests
import json


url = 'http://localhost:5000/'
headers = {'Content-Type': 'application/json'}


def pretty_print_request(request):
    _0 = '\n'.join(f'{k}: {v}' for k, v in request.headers.items())
    print('\n\n-----------Request----------->\n'
          f'{request.method} {request.url}\n\n{_0}\n\n{request.body}\n')


def pretty_print_response(response):
    _0 = '\n'.join(f'{k}: {v}' for k, v in response.headers.items())
    print('\n<-----------Response-----------\n'
          f'Status code:{response.status_code}\n\n{_0}\n\n{response.text}\n')


def test_post_alice_to_bob_ok():
    payload = {
        "sender": "40e6215d-b5c6-4896-987c-f30f3678f608",
        "receiver": "6ecd8c99-4036-403d-bf84-cf8400f67836",
        "amount": 1.3
    }
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
    pretty_print_request(resp.request)
    pretty_print_response(resp)
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body['message'] == "Done successfully"


def test_post_bob_to_alice_ok():
    payload = {
        "receiver": "40e6215d-b5c6-4896-987c-f30f3678f608",
        "sender": "6ecd8c99-4036-403d-bf84-cf8400f67836",
        "amount": 10.2
    }
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=2))
    pretty_print_request(resp.request)
    pretty_print_response(resp)
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body['message'] == "Done successfully"


def test_post_empty():
    payload = {}
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=2))
    pretty_print_request(resp.request)
    pretty_print_response(resp)
    assert resp.status_code == 422
    resp_body = resp.json()
    assert 'errors' in resp_body


def test_post_bullshit():
    payload = {
        "receiver": "6ecd8c99",
        "sender": 456345,
        "amount": ''
    }
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=2))
    pretty_print_request(resp.request)
    pretty_print_response(resp)
    assert resp.status_code == 422
    resp_body = resp.json()
    assert 'errors' in resp_body


def test_post_zero():
    payload = {
        "receiver": "6ecd8c99-4036-403d-bf84-cf8400f67836",
        "sender": "40e6215d-b5c6-4896-987c-f30f3678f608",
        "amount": 0
    }
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=2))
    pretty_print_request(resp.request)
    pretty_print_response(resp)
    assert resp.status_code == 422
    resp_body = resp.json()
    assert 'errors' in resp_body


def test_post_negative():
    payload = {
        "receiver": "6ecd8c99-4036-403d-bf84-cf8400f67836",
        "sender": "40e6215d-b5c6-4896-987c-f30f3678f608",
        "amount": -123.2
    }
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=2))
    pretty_print_request(resp.request)
    pretty_print_response(resp)
    assert resp.status_code == 422
    resp_body = resp.json()
    assert 'errors' in resp_body


def test_post_insufficient_funds():
    payload = {
        "receiver": "6ecd8c99-4036-403d-bf84-cf8400f67836",
        "sender": "40e6215d-b5c6-4896-987c-f30f3678f608",
        "amount": 123345.2
    }
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=2))
    pretty_print_request(resp.request)
    pretty_print_response(resp)
    assert resp.status_code == 400
    resp_body = resp.json()
    assert 'errors' in resp_body


def test_post_to_unknown():
    payload = {
        "receiver": "0ecd8c99-4036-403d-bf84-cf8400f67836",
        "sender": "40e6215d-b5c6-4896-987c-f30f3678f608",
        "amount": 123.2
    }
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=2))
    pretty_print_request(resp.request)
    pretty_print_response(resp)
    assert resp.status_code == 400
    resp_body = resp.json()
    assert 'errors' in resp_body


def test_post_from_unknown():
    payload = {
        "receiver": "6ecd8c99-4036-403d-bf84-cf8400f67836",
        "sender": "00e6215d-b5c6-4896-987c-f30f3678f608",
        "amount": 123.2
    }
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=2))
    pretty_print_request(resp.request)
    pretty_print_response(resp)
    assert resp.status_code == 400
    resp_body = resp.json()
    assert 'errors' in resp_body