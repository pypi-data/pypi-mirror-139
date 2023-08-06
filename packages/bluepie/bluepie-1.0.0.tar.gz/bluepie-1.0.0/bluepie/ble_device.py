import asyncio
from asyncio.exceptions import TimeoutError
from .logs import Logs


import bleak
from bleak import BleakClient
from bleak.exc import BleakError, BleakDBusError
from typing import Callable


class BLEDevice(object):
    """
    Main class for BLE device.

    We can:
    - connect to a BLE device
    - disconnect from it
    - get its BLE services
    - write to its characteristics
    - read from its characteristics
    """

    def __init__(self, mac_addr: str, enable_logs: bool = False) -> None:
        """Creates an BLEDevice object.

        Args:
            mac_addr (str): MAC address of the BLE device
            enable_logs (bool): whether the logs should be enabled
        """

        self.mac_addr = mac_addr
        self.loop = asyncio.get_event_loop()
        self.client = BleakClient(mac_addr, loop=self.loop)
        self.log = Logs(enable=enable_logs)

    def __del__(self) -> None:
        """Destructor."""
        self.disconnect()
        self.loop.close()

    def connect(self, timeout: int = 3) -> bool:
        """Connects to a BLE device in a blocking fashion.

        Args:
            timeout (int): After how many seconds the function should time out
            in case of unsuccessful connection.

        Raises:
            BleakError: In case there is a problem with Bleak library
            TimeoutError: If the connection to a device timed out

        Returns:
            True if device was connected to, otherwise false.
        """

        async def async_connect():
            await self.client.connect(timeout=timeout)

        try:
            self.loop.run_until_complete(async_connect())

        except (BleakError, TimeoutError, BleakDBusError) as e:
            self.log.warning(f"Failed to connected to the device {self.mac_addr}")
            return False

        self.log.info(f"Connected to the device {self.mac_addr}")
        return True

    def disconnect(self) -> None:
        """Disconnect from the device in a blocking fashion."""

        async def async_disconnect():
            await self.client.disconnect()

        try:
            self.loop.run_until_complete(async_disconnect())
            self.log.info(f"Disconnected from device {self.mac_addr}")

        # Rich logger does not like it if we exit quickly, this is just to
        # ignore the error.
        except ImportError:
            pass

        except BleakError as e:
            self.log.exception(e)

    def get_services(self) -> bleak.backends.service.BleakGATTServiceCollection:
        """Gets all services that are registered for this device.

        Suitable for custom processing

        Returns:
                A bleak.backends.service.BleakGATTServiceCollection with this
                device’s services tree.
        """

        async def async_get_services():
            return await self.client.get_services()

        return self.loop.run_until_complete(async_get_services())

    def list_services(self) -> list:
        """List all device characteristics.

        Suitable for simple info enquiry

        Returns: A list of dicts, where each dicts represents one
                service.
                Each service contains:
                    - UUID
                    - List of characteristic dicts

                Each characteristic dict contains:
                    - UUID
                    - Handle
                    - Properties
                    - Name (description)
        """

        services = []

        for service in self.get_services():
            service_dict = {"uuid": service.uuid, "characteristics": []}
            for char in service.characteristics:
                # https://bleak.readthedocs.io/en/latest/api.html?highlight=connect#bleak.backends.characteristic.BleakGATTCharacteristic
                char_dict = {
                    "UUID": char.uuid,
                    "Handle": hex(char.handle),
                    "Properties": char.properties,
                    "Name": char.description,
                }
                service_dict["characteristics"].append(char_dict)
            services.append(service_dict)

        return services

    def handle_rx(self, _: int, data: bytearray):
        # print("Received: ",data)
        print(data.decode("utf-8"), end="", flush=True)

    def write_characteristic(self, uuid: str, data: bytearray) -> None:

        """Writes to a characteristic in a blocking fashion.

        Args:
            uuid (str): String representation of UUID, something like:
            6E400001-B5A3-F393-E0A9-E50E24DCCA9E
            data (bytearray): Data to be written, strings can be written like
            so:
                device.write_characteristic(SOME_UUID, some_string.encode())
        """

        async def async_write():
            await self.client.write_gatt_char(
                char_specifier=uuid, data=data, response=False
            )

        self.loop.run_until_complete(async_write())

    def read_characteristic(self, uuid: str) -> bytearray:
        """Reads from a characteristic in a blocking fashion.


        Returns: bytearray object, which can be converted into a string like so:
            data = device.read_characteristic(SOME_UUID)
            message = data.decode()
        """

        async def async_read():
            return await self.client.read_gatt_char(char_specifier=uuid)

        return self.loop.run_until_complete(async_read())

    def start_notify(self, uuid: str, callback) -> None:
        """Starts notifications on given UUID characteristic.

        Given callback is called with received data.

        Args:
            uuid (str): characteristic UUID
            callback (Callable[[int, bytearray], None]): callback
        """

        async def async_notify_enable():
            await self.client.start_notify(uuid, callback)

        self.loop.run_until_complete(async_notify_enable())

    def stop_notify(self, uuid: str) -> None:
        """Stops notifications on given UUID characteristic

        Args:
            uuid (str): characteristic UUID
        """

        async def async_stop_notify():
            await self.client.stop_notify(uuid)

        self.loop.run_until_complete(async_stop_notify())


