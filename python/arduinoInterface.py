import serial.tools.list_ports


class ArduinoI:
    def __init__(self, port_num=3, baud_rate=9600):
        self.serialInst = serial.Serial()
        self.use = "COM" + str(port_num)
        self.serialInst.baudrate = baud_rate
        self.serialInst.port = self.use
        self.open()

    def close(self):
        self.serialInst.close()

    def open(self):
        self.serialInst.open()

    def display_number(self, number):
        if not (0 <= int(number) <= 99):
            print('not a 2 digit number')
            number = 0
        try:
            self.serialInst.write(("@" + str(number)).encode('utf-8'))
        except Exception as e:
            raise e

    def change_led_status(self, status):
        self.serialInst.write(str(status).encode('utf-8'))

    def display(self, _input):
        try:
            int_input = int(_input)
            self.display_number(int_input)
        except:
            print("reset")
            self.change_led_status(_input)
def test():

    ports = serial.tools.list_ports.comports()
    serialInst = serial.Serial()
    portsList = []

    for one in ports:
        portsList.append(str(one))
        print(str(one))

    com = input("Select Com Port for Arduino #: ")

    for i in range(len(portsList)):
        if portsList[i].startswith("COM" + str(com)):
            use = "COM" + str(com)
            print(use)

    serialInst.baudrate = 9600
    serialInst.port = use
    serialInst.open()

if __name__ == '__main__':
    # test()


    myArduino = ArduinoI()
    while True:
        _input = input()
        myArduino.display(_input)
