import serial, json
from state import SimulationState

def send_uart_data(port: str, baudrate: int, state: SimulationState):
    try:
        ser = serial.Serial(port, baudrate, timeout = 1)
        json_data = json.dumps(state)
        ser.write((json_data + '\n').encode('utf-8')) # Append newline for parsing
        ser.close()
    except serial.SerialException as e:
        print(f"UART Error: {e}")