
import os
import subprocess
import time
import re
import json
import glob
from threading import Thread
from smbus2 import SMBus, i2c_msg


from remoteCtrlServer.httpserver import start_server_in_thread
remCtrlPort = 8080
NOTES_FILE = "notes.txt"
i2cBus = 1


class Main:
    def __init__(self):
        print("Run app...")
        self.server, self.server_thread = start_server_in_thread(remCtrlPort, self.remCtrlCB, self) #Start remote control server
        self.bus = SMBus(i2cBus)
        self.notes = "empty"
        self.run()
    def run(self):
        while(True):
            time.sleep(1)
            pass
    def load_notes_from_file(self):
        """Завантажує нотатки з файлу, якщо файл існує."""
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r", encoding="utf-8") as file:
                return file.read()
        return "empty"

    def save_notes_to_file(self, notes):
        """Зберігає нотатки у файл."""
        with open(NOTES_FILE, "w", encoding="utf-8") as file:
            file.write(notes)


    def remCtrlCB(self, arg):                                   #Remote control callback
        #['', 'slot', '0', 'status']
        reguest = arg.split("/")                        #Split request to array
        print("CB arg-", reguest )
        if reguest[0].startswith("i2c-write"):
            cmdStr = reguest[0].split(";")
            print("cmdStr-", cmdStr)
            if len(cmdStr) < 5:
                return "Error: Invalid command"
            if cmdStr[4] == "":
                return "Error: Empty byte array"
    
            try:
                addr = int(cmdStr[1], 16)  # Адреса пристрою
                reg = int(cmdStr[2], 16)   # Адреса регістра
                value = int(cmdStr[4], 16) # Значення регістра
        
                # Формуємо масив байтів: [адреса регістра, значення]
                byte_array = bytes([reg, value])
                print("Byte array-", byte_array)
            except ValueError as e:
                return "Error converting to byte array"
    
            try:
                write = i2c_msg.write(addr, byte_array)
                self.bus.i2c_rdwr(write)
                return "Write successful"
            except Exception as e:
                print("Error writing to i2c:", e)
                return "Error writing to i2c"

        if reguest[0].startswith("i2c-read"):
            cmdStr = reguest[0].split(";")
            print("cmdStr-", cmdStr)
            
            try:
                addr = int(cmdStr[1], 16)
                reg = int(cmdStr[2], 16)
                #read = i2c_msg.read(addr, int(cmdStr[2]))
                #self.bus.i2c_rdwr(read)
                print("addr-", addr)
                print("reg-" , reg)
                print("len-" , cmdStr[3])    
                read = self.bus.read_i2c_block_data(addr, reg, int(cmdStr[3]))
                print("Read-", read)

                return " ".join(f"{byte:02X}" for byte in list(read))
            except Exception as e:
                return ("Error reading from i2c")

        if reguest[0].startswith("getNotes"):
            self.notes = self.load_notes_from_file()
            return self.notes

        if reguest[0].startswith("saveNotes"):
            notesContent = reguest[0].replace("saveNotes:", "", 1)
            self.save_notes_to_file(notesContent)
            return "OK"

        return "OK"



if __name__ == "__main__":
    Main()