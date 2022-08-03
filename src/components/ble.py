import time

from adafruit_ble import BLERadio
from adafruit_bluefruit_connect.packet import Packet



class BLE(BLERadio):
    def advertisement_test(self):
        from adafruit_ble.advertising.standard import Advertisement
        advertisement = Advertisement()
        advertisement.short_name = "HELLO"
        advertisement.connectable = True

        while True:
            print(advertisement)
            self.start_advertising(advertisement, scan_response=b"")
            while not self.connected:
                pass
            print("connected")
            while self.connected:
                pass
            print("disconnected")

    def deviceinfo_service(self):
        """
        This example does a generic connectable advertisement and prints out the
        manufacturer and model number of the device(s) that connect to it.
        """
        from adafruit_ble.services.standard.device_info import DeviceInfoService

        a = Advertisement()
        a.connectable = True
        self.start_advertising(a)

        # Info that the other device can read about us.
        my_info = DeviceInfoService(manufacturer="CircuitPython.org", model_number="1234")

        print("advertising")

        while not self.connected:
            pass

        print("connected")

        while self.connected:
            for connection in self.connections:
                if not connection.paired:
                    connection.pair()
                    print("paired")
                print(connection, connection.connected)
            time.sleep(5)

        print("disconnected")

    def uart_service(self):
        from adafruit_ble.services.nordic import UARTService

        SEND_RATE = 10  # how often in seconds to send text

        uart_server = UARTService()
        advertisement = ProvideServicesAdvertisement(uart_server)

        count = 0
        while True:
            print("WAITING...")
            # Advertise when not connected.
            self.start_advertising(advertisement)
            while not self.connected:
                pass

            # Connected
            self.stop_advertising()
            print("CONNECTED")

            # Loop and read packets
            last_send = time.monotonic()
            while self.connected:
                # INCOMING (RX) check for incoming text
                if uart_server.in_waiting:
                    raw_bytes = uart_server.read(uart_server.in_waiting)
                    text = raw_bytes.decode().strip()
                    # print("raw bytes =", raw_bytes)
                    print("RX:", text)
                # OUTGOING (TX) periodically send text
                if time.monotonic() - last_send > SEND_RATE:
                    text = "COUNT = {}\r\n".format(count)
                    print("TX:", text.strip())
                    uart_server.write(text.encode())
                    count += 1
                    last_send = time.monotonic()

            # Disconnected
            print("DISCONNECTED")

    def uart2(self):
        from adafruit_ble.advertising.standard import ProductServicesAdvertisement
        from adafruit_ble.services.nordic import UARTService
        from adafruit_bluefruit_connect.color_packet import ColorPacket

        uart_server = UARTService()
        advertisement = ProvideServicesAdvertisement(uart_server)

        while True:
            # Advertise when not connected.
            self.start_advertising(advertisement)
            while not self.connected:
                pass

            while self.connected:
                packet = Packet.from_stream(uart_server)
                if isinstance(packet, ColorPacket):
                    print(packet.color)

    def scan(self):
        from adafruit_ble.advertising.standard import Advertisement, ProvideServicesAdvertisement

        print("scanning")
        found = set()
        scan_responses = set()
        devices = {}
        for advertisement in self.start_scan(ProvideServicesAdvertisement, Advertisement):
            addr = advertisement.address
            if advertisement.scan_response and addr not in scan_responses:
                scan_responses.add(addr)
            elif not advertisement.scan_response and addr not in found:
                found.add(addr)
            else:
                continue

            if advertisement.connectable:
                print("found connectable device", addr, advertisement)
            else:
                print("found non-connectable device", addr, advertisement)
            print()
        print("scan done")
        return found, scan_responses


def test_ble():
    ble = BLE()
    ble.deviceinfo_service()


if __name__ == "__main__":
    test_ble()