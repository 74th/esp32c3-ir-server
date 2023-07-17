import wifi
import json
import socketpool
import digitalio
import neopixel_write
import time
import array
import pulseio
import digitalio
import board
from adafruit_httpserver import Server, Request, Response
from adafruit_httpserver.status import INTERNAL_SERVER_ERROR_500

IR_SEND_PIN_NO = board.G1
LED_PIN_NO = board.NEOPIXEL

led_pin = digitalio.DigitalInOut(board.NEOPIXEL)
led_pin.direction = digitalio.Direction.OUTPUT


def flash_led(g: int, r: int, b: int):
    neopixel_write.neopixel_write(led_pin, bytearray([g, r, b]))


def run_server():
    pool = socketpool.SocketPool(wifi.radio)
    server = Server(pool, "/static", debug=True)

    @server.route("/api/ir", methods="POST")
    def send_ir_api(request: Request):
        flash_led(0, 255, 0)

        print("access /api/ir")
        print(request.body)
        data = json.loads(request.body)
        pulse = data["pulse"]

        print(pulse)
        send_ir(pulse)

        flash_led(0, 0, 255)

        return Response(request, json.dumps({"success": True}))
    flash_led(0, 0, 255)

    server.serve_forever(str(wifi.radio.ipv4_address))


def send_ir(pulse: list[int]):
    with pulseio.PulseOut(IR_SEND_PIN_NO) as pulseout:
        data = array.array("H", pulse)

        print("send")
        for _ in range(3):
            pulseout.send(array.array("H", data))
            time.sleep(0.025)
        print("send done")


def test_send_ir():
    btn = digitalio.DigitalInOut(board.G3)

    btn.switch_to_input(pull=digitalio.Pull.UP)
    pulseout = pulseio.PulseOut(board.G1)

    led = digitalio.DigitalInOut(board.IO5)
    led.switch_to_output(False)

    btn_status = [True for _ in range(1)]

    data = array.array(
        "H",
        [
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
        ],
    )

    while True:
        time.sleep(0.1)
        if btn_status[0] != btn.value and not btn.value:
            print("send")
            for _ in range(3):
                led.value = True
                pulseout.send(array.array("H", data))
                time.sleep(0.025)
            print("send done")
            time.sleep(1)
            led.value = False


run_server()
