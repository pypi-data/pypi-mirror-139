from serial import Serial
from threading import Thread
from typing import Callable, Union


class BSerial(Serial):
    """Class makes the connection, sends data and receives data from serial port.

    :param Serial: inherits from Serial class
    :type Serial: Serial
    """

    def __init__(self,**kwargs):
        """constructor of Serial. see more information: init from Serial.

        :param \**kwargs: like in init Serial in pyserial.
        :type \**kwargs: see in https://pyserial.readthedocs.io/en/latest/pyserial_api.html.
        
        Example: port='COM3', baudrate=9600 

        """
        super().__init__(**kwargs)

        self.__separator = "-"  # to separate values received
        self.__terminator = "\n"  # to set end line to send values by serial port
        self.__value_received = None  # it is not None when there are data on serial port

    @property
    def terminator(self)->str:
        """It works with write_string_port

        :getter: Return terminator
        :setter: Sets terminator
        :type: str
        """
        return self.__terminator

    @terminator.setter
    def terminator(self, terminator):
        if len(terminator) == 1 and terminator.isascii() and not terminator.isdigit():
            self.__terminator = terminator
        else:
            raise TypeError("Must be a character and not number")

    @property
    def value_received(self)->Union[list, None]:
        """
        get value received after to call start_read_string_port
        
        :return:If there are data in port return a list with values received. If not return None
        :rtype: 
        """
        return self.__value_received

    @property
    def separator(self)->str:
        """It works with start_read_string_port
        
        :getter: Returns separator
        :setter: Sets separator
        :type: str
        """
        return self.__separator

    @separator.setter
    def separator(self, separator:str):
        
        if len(separator) == 1 and separator.isascii() and not separator.digit():
            self.__separator = separator
        else:
            raise TypeError("Must be a character and not number")

    def write_string_port(self,value):
        """write string like bytes in serial port.

        :param value: send value to serial port. It will be converted to string, you have to control it.
        :type value: list or None
        """
        self.write((str(value)+self.__separator).encode())


    def start_read_string_port(self,function:Callable[[list], None]):
        """start read on port

        :param callable: set value to this callable
        :type callable: Callable[[list], None]
        """
        self.__start_thread = True
        self.__thread = Thread(target=self.__Thread_read_port,args=(function, ))
        self.__thread.start()
        print("[LOG] >> Reading data...")


    def stop_read_string_port(self):
        """method to stop receiving values"""
        self.__start_thread = False
        self.__thread.join()
        del(self.start_thread)
        del(self.__thread)
        print("[LOG] >> Connection has been closed.")

    def __Thread_read_port(self,command):
        while self.__start_thread:
            if self.in_waiting > 0:
                try:
                    self.__value_received = (self.readline().decode().replace("\n","")).split(self.__separator)
                    command(self.__value_received)
                except Exception as e:
                    print(f"[ERROR] >> {str(e)}")
            else:
                self.__value_received = None
        
