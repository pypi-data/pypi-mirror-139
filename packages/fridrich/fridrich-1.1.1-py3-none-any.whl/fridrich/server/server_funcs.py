"""
defines functions for the Server
(Server)

Author: Nilusink
"""
from fridrich.server.classes import *
from fridrich.classes import FileVar
from fridrich.server import Const
from sys import platform
from os import system
import contextlib
import datetime
import typing
import socket
import json
import time


def send_success(user: User) -> None:
    """
    send the success message to the client
    """
    user.send({'Success': 'Done'})


def check_if(s: str, d: dict, voting: str) -> str:
    """
    if the name is already in the dict, return the name in the dict

    else return the given name ("s")
    """
    if voting in d:
        d = d[voting]
        keys = [d[key] for key in d] + ['Lukas', 'Melvin',
                                        'Niclas']  # keys is (ex.) ['Fridrich', 'Lukas', 'Melvin', 'Niclas]

        for element in keys:
            if s.lower().replace(' ', '') == element.lower().replace(' ', ''):
                return element
        return s
    return s


def get_new_ones(flag: str, vote_instance: FileVar, last_file: str, voting: str) -> list:
    """
    get all attendants which are not in the default name list
    """
    new_ones = list()
    tmp: dict
    match flag:
        case 'now':
            tmp = vote_instance.get()
        case 'last':
            tmp = json.load(open(last_file, 'r'))
        case _:
            raise ValueError(f'"{flag}" is not an option')

    for element in tmp[voting]:
        if not tmp[voting][element] in ['Lukas', 'Niclas', 'Melvin'] + new_ones:
            new_ones.append(tmp[voting][element])

    return new_ones


def reboot() -> None:
    if platform == "win32":
        system("shutdown -r -t 0")
        return
    system("sudo reboot")


class Chat:
    """
    Handler for Chat file
    """

    @staticmethod
    def add(message: str, from_user: str) -> None:
        """
        append a message to the file
        """
        mes = Chat.get()  # get message list from file

        curr_time = datetime.datetime.now()
        formatted_time = curr_time.strftime('%H:%M:%S.%f') + time.strftime(' - %d.%m.%Y')
        mes.append({'time': formatted_time, 'content': message, 'user': from_user})  # append message
        json.dump(mes, open(Const.ChatFile, 'w'), indent=4)  # write message

    @staticmethod
    def get() -> list:
        """
        get all messages
        """
        try:
            mes = json.load(open(Const.ChatFile, 'r'))  # try to read file
        except FileNotFoundError:
            mes = list()  # if file doesn't exist, create new list
        return mes


class Communication:
    """
    Handler for server side communication between Server and Client
    """

    @staticmethod
    def send(client: socket.socket, message: dict | list, encryption=None, key=None) -> None:
        """
        send message to client
        """
        string_mes = json.dumps(message, ensure_ascii=False)
        print(string_mes)
        if encryption:
            mes = encryption(string_mes, key=key)
            # print(mes)
            with contextlib.suppress(OSError, AttributeError):
                client.send(mes)
                print(f'sent to client: {mes}')
            print('failed to send')
            return

        with contextlib.suppress(OSError, AttributeError):
            print(f'sent to client ({client}): {string_mes.encode("utf-8")}')
            client.send(string_mes.encode('utf-8'))

    @staticmethod
    def receive(server: socket.socket, debugging_method, keys: list | typing.Generator
                ) -> typing.Tuple[socket.socket, str] | typing.Tuple[None, None] | bool:
        """
        receive message from client
        """
        # Accept Connection
        try:
            client, address = server.accept()
            del address
            # debug.debug(f'Connected to {address}')
        except OSError:
            return False
        # try to load the message, else ignore it and restart
        mes = client.recv(2048)
        mes = cryption_tools.try_decrypt(mes, keys)

        if not mes:
            debugging_method('Message Error')
            with contextlib.suppress(AttributeError):
                Communication.send(client, {'Error': 'MessageError', 'info': 'Invalid Message/AuthKey'})
                client.close()
            return None, None
        return client, mes
