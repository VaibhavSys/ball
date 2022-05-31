# Welcome to Ball Discord Bot's documentation

## Adding our Public Bot
Don't want to host it yourself? We got you covered!
You can add our [public bot][1] and relax.

### Step-by-step instruction
1. Click [here][1].
![select guild screen](/img/getting-started/default.png)
1. Select the guild you want to add the bot to and click "Continute" on the bottom right of the panel.
![select guild](/img/getting-started/select-guild.png)
1. Go to the bottom right of the panel and click "Authorize".
1. You may need to do a captcha, then the bot should be added to your guild.

[1]: https://discord.com/api/oauth2/authorize?client_id=923535197260087296&permissions=1644971949559&scope=bot%20applications.commands

## Self-Hosting

### Environment Variables
- `TOKEN`: Discord Bot Token.
- `RANDOMMER_API`: The API key for [randommer](https://randommer.io).
- `POSTGRESQL_HOST`: The hostname for your [PostgreSQL][2] database.
- `POSTGRESQL_DATABASE`: The name of your [PostgreSQL][2] database.
- `POSTGRESQl_USER`: The username for your [PostgreSQL][2] database.
- `POSTGRESQL_PASSWORD`: The password for your [PostgreSQL][2] database user.

[2]: https://www.postgresql.org/

### Hosting locally
1. Clone the [repository](https://github.com/MouseMoosz/ball).
1. Install any missing dependencies.
1. Get into the poetry virtual environment. 
1. Start the bot.

```console
$ git clone https://github.com/MouseMoosz/ball.git
$ poetry install
$ poetry shell
$ python3 src/bot.py
```

### Hosting in cloud
- Hosting on [Railway](/hosting/railway) (Recommended)
- Hosting on [Heroku](/hosting/heroku)
- Hosting on [Replit](/hosting/replit) (Discouraged)