#     def callback_func(
#         self, sender, data
#     ):  # callback defines what happens with received data
#         """Prints device response to standard output"""
#         response = f"{sender}: {data}"
#         # print(f"Received callback: {response}")

#     def get_connection_lost(self):
#         return self.connection_lost


#     def start_notify(self, uuid, callback):
#         async def async_start_notify():
#             await self.client.start_notify(
#                 uuid, callback
#             )  # to get response from device we have to subscribe to notify

#         self.loop.run_until_complete(async_start_notify())

#     def stop_notify(self, uuid):
#         async def async_stop_notify():
#             await self.client.stop_notify(uuid)

#         self.loop.run_until_complete(async_stop_notify())

#     def send_receive_message(self, msg):
#         """Subscribes to notifications of device, sends message and waits for response"""
#         try:
#             response_msg = io.StringIO()

#             async def async_send_receive_message():
#                 with redirect_stdout(
#                     response_msg
#                 ):  # bad workaround for capturing callback prints - what to do?
#                     data = bytearray(msg, encoding="utf8")
#                     await self.client.write_gatt_char(
#                         _uuid=CHAR_WRITE, data=data, response=True
#                     )
#                     # print("Model Number: {0}".format("".join(map(chr, resp))))
#                     await asyncio.sleep(
#                         0.5, loop=self.loop
#                     )  # sleep to make sure response is not missed

#             self.loop.run_until_complete(async_send_receive_message())
#             response = response_msg.getvalue()
#             # print(response)
#             return response
#         except:
#             return None

#     def send_message(self, msg):
#         try:

#             async def async_send_message():
#                 # data = bytearray(msg, encoding='utf8')
#                 await self.client.write_gatt_char(CHAR_WRITE, msg, response=True)

#             self.loop.run_until_complete(async_send_message())
#             # print("write success")
#         except Exception as e:
#             logging.error(f"An exception occured during send message: {e}")
#             return None

#     def read_characteristic(self, uuid):
#         try:
#             # response_msg = io.StringIO()
#             async def async_read_characteristic():
#                 # with redirect_stdout(response_msg):  # bad workaround for capturing callback prints - what to do?
#                 ret = await self.client.read_gatt_char(uuid)
#                 # print(f"Read: {ret}")
#                 # print("Model Number: {0}".format("".join(map(chr, resp))))
#                 await asyncio.sleep(
#                     0.5, loop=self.loop
#                 )  # sleep to make sure response is not missed
#                 return ret

#             return self.loop.run_until_complete(async_read_characteristic())
#         except BleakError as e:
#             self.connection_lost = True
#             logging.error(f"A BleakError occured during reading of characteristic: {e}")
#             return None
#         except Exception as e:
#             logging.error(f"An exception occured during reading of characteristic: {e}")
#             return None
