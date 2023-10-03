import ast
import pathlib
import time
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
    host = select_host(c, host)
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
    host = select_host(c, host)
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
def test_send(c, host="", delay=0):

    if delay:
        time.sleep(delay)
    host = select_host(c, host)

    tv_on = ast.literal_eval(
        "[2403,642,1170,645,588,621,1167,648,588,621,1191,624,588,621,588,621,1167,648,588,621,588,624,585,624,588]"
    )
    living_aircon_off = ast.literal_eval(
        "[3474,1703,437,1281,437,1278,437,422,437,421,437,421,437,1279,437,422,437,421,437,1281,437,1277,438,421,437,1280,437,422,436,422,436,1279,438,1281,437,421,437,1278,437,1281,437,420,436,422,437,1279,437,422,436,422,436,1280,437,422,436,422,437,422,436,422,436,422,436,422,436,424,436,422,436,423,435,421,436,424,436,422,436,423,435,423,435,421,436,423,435,423,435,424,434,424,435,424,435,424,434,423,434,425,435,424,434,424,434,424,434,1281,435,1281,435,424,434,1282,435,423,435,1282,434,1282,435,424,434,424,434,424,434,424,434,425,434,424,434,424,434,1282,434,1284,435,423,433,425,434,424,433,425,434,424,434,426,434,424,434,425,433,1281,434,1283,434,424,434,1284,434,423,433,426,433,425,433,425,433,425,433,425,434,426,433,426,433,423,433,426,432,426,433,425,433,425,433,427,433,425,433,426,432,424,433,426,432,426,433,425,433,427,433,424,433,425,433,425,433,425,433,426,432,426,432,426,433,427,432,425,432,428,432,1282,433,426,432,426,432,426,433,426,432,1284,432,426,433,426,432,426,432,426,432,426,433,426,432,426,432,426,432,426,432,426,433,426,432,428,432,424,432,427,432,426,432,426,432,426,433,426,432,426,432,426,432,427,431,1286,432,1283,432,428,432,1283,432,427,431,427,432,426,432,13299,3441,1710,433,1283,432,1285,433,426,432,425,432,426,432,1284,432,427,432,427,432,1283,432,1285,432,428,431,1284,431,429,431,427,431,1284,431,1285,432,427,431,1285,431,1286,431,428,432,427,431,1285,431,426,431,427,431,1286,431,427,431,427,432,427,431,427,431,427,431,427,432,427,431,427,431,427,431,427,431,428,431,427,431,427,431,427,432,427,431,427,431,427,431,427,432,427,431,427,431,427,431,427,431,428,431,427,431,427,431,428,431,1309,407,1287,431,427,431,1308,407,428,430,1310,407,1311,407,426,431,428,430,453,407,451,407,452,406,450,407,453,407,1308,406,1310,407,452,406,452,406,452,407,452,406,452,406,452,407,451,406,452,407,1310,406,1312,406,451,406,1310,407,453,406,451,406,451,407,452,406,452,407,452,406,452,406,452,406,452,406,453,406,452,406,452,406,452,407,453,407,451,406,451,406,454,406,451,406,452,406,452,406,452,406,453,406,452,406,452,406,452,406,453,406,452,406,452,406,453,405,454,406,452,406,1310,405,453,406,454,406,452,406,452,406,1309,406,452,406,452,406,453,406,452,406,454,405,453,405,452,405,454,406,451,406,453,405,453,405,453,405,453,406,452,406,453,405,453,405,453,406,452,406,453,405,453,405,455,405,1310,405,1311,406,452,406,1311,405,453,406,453,405,453,405,1024]"
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
