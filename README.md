# EnglishBot
this bot allows you to efficiently prepare for the exam on the go, in the telegram

## Configuration and starting

### config.json structure:
```json
"DB" : {
    "host" : "",
    "username" : "",
    "password" : "",
    "db" : "",
    "charset" : ""
},
"BOT" : {
    "TOKEN" : "",
    "WEBHOOK_URL" : ""
}
```

### How to run this bot:

#### WebHooks
```shell
$ python FlaskStarter.py
```
#### Polling
```shell
$ python main.py
```
