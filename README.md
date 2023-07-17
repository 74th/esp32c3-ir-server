# IR Server M5StampC3

<img src="docs/photo.jpg" width="300px" />

M5StampC3 で WebServer を立てて、赤外線信号を JSON 形式で POST すると、送信してくれるやつ。

CircuitPyhon 上に実装。

```python
import requests

data = {
    "pulse": [ 2403, 642, 1170, 645, 588, 621, 1167, 648, 588,
        621, 1191, 624, 588, 621, 588, 621, 1167, 648, 588, 621, 588,
        624, 585, 624, 588,
    ]
}

url = f"http://{host_name}/api/ir"

res = requests.post(url, json.dumps(data))

print(f"status: {res.status_code}")
print("body:")
print(res.text)
```

## 必要なもの

- M5Stamp C3 Mate https://www.switch-science.com/products/7474
- M5Stack 用赤外線送受信ユニット https://www.switch-science.com/products/5699

## install

CIRCUIT PYTHON: https://circuitpython.org/board/m5stack_stamp_c3/

ファームウェアやコードのアップロードの方法など https://learn.adafruit.com/circuitpython-with-esp32-quick-start

ESP32-C3 は USB デバイス機能はないため、CIRCUIT PYTHON のファームウェアを焼いた後は、HTTP 経由でコードをアップロードする。

https://learn.adafruit.com/circuitpython-with-esp32-quick-start/setting-up-web-workflow

main.py を code.py としてアップロードする。

## LICENSE

MIT

### imported

- adafruit_httpserver (MIT): https://github.com/adafruit/Adafruit_CircuitPython_HTTPServer
