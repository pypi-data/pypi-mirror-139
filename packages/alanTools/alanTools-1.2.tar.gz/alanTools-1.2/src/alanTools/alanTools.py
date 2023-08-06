class rand:
    def num(min_int, max_int):
        import random
        return random.randint(min_int, max_int)
    
    def choice(sequence):
        import random
        return random.choice(sequence)

    def shuffle(sequence):
        import random
        return random.shuffle(sequence)

class os:
    def clear():
        import os
        import platform

        if platform.system() == "windows":
            os.system("cls")
        else:
            os.system("clear")

    def command(command):
        import os
        os.system(command)

class request:
    def get(url):
        import requests
        sent = requests.get(url)
        return sent

class qr:
    def make(text):
        import qrcode
        pic = qrcode.make(text)
        pic.save("qrcode.png")
