class URLLib3Transport(httpx.BaseTransport):
    def __init__(self):
        self.pool = urllib3.PoolManager()

    def handle_request(self, request: httpx.Request):
        payload = json.loads(request.content.decode("utf-8").replace("'",'"'))
        urllib3_response = self.pool.request(request.method, str(request.url), headers=request.headers, json=payload)  # Convert httpx.URL to string
        content = json.loads(urllib3_response.data.decode('utf-8'))  # Decode the data and load as JSON
        stream = httpx.ByteStream(json.dumps(content).encode("utf-8"))  # Convert back to JSON and encode
        headers = [(b"content-type", b"application/json")]
        return httpx.Response(200, headers=headers, stream=stream)
