from invoke import task
import json
import requests

CIRCUITPY_HOSTNAME = ""
CIRCUITPY_WEB_API_PASSWORD = ""


@task
def upload(c, p="main.py"):
    host_name = (
        CIRCUITPY_HOSTNAME if CIRCUITPY_HOSTNAME else c.config.circuitpy_hostname
    )
    password = (
        CIRCUITPY_WEB_API_PASSWORD
        if CIRCUITPY_WEB_API_PASSWORD
        else c.config.circuitpy_web_api_password
    )
    if p == "main.py":
        target_path = "code.py"
    else:
        target_path = p

    c.run(
        f"curl -v -u :{password} -T {p} -L --location-trusted http://{host_name}/fs/{target_path}"
    )


@task
def test_send(c):
    host_name = (
        CIRCUITPY_HOSTNAME if CIRCUITPY_HOSTNAME else c.config.circuitpy_hostname
    )

    data = {
        "pulse": [
            2403,
            642,
            1170,
            645,
            588,
            621,
            1167,
            648,
            588,
            621,
            1191,
            624,
            588,
            621,
            588,
            621,
            1167,
            648,
            588,
            621,
            588,
            624,
            585,
            624,
            588,
        ]
    }
    url = f"http://{host_name}/api/send_ir"

    print(url)

    res = requests.post(url, json.dumps(data))

    print(f"status: {res.status_code}")
    print("body:")
    print(res.text)

@task
def test_receive(c):
    host_name = (
        CIRCUITPY_HOSTNAME if CIRCUITPY_HOSTNAME else c.config.circuitpy_hostname
    )

    url = f"http://{host_name}/api/receive_ir"

    print(url)

    res = requests.post(url)

    print(f"status: {res.status_code}")
    print("body:")
    print(res.text)
