from .ble_device import BLEDevice

import asyncio

NUS_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
NUS_RX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
NUS_TX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


class NUSDevice(BLEDevice):
    """
    NUS device class which is derived from BLE device class

    With it we can:
    - Send strings to the device
    - Receive strings from the device
    """

    def __init__(
        self,
        mac_addr: str,
        max_lines_read: int,
        eol: str = "\r\n",
        enable_logs: bool = False,
    ):
        """Creates instance of NUSDevice class.

        Instance will enable notifications on NUS_TX_UUID characteristic.

        Before using any of the public methods we should be connected to the
        device.

        Args:
            mac_addr (str): MAC address of the BLE device
            max_lines_read (int): how many lines will method nus_read_lines try
            to read by default.
            eol (str): End of line character. String terminated of it is defined
            as a line in this file.
            enable_logs (bool): whether the logs should be enabled
        """

        super().__init__(mac_addr, enable_logs)
        self.eol = eol
        self.max_lines_read = max_lines_read
        self.queue = asyncio.Queue()

    def __del__(self) -> None:
        """Destructor."""
        self.disconnect()

    def _receive_notify_enable(self) -> None:
        """Enables notifications on NUS_TX_UUID characteristic."""

        async def async_handle_rx(_, data):
            await self.queue.put(data)

        super().start_notify(NUS_TX_UUID, async_handle_rx)

    def _receive_notify_disable(self) -> None:
        """Disables notifications on NUS_TX_UUID characteristic."""

        super().stop_notify(NUS_TX_UUID)

    def connect(self, timeout: int = None) -> bool:
        """Connects to the Nus device and enables notifications.

        Args:
            timeout (int): connection timeout

        Returns:
            True if connected succesfully, otherwise false.
        """

        if super().connect(timeout):
            self._receive_notify_enable()
            return True
        else:
            return False

    def disconnect(self) -> bool:
        """Disconnects from the NUS device.

        Args:
            timeout (int): connection timeout

        Returns:
            True if connected succesfully, otherwise false.
        """
        if self.client.is_connected:
            self._receive_notify_disable()
            super().disconnect()

    def nus_send(self, line: str):
        """Sends line string over NUS.

        Args:
            line (str): string that will be sent
        """
        # We clean queue before sending out line, as we do not care
        # about previous unproccessed responses
        self._clean_queue()

        line += self.eol
        super().write_characteristic(NUS_RX_UUID, line.encode())

    def _clean_queue(self) -> None:
        """Cleans out the queue, by throwing away all items in it."""

        while True:
            try:
                self.queue.get_nowait()
            except asyncio.QueueEmpty:
                break

    def nus_read_lines(self, max_lines_read: int = None, timeout: int = 0.4) -> list:
        """Reads a number of lines over NUS.

        Function will wait for __timeout__ seconds after each received
        NUS TX notification before processing received content.

        Received content is then processed, up to a max number of lines are
        extracted and returned in a list.

        The rest of the content is discarded.

        If none of the function arguments are given then the ones specified in
        __init__ are used.

        Args:
            num_lines_read (int): how many lines to read
            timeout (int): how long to wait after each received TX notification

        Returns:
            List of read lines, can be an empty list if no lines were read.
        """

        if not max_lines_read:
            max_lines_read = self.max_lines_read

        async def read_all():
            temp_buf = ""
            try:
                while True:
                    # get item from queue
                    item = await asyncio.wait_for(self.queue.get(), timeout)

                    # decode it and concentate it to temporary_buffer
                    temp_buf += item.decode()

            except asyncio.TimeoutError:
                pass

            # Return out only full lines, if max lines were read return them,
            # otherwise return as many as you can
            lines = temp_buf.split(self.eol)

            if temp_buf.count(self.eol) >= max_lines_read:
                return lines[:max_lines_read]
            else:
                return lines[:-1]

        return self.loop.run_until_complete(read_all())
