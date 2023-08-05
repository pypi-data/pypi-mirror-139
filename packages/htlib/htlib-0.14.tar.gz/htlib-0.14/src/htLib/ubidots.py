"""
This module offers clients to send and receive data.
This module consumes the Ubidots API, you can find more examples of the data that is sent or received in the following link
https://docs.ubidots.com/v1.6/reference/welcome

This tool is still in development so you may encounter some errors or missing methods to perform certain actions.
This will improve as needed based on the projects we carry out or based on the orders in the repository.

At this time you can create clients that use the http and tcp protocols.

"""
from requests import post, get
from threading import Thread
from typing import Union, Tuple 


class HTTPClient:
    """
    This class offers connections to Ubidots platform using Http procotol.
    """
    def __init__(self,token):
        """
        
        :param token: token of your ubidots account
        :type token: str
        """

        self.__HEADERS = {'X-Auth-Token':token, "Content-Type":"application/json"}


    def __send_values(self, data:dict, link:str):
        
        try:
            rpta = post(link, headers=self.__HEADERS, data=data)

            if rpta.status_code == 200:
                print("[OK] >> Data has been sended successfully")
            elif rpta.status_code == 400:
                print("[ERROR] >> Incorrect Request, verify labels names")
            elif rpta.status_code == 401:
                print("[ERROR] >> Unauthorized")
        
        except Exception as e:
            print(f"[ERROR] >> {str(e)}")

    def send__to_device(self, device_label:str, data:dict, block=False):
        """Sends data to one or more variables on a Device

        :param device_label: device label. You can find it in yoyur ubidots account
        :type device_label: str
        :param data: dictionary of data {"variable_label1":1, "variable_label2": 3}. See more examples in https://docs.ubidots.com/v1.6/reference/send-data-to-a-device
        :type data: dict
        :param block: If It's False send data in a Thread, defaults to False
        :type block: bool, optional
        """
        link = f"https://industrial.api.ubidots.com/api/v1.6/devices/{device_label}/"
        if block:
            self.__send_values(data, link)
        else:
            Thread(target=self.__send_values, args=(data, link)).start()

    def send_to_variable(self, device_label:str, variable_label:str, data:dict, block=False):
        """Sends data to a variable on a Device

        :param device_label: device label. You can find it in your ubidots account
        :type device_label: str
        :param variable_label: variable label. You can find it in your ubidots account
        :type variable_label: str
        :param data: dictionary of values to variable {"value":10}. See more examples in https://docs.ubidots.com/v1.6/reference/send-data-to-a-variable
        :type data: dict
        :param block: If It's False send data in a Thread, defaults to False
        :type block: bool, optional
        """
        
        link = f"https://industrial.api.ubidots.com/api/v1.6/devices/{device_label}/{variable_label}/values"
        
        if block:
            self.__send_values(data, link)
        else:
            Thread(target=self.__send_values, args=(data, link)).start()


    def send_to_variable_by_id(self, variable_id:str, data:dict, block=False):
        """ send to specific variable based on id
        
        :param variable_id: variable id . You can find it in your ubidots account
        :type variable_id: str
        :param data: dictionary of values to variable {"value":10}. See more examples in https://docs.ubidots.com/v1.6/reference/send-data-to-a-device-1
        :type data: dict
        :param block: If It's False send data in a Thread, defaults to False
        :type block: bool, optional 
        """
        link = f"https://industrial.api.ubidots.com/api/v1.6/variables/{variable_id}/values"
        if block:
            self.__send_values(data, link)
        else:
            Thread(target=self.__send_values, args=(data, link)).start()

    def __get_values(self, link):
        try:
            rpta = get(link, headers=self.__HEADERS)

            if rpta.status_code == 200:
                print("[OK] >> Data has been sended successfully")
                return False, None
            elif rpta.status_code == 400:
                print("[ERROR] >> Incorrect Request, verify labels names")
                return False, None
            elif rpta.status_code == 401:
                print("[ERROR] >> Unauthorized")
                return False, None
            return True, rpta.json()

        except Exception as e:
            print(f"[ERROR] >> {str(e)}")
            return False, None

    def get_from_device(self):
        pass

    def get_from_variable(self, device_label:str, variable_label:str):
        if block:
            self.__get_values()
        else:
            Thread(target=self.__get_values, args=(device_label, variable_label)).start()
        
    def get_from_variable_by_id(self, variable_id:str)->Tuple[bool, Union[dict, None]]:
        """ get data of variable based on id
        
        :param variable_id: variable id . You can find it in your ubidots account
        :type variable_id: str

        
        :return: Tuple with 2 items, the first element indicates if there was an error the second element contains a dictionary if there was no error
        :rtype: tuple 
        """
        link = f"https://industrial.api.ubidots.com/api/v1.6/variables/{variable_id}/values" 
        self.__get_values(link)


class TCPClient:
    """
    This class offers connections to Ubidots platform using Http procotol.
    """
    def __init__(self, token:str):
        """
        
        :param token: token of your ubidots account
        :type token: str
        """
        self.__token = token
        self.user_agent = "PYTHON/1.0"
        self.__host = "industrial.api.ubidots.com"
        self.__port = 9012

    def connect(self):
        """start the connection"""
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.connect((self.__host,self.__port))

    def disconnect(self):
        """close the connection"""
        self.__socket.close()

    def __send_data_thread(self, mssg:str):
        try:
            self.__socket.sendall(mssg.encode())
            print(f"[LOG] >> {self.__socket.recv(4096).decode()}")
        except Exception as e:
            print(f"[ERROR] >> {str(e)}")

    def send_data(self,data:dict, variable_label:str, block=False):
        """
        
        :param data: data to will be sended {"variable_label":value}. See more examples in https://docs.ubidots.com/v1.6/reference/sending-data-2
        :type data: dict

        :param variable_label: Check It in your ubidots account
        :type variable_label: str

        :param block: If It's True send data in Thread, defaults to False
        :type block: bool

        """
        
        data = ','.join([f"{key}:{item}" for key, item in data.items()])
        msg = f"{self.user_agent}|POST|{self.token}|{self.device_label}=>[{data}|end"
            
        if block:
            Thread(target=self.__send_data_thread, args=(mssg, )).start()
        else:
            self.__send_data_thread(mssg)
        

    def rcv_data(self,variable_label:str)->Tuple[bool,Union[float, None]]:
        """ receive data
        
        :param variable_label: variable label. Check it in your ubidots account
        :type variable_label: str
 
        :return: Tuple with 2 items, the first element indicates if there was an error the second element contains a float value if there was no error
        :rtype: tuple
        """
        try:
            msg = f"{self.user_agent}|LV|{self.token}|{self.device_label}:{variable_label}|end"
            self.socket.sendall(msg.encode())
            data = self.socket.recv(1023).decode()
            datas = [t for t in list(data) if t.isdigit()]
            datas = "".join(datas)
            return True, float(datas)
        except Exception as e:
            print(f"[ERROR] >> {str(e)}")
            return False, None


def get_client(token:str, client:str)->Union[HTTPClient, TCPClient, None]:
    """get a Client
    
    :param token: token of your ubidots account
    :type token: str
    :param client: type of client. Could be tcp, http
    :type client: str

    :return: a Client to Ubidots API. If client doesn't exist return None
    :rtype: HTTPClient, TCPClient, None
    """
    if client == "tcp":
        return TCPClient(token)
    elif client == "http":
        return HTTPClient(token)
    else: return None

