![FA Github Header](https://user-images.githubusercontent.com/2868/98735818-fabe8a80-2371-11eb-884a-e555e31aa348.png)

# Sales Navigator Bot

A robot that extracts contacts from saved lists.  It can also run those contacts against hunter.io and add an email.  
This bot allows humans to focus on crafting lists and not spend time list-building in LinkedIn.

# Local Installation

1.  Clone the repo
2.  Install the dependencies using `rcc`
3.  Create a `.env` with the following variables:

```
RC_API_SECRET_HOST=''
RPA_SECRET_MANAGER='RPA.Robocloud.Secrets.FileSecrets'
RPA_SECRET_FILE='/path/to/vault.json'
```

# Running

The bot runs as an Assistant Bot on Robocorp or you can just run it with pure python as `python task.py`

# Questions

Reach out to us at hello@formulatedautomation.com