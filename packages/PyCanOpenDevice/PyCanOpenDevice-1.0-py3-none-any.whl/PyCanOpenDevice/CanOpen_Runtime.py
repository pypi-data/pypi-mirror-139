import can
import CanOpen_Callbacks, CanOpen_Arbitrier, CanOpen_BusActions,CanOpen_Receiver

class CanOpen_Runtime:
    def __init__(self, bus: can.Bus):
        self.heartbeat_task = None
        bus_actions = CanOpen_BusActions.CanOpen_BusActions(bus)
        callbacks = CanOpen_Callbacks.CanOpen_Callbacks(bus_actions)
        arbitrier = CanOpen_Arbitrier.CanOpen_Arbitrier(callbacks)
        receiver = CanOpen_Receiver.CanOpen_Receiver(bus, arbitrier)

    def setHeartbeatTask(self, heartbeat_task):
        self.heartbeat_task = heartbeat_task

