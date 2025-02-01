import httpx


async def send(method, url, verify: bool = True, **kwargs):
    # 60.0: Tổng thời gian cho phép cho toàn bộ yêu cầu.
    # connect=10.0: Thời gian tối đa cho phép để thiết lập kết nối tới server.
    timeout = httpx.Timeout(60.0, connect=10.0)
    transport = httpx.AsyncHTTPTransport(retries=3)

    # Tạo AsyncClient với tham số 'verify'
    async with httpx.AsyncClient(timeout=timeout, transport=transport, http2=True, verify=verify) as client:
        response = await client.request(method, url, **kwargs)

    return response


async def get(url, params: dict = None, data: dict = None, json: dict = None, headers: dict = None, follow_redirects: bool = True, verify: bool = True, content: bytes = None):
    return await send(method="GET", url=url, params=params, data=data, json=json, headers=headers, follow_redirects=follow_redirects, verify=verify, content=content)


async def post(url, params: dict = None, data: dict = None, json: dict = None, headers: dict = None, files=None, follow_redirects: bool = True, verify: bool = True):
    return await send(method="POST", url=url, params=params, data=data, json=json, headers=headers, files=files, follow_redirects=follow_redirects, verify=verify)


async def put(url, params: dict = None, data: dict = None, json: dict = None, headers: dict = None, verify: bool = True):
    return await send(method="PUT", url=url, params=params, data=data, json=json, headers=headers, verify=verify)


async def delete(url, params: dict = None, data: dict = None, json: dict = None, headers: dict = None, verify: bool = True):
    return await send(method="DELETE", url=url, params=params, data=data, json=json, headers=headers, verify=verify)
