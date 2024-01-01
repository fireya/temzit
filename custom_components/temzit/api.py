"""Sample API Client."""
from __future__ import annotations

import asyncio
from io import BytesIO

class TemzitApiClientError(Exception):
    """Exception to indicate a general API error."""


class TemzitApiClientCommunicationError(
    TemzitApiClientError
):
    """Exception to indicate a communication error."""


class TemzitApiClientAuthenticationError(
    TemzitApiClientError
):
    """Exception to indicate an authentication error."""



class TemzitApiClient:
    def __init__(self, ip) -> None:
        self.ip = ip
        self.port = 333

    async def fetch_data(self) -> temzit_state:
        reader, writer = await asyncio.open_connection(host=self.ip, port=self.port)
        writer.write(b"\x30\x00")

        # if writer.can_write_eof():
        #     writer.write_eof()

        await writer.drain()

        # better use BytesIO than += if you gonna concat many times
        BytesIO()  # now get server answer
        try:
            data = await reader.read(64)
            if data.__len__() == 0:
                print("Empty response")
            return temzit_state(data)
        except ConnectionAbortedError as exception:
            # if our client was too slow
            raise TemzitApiClientCommunicationError (
                "Error fetching data"
            ) from exception
        except (asyncio.TimeoutError, asyncio.CancelledError) as exception:
            # if server was too slow
             raise TemzitApiClientCommunicationError (
                "Timeout fetching data"
            ) from exception
        finally:
            writer.close()

    async def fetch_settings(self) -> temzit_settings:
        reader, writer = await asyncio.open_connection(host=self.ip, port=self.port)
        writer.write(b"\x34\x00")

        # if writer.can_write_eof():
        #     writer.write_eof()

        await writer.drain()

        # better use BytesIO than += if you gonna concat many times
        BytesIO()  # now get server answer
        try:
            data = await reader.read(64)
            if data.__len__() == 0:
                print("Empty response")
            return temzit_settings(data)
        except ConnectionAbortedError:
            # if our client was too slow
            print("Server timed out connection")
            writer.close()
        except (asyncio.TimeoutError, asyncio.CancelledError):
            # if server was too slow
            print("Did not get answer from server due to timeout")
            writer.close()

class temzit_state:
    def __init__(self, data) -> None:
        self.data = data[2:]

    @property
    def state(self) -> int:
        return self.convert(0, 2)

    @property
    def schedule(self) -> int:
        return self.convert(2, 4)

    @property
    def outdoor_temp(self) -> float:
        return self.convert(4, 6) / 10

    @property
    def indoor_temp(self) -> float:
        return self.convert(6, 8) / 10

    @property
    def hotwater_temp(self) -> float:
        return self.convert(16, 18) / 10

    @property
    def supply_temp(self) -> float:
        return self.convert(8, 10) / 10

    @property
    def return_temp(self) -> float:
        return self.convert(10, 12) / 10

    @property
    def consumption(self) -> float:
        return self.convert(28, 30) / 10

    def convert(self, s: int, e: int) -> int:
        return int.from_bytes(self.data[s:e], byteorder="little", signed=True)


class temzit_settings:
    def __init__(self, data) -> None:
        self.data = data[2:]

    def convert(self, s: int, e: int) -> int:
        return int.from_bytes(self.data[s:e], byteorder="little", signed=True)
