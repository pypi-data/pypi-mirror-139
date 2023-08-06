import can
import CanOpen_Codes
import CanOpen_Callbacks

class CanOpen_Arbitrier:

    def __init__(self, callback: CanOpen_Callbacks.CanOpen_Callbacks):
        self.callbacks: CanOpen_Callbacks.CanOpen_Callbacks = callback

    def can_open_arbitrier(self, message: can.Message):
        msg_arbitrier_id = message.arbitration_id

        if msg_arbitrier_id == CanOpen_Codes.SYNC:
            self.callbacks.sync(message)
        elif ((msg_arbitrier_id > CanOpen_Codes.SDO_RX_BASE_ARB) and (msg_arbitrier_id <= CanOpen_Codes.SDO_RX_MAX_ARB)):
            adress = msg_arbitrier_id - CanOpen_Codes.SDO_RX_BASE_ARB
            self.callbacks.sdo_recv(message, adress, True)
        elif ((msg_arbitrier_id > CanOpen_Codes.PDO1_RX_MIN) and (msg_arbitrier_id <= CanOpen_Codes.PDO1_RX_MAX)):
            adress = msg_arbitrier_id - CanOpen_Codes.PDO1_RX_MIN
            self.callbacks.sdo_recv(message, adress, False)