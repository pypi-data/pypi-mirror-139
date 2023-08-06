# PyBark

A simple application to send a message push via Bark

## 1. Installation
``` Bash
# Install via pip
pip install PyBark
```

## 2. Usage
``` Bash
from PyBark import Bark

bark = Bark("XXXXXXXXXXXXXXXXXXXXXX") # Replace with your Key Token

# bark = Bark("XXXXXXXXXXXXXXXXXXXXXX", server="https://api.day.app") 
# You can use your own server like this.

bark.send("Test Message") # Simple message push
bark.send("Test Message", title="Message Title") # Push message with title
bark.send("Test Message", title="Message Title", icon="https://day.app/assets/images/avatar.jpg") # Push message with multiple params

# Full params guide can be found in function description
```

## Great Thanks to [Bark](https://github.com/Finb/Bark)