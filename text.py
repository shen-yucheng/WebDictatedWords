import requests

request = requests.post(
    "http://localhost/pinyin",
    {
        "content": "沈御程 最帅",
        "title": "cat",
    }
)
request.encoding = "utf-8"
print(request.text)
