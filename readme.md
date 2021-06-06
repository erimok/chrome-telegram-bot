# File receiver bot

## Bot configuration

Configuration of the bot setting up via `config.ini`. 
Example of config file is placed in root folder of the project (`config.ini.example`).

## Bot initialization

Entry point of the bot is `init.py`
You have to use ssh and following command to run the bot for an unlimited time:
> nohup python init.py &

### How to restart bot
You have to use ssh and following command:
> ps aux 

You can find `process ID`. After that use this one command `kill <process ID>`. Example:
> kill 219394

After that run bot init command again.

## Venv

Installation
> python3 -m venv venv

Use virtual env
> source venv/bin/activate

Install required libraries
> pip install -Ur requirements.txt

Deactivate venv
> deactivate

## Git repository

https://github.com/erimok/chrome-telegram-bot/

