import ast
import pathlib
from invoke import task
import json
import requests

CIRCUITPY_HOSTNAME = ""
CIRCUITPY_WEB_API_PASSWORD = ""


def select_host(c, host="") -> str:
    if host:
        return host
    elif CIRCUITPY_HOSTNAME:
        return CIRCUITPY_HOSTNAME
    elif c.config.circuitpy_hostname:
        return c.config.circuitpy_hostname
    raise Exception("hostname is not set")


def select_pass(c) -> str:
    return (
        CIRCUITPY_WEB_API_PASSWORD
        if CIRCUITPY_WEB_API_PASSWORD
        else c.config.circuitpy_web_api_password
    )


@task
def upload(c, src="main.py", host="", dst="", code=False):
    host = select_host(host)
    password = select_pass(c)

    if src == "main.py" or code:
        dst = "code.py"
    else:
        dst = src

    cmd = (
        f"curl -v -u :{password} -T {src} -L --location-trusted http://{host}/fs/{dst}"
    )

    print(cmd.replace(password, "********"))

    c.run(cmd)


@task
def mkdir(
    c,
    directory,
    host="",
):
    host = select_host(host)
    password = select_pass(c)

    cmd = f"curl -XPUT -v -u :{password} -L --location-trusted http://{host}/fs/{directory}"

    print(cmd.replace(password, "********"))

    c.run(cmd)


@task
def upload_libs(c, path="lib", host=""):
    for item in pathlib.Path(path).iterdir():
        print(item.as_posix())
        if item.is_dir():
            mkdir(c, f"{item}/", host=host)
            upload_libs(c, path=item, host=host)
            continue
        if item.is_file() and item.suffix in (".mpy", ".py"):
            upload(c, src=item.as_posix(), host=host)


@task
def test_send(c, host=""):
    host = select_host(c, host)

    tv_on = ast.literal_eval(
        "[2403,642,1170,645,588,621,1167,648,588,621,1191,624,588,621,588,621,1167,648,588,621,588,624,585,624,588]"
    )
    living_aircon_off = ast.literal_eval(
        "[210, 8439, 231, 11289, 102, 330, 147, 6939, 267, 17226, 153]"
    )

    data = {
        "pulse": living_aircon_off,
    }
    url = f"http://{host}/api/send_ir"

    print(url)

    res = requests.post(url, json.dumps(data))

    print(f"status: {res.status_code}")
    print("body:")
    print(res.text)


@task
def test_receive(c, host=""):
    host = select_host(c, host)

    url = f"http://{host}/api/receive_ir"

    print(url)

    res = requests.post(url)

    print(f"status: {res.status_code}")
    print("body:")
    print(res.text)
