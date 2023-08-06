
# Py Mail-Sender

A small Email sending package. You can use this package on your project.


## Releases


![PyPi](https://img.shields.io/pypi/v/shahr2.pymailsender?logo=PyPi&logoColor=orange)
## Requirements

![Python](https://img.shields.io/badge/Python%203.10.2-TESTED-brightgreen)
## Installation

Install shahr2.pymailsender with pip

```bash
  pip install shahr2.pymailsender
```
    
## Usage/Examples

```python
from shahr2 import pymailsender

SENDER = 'sender gmail'
PASSWORD = 'sender app password/gmail password'
RECEIVER = 'receiver email'
SUBJECT = 'subject of mail'
BODY = 'body of mail'

mail = pymailsender.input(
    SENDER, PASSWORD, RECEIVER, SUBJECT, BODY
    )
mail.send()
```


## Authors

- [@shahadathshahriarakash](https://github.com/shahadathshahriarakash)

