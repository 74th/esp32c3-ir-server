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

IR_SEND_PIN_NO = board.G1
IR_RECEIVE_PIN_NO = board.G0
LED_PIN_NO = board.NEOPIXEL

led_pin = digitalio.DigitalInOut(board.NEOPIXEL)
led_pin.direction = digitalio.Direction.OUTPUT

pulsein = pulseio.PulseIn(IR_RECEIVE_PIN_NO, maxlen=120, idle_state=True)
pulsein.pause()

def flash_led(g: int, r: int, b: int):
    neopixel_write.neopixel_write(led_pin, bytearray([g, r, b]))


def run_server():
    pool = socketpool.SocketPool(wifi.radio)
    server = Server(pool, "/static", debug=True)

    @server.route("/api/send_ir", methods="POST")
    def send_ir_api(request: Request):
        flash_led(0, 255, 0)

        print("access /api/send_ir")
        print(request.body)
        data = json.loads(request.body)
        pulse = data["pulse"]

        print(pulse)
        send_ir(pulse)

        flash_led(0, 0, 255)

        res = {"success": True}
        return Response(request, json.dumps(res))

    @server.route("/api/receive_ir", methods="POST")
    def receive_ir_api(request: Request):
        flash_led(0, 255, 0)
        print("access /api/receive_ir")

        pulses = receive_ir()

        flash_led(0, 0, 255)

        res = {
            "success": len(pulses) > 0,
            "data": {
                "pulses": pulses,
            }
        }

        return Response(request, json.dumps(res))

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


def receive_ir() -> list[int]:
    timeout = 10

    pulses = []

    start = time.monotonic()
    is_received = False
    pulsein.clear()
    pulsein.resume()
    while not is_received and (time.monotonic() - start) < timeout:
        time.sleep(0.1)
        while pulsein:
            pulse = pulsein.popleft()
            pulses.append(pulse)
            is_received = True
    pulsein.pause()

    if pulses is None:
        print("cannot receive pulses")
    else:
        print("Heard", len(pulses), "Pulses:", pulses)

    return pulses


run_server()
