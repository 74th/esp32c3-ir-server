# IR Server M5StampC3

M5StampC3 で WebServer を立てて、赤外線信号を JSON 形式で POST すると、送信してくれるやつ。

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

## LICENSE

MIT

### imported

- adafruit_httpserver (MIT): https://github.com/adafruit/Adafruit_CircuitPython_HTTPServer
