
# Py Multi-Mailer

Send mail to multiple user at once.


## Releases


![PyPi](https://img.shields.io/pypi/v/shahr2.multimailer?color=orange&label=PyPi%20release&logo=PyPi&logoColor=white)
## Requirements

![Python](https://img.shields.io/badge/Python%203.10.2-TESTED-brightgreen)
## Installation

Install shahr2.pymultimailer with pip

```bash
  pip install shahr2.pymultimailer
```
    
## Usage/Examples

```python
from shahr2 import pymultimailer

SENDER = 'sender gmail'
PASSWORD = 'sender app password/gmail password'
SUBJECT = 'subject of mail'
BODY = 'body of mail with {} {} 2 empty braces for first and last name.'
FILE = 'csv file location'
FIRST_NAME = 'first name parameter in csv file'
LAST_NAME = 'last name parameter in csv file'
EMAIL = 'email parameter in csv file'

mail = pymultimailer.input(
    SENDER, PASSWORD, SUBJECT, BODY
    )

mail.csvData(
    FILE, FIRST_NAME, LAST_NAME, EMAIL
    )

mail.send()
```


## Authors

- [@shahadathshahriarakash](https://github.com/shahadathshahriarakash)

