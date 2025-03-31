# BoringUtil
A bot which is just "boring".

# Features
The following bot features are:
- Music
- Air fryer (not literally)
- AI powered by Gemini

# Installation
1. Install Python (if you haven't already)
2. Install ffmpeg (needed for the music bot function)
3. Copy the .env.example file to .env

## Part 1. Discord
4. Run `pip install -r requirements.txt` in the project directory.
5. Get the Discord token from https://discord.dev in the applications tab and create a app.
6. Then once you are in the application click "Bot" and then click the "Reset Token" button.
7. Scroll down to "Privileged Gateway Intents" and enable all of them and click "Save Changes" after.
8. Open the .env file and replace `TOKEN=discord_token` with `TOKEN=` (inside it being the token you got).
9. Go to OAuth2 and scroll down to the URL generator and in the scopes click "bot".
10. Permissions set as "Send Messages", "Send Messages in Threads", "Use Slash Commands", "Connect", "Speak" or just pick "Administrator"

## Part 2: Gemini
**WIP cuz I am lazy**