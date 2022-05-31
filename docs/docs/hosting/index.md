# Prerequisites

## Creating a discord bot account
1. Create a [new application](https://discord.com/developers/applications).
![create a new application](/img/prerequisites/new_application.png)
1. Give it a nice name and create.
![give it a name](/img/prerequisites/name.png)
1. Click on the bot section.
![click on the bot section](/img/prerequisites/bot_section.png)
1. Add a bot to your application.
![add a bot](/img/prerequisites/add_bot.png)
1. Confirm.
![confirm](/img/prerequisites/confirm.png)
1. Get the bot token.
![reset token](/img/prerequisites/reset_token.png)
1. Confirm.
![confirm reset token](/img/prerequisites/confirm_token.png)
1. Copy the token (The token shown in the image is not valid anymore).
![copy token](/img/prerequisites/copy_token.png)
1. Scroll down and enable Server Members Intent and save changes.
![enable server members intent](/img/prerequisites/enable_intent.png)
1. Click on the OAuth2 tab.
![click on oauth2 tab](/img/prerequisites/oauth2_tab.png)
1. Click on Url Generator tab inside the OAuth2 tab.
![click on url generator tab](/img/prerequisites/url_generator.png)
1. Select "bot" and "application.commands" scopes and "Administrator" permission (for the sake of getting started).
![select "bot" and "application.commands" scopes and "Administrator" permission](/img/prerequisites/scopes_permissions.png)  
1. Scroll down and copy your generated URL.
![scroll down and copy generated url](/img/prerequisites/copy_url.png)
1. Visit that URL and add the bot to your guild like shown [here](/#adding-our-public-bot).
1. Add the bot token as a Environment Variable.

## Environment Variables
- `TOKEN`: Discord Bot Token
- `RANDOMMER_API`: The API key for [randommer](https://randommer.io)
- `POSTGRESQL_HOST`: The hostname for your [PostgreSQL][1] database
- `POSTGRESQL_DATABASE`: The name of your [PostgreSQL][1] database
- `POSTGRESQl_USER`: The username for your [PostgreSQL][1] database
- `POSTGRESQL_PASSWORD`: The password for your [PostgreSQL][1] database user

[1]: https://www.postgresql.org/

# Guides
- [Locally](/hosting/local)
- [Railway](/hosting/railway) (Recommended)
- [Heroku](/hosting/heroku)
- [Replit](/hosting/replit) (Discouraged)