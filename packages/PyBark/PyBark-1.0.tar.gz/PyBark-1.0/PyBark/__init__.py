from urllib.request import urlopen
from urllib.parse import quote
import ssl

sounds = ["alarm", "anticipate", "bell", "birdsong", "bloom", "calypso", "chime", "choo", "descent", "electronic", "fanfare", "glass", "gotosleep", "healthnotification", "horn", "ladder", "mailsent", "minuet", "multiwayinvitation", " newmail", "newsflash", "noir", "paymentsuccess", "shake", "sherwoodforest", "silence", "spell", "suspense", "telegraph", "tiptoes", "typewriters", "update"]
levels = ["active", "timeSensitive", "passive"]

class Bark:
    def __init__(self, token, server="https://api.day.app"):
        """
        Setting Bark Params.
        Args:
            token: Personal Key Token provided by Bark (Required)
            server: Bark Server (Optional, default value is https://api.day.app)
        """
        self.token = token
        self.server = server

    def send(self, content, title=None, sound=None, isArchive=None, icon=None, group=None, url=None, level=None):
        """
        Send Messages.
        Args:
            content: Message content (Required)
            title: Message title (Optional, Bolder font in message)
            sound: Message will come with a sound notification (Optional, only sounds in list are supported)
            isArchive: Set to 1 if you want message will be archived, otherwise set to 0, if not provided, it will depends on the receiver's setting (Optional)
            icon: Message will come with a provided icon, Bark icon if not provided (Optional, URL, svg is not supported)
            group: Message will be grouped in Notification Center (Optional)
            url: Message will come with a redirectable link (Optional)
            level: 
                - active: Default
                - timeSensitive: Notification will be poped even in Focus Mode
            - passive: Only add a notification in notification list
        """
        final_url = self.server + "/" + self.token + "/"
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
        if level is not None:
            if level in levels:
                if not param_mark:
                    final_url += "?"
                else:
                    final_url += "&"
                final_url += "level={}".format(level)

        urlopen(final_url, context=ssl._create_unverified_context()).read()
