from threading import Thread
from smtplib import SMTP


class Email:
    """This class offers method to send a email of a easy mode"""
    def __init__(self,email,password):
        """

        :param email: user email.
        :type email: str
        :param password: user password.
        :type password: str
        """

        self.__email = email
        self.__password = password


    def send_email(self,dest,message="email from python",server="smtp.live.com",port=587, block=False):
        """Send a email. defaults It works with gmail

        :param dest: Destination email.
        :type dest: str
        :param message: messsage to send, defaults to "email from python"
        :type message: str, optional
        :param server: server email, defaults to "smtp.live.com"
        :type server: str, optional
        :param port: port email, defaults to 587
        :type port: int, optional
        :param block: if it's True execute in Thread
        :type block: bool, optional
        """
        if not block:
            t = Thread(target=self.__thread_send_email,args=(dest,message,server,port))
            t.start()
        else:
            self.__thread_send_email(dest, message, server, port)

    def __thread_send_email(self,dest,message,server,port):
        message = '\n'+message
        try:
            with SMTP(server,port) as server:
                server.ehlo() 
                server.starttls() 
                server.login(self.__email,self.__password)
                server.sendmail(self.__email,dest,message)
                server.quit()
        except Exception as e:
            print(f"[RROR] = {str(e)}")
