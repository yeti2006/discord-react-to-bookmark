# discord-react-to-bookmark
A simple script that lets you bookmark messages in Discord with reactions to channel(s) of your choosing!

:warning: This script is supposed to be use as a self bot, and self-botting is against the Discord ToS. There is a chance for you to get banned. Proceed to use at your own risk!

## Why and what for?
In case you want to bookmark messages, specially attachments and stuff(memes) in Discord itself for retreiving them later all in one place. 

This script works by downloading attachments if any, and then uploading them to the channel you specify. I made it download them without sending the attachment URLs because if the original author deletes the message, they are no longer accessible.

I recommend having a private server for having all of your bookmark channels. I might consider adding some self-commands for sending bookmarks by filtering through indexes and such and sending them.

This might seem useless, but some might find it useful idk. If you do, leave a star <3

## Demo
![demo](./readme/discord-react-to-bookmark-demo.mp4)

Context: Setting up 2 bookmark channels for the emojis :star: and :bookmark: for #memes and #important respectively

## Requirements
* [discord-py-self](https://github.com/dolfies/discord.py-self@renamed#egg=selfcord.py[voice]) - renamed branch(`selfcord`)
* loguru - for logging

# Usage

> Clone the repo
```sh
git clone https://github.com/yeti2006/discord-react-to-bookmark && cd discord-react-to-bookmark
```
> Install requirements via pip
```sh
pip install -r requirements.txt
```
> Configure `config.ini` ([see below](#Configuration))

```ini
# Welcome to the Configuration!

[info]
discord_account_token = your_account_token
logs_channel_id = 0
message_format = **(_{server}_)** | {author} | {time}{newline}`{message.content}`
```
> Run the script
```sh
python -m bm
```

ℹ️ To exit the script press ctrl + c
## Configuration

The `config.ini` file exists for you to add as many reaction emojis as you want and send the messages you react messages with to channels you specify.

...To add an emoji, you need to create a block with brackets `[]` and type in an emoji unicode inside them. After that, it requires to values inside that block:

- [x] `channel_id` - The ID of the text channel you want the bookmarked message sent to
- [x] `message_format` - The format of the message. Use variables with `{}`. You can leave this empty to use the default value:

    - ```fix
      **{author}**(_{server}_) - {time}{newline}{message.content}
      ```

### Formatting values


| Tag | Value | Attributes |
|--|--|--|
| `author` | The author of the message | [`Member`](https://discordpy-self.readthedocs.io/en/latest/api.html?highlight=member#discord.Member)
| `time` | The time the message was created | None
| `server` | The guild of the message | [`Guild`](https://discordpy-self.readthedocs.io/en/latest/api.html?highlight=member#discord.Guild)
| `message` | The message | [`Message`](https://discordpy-self.readthedocs.io/en/latest/api.html?highlight=member#discord.Message)|
| `emoji` | The emoji you reacted with | None
| `newline` | Appends a new line to the string | None
