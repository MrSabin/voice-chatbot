# Bots for VK and Telegram with DialogFlow

You can see how the bots is working by visiting [@dvmn-test](http://t.me/dvmn_misc_bot) for telegram and [DVMN-bot](https://vk.com/club219791098) for VK.

## How to install:
1. Python 3 should be already installed
2. Download repository 
3. Install dependencies by running
```bash
python3 -m pip install -r requirements.txt
```

## Setting up:

For use this scripts, you will need:
- Telegram bot token (use existing one or create new on [@BotFather](http://t.me/BotFather))
- Your Telegram chat ID (use [@userinfobot](tg://resolve?domain=userinfobot) if you don't know where to look for ID)
- Your DialogFlow project ID. To obtain it, login to [DialogFlow](https://dialogflow.cloud.google.com/#/login), create new agent on [this](https://dialogflow.cloud.google.com/#/newAgent) page, then go to agent settings - your project ID will be there.
- Your VK group token (for using VK bot). Create group [here](https://vk.com/groups_create), in group `Settings - Messages - Bot settings` enable `Bot abilities`, then in `Settings - API usage` create token.

Create .env file and fill it with variables as in env_example file.

Now you need to install Google Cloud CLI as described in [this source](https://cloud.google.com/sdk/docs/install). Initialize `gcloud` using command

```bash
gcloud init
```

then log in and save your auth credentials using command

```bash
gcloud auth application-default login
``` 

## Batch create DialogFlow intents (teach the bot):

To create multiple bot intents at once, create JSON file with questions and answers needed by you using `questions.json` as example, and run the script by command

```bash
python3 training.py --json_path "path_to_json_file"
```

New intents will be added in your DialogFlow project. If no JSON file is specified, script will use included `questions.json`.

## Running scripts:

To use telegram bot, type

```bash
python3 tg_bot.py
```

To use VK bot, type

```bash
python3 vk_bot.py
```

## Project goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/)