from urllib.request import urlopen
from urllib.parse import quote
import ssl

sounds = ["alarm", "anticipate", "bell", "birdsong", "bloom", "calypso", "chime", "choo", "descent", "electronic", "fanfare", "glass", "gotosleep", "healthnotification", "horn", "ladder", "mailsent", "minuet", "multiwayinvitation", " newmail", "newsflash", "noir", "paymentsuccess", "shake", "sherwoodforest", "silence", "spell", "suspense", "telegraph", "tiptoes", "typewriters", "update"]

class Bark:
    def __init__(self, token, server=None):
        self.token = token
        if server:
            self.server = server
        else:
            self.server = "https://api.day.app/"

    def send(content, title=None, sound=None, isArchive=None, icon=None, group=None, url=None):
        final_url = self.server + self.token + "/"
        if title:
            final_url += quote(title, safe="") + "/"
        final_url += quote(content, safe="")
        param_mark = False
        if sound is not None:
            if sound in sounds:
                if not param_mark:
                    final_url += "?"
                else:
                    final_url += "&"
                final_url += "sound={}".format(sound)
        if isArchive is not None:
            if isArchive == 1 or isArchive == 0:
                if not param_mark:
                    final_url += "?"
                else:
                    final_url += "&"
                final_url += "isArchive={}".format(isArchive)
        if icon is not None:
            if not param_mark:
                final_url += "?"
            else:
                final_url += "&"
            final_url += "icon={}".format(quote(icon, safe=""))
        if group is not None:
            if not param_mark:
                final_url += "?"
            else:
                final_url += "&"
            final_url += "group={}".format(quote(group, safe=""))
        if url is not None:
            if not param_mark:
                final_url += "?"
            else:
                final_url += "&"
            final_url += "url={}".format(quote(url, safe=""))

        urlopen(final_url, context=ssl._create_unverified_context()).read()
