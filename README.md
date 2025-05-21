# AM2Slack
A mini script to update your Slack status with the song currently playing on Apple Music on macOS.

## Features:
- Shell script to run on your Mac Terminal.
- Constantly running with custom execution frequency.
- Custom status expiration time.
- Does not update if current Slack status is in custom whitelist.
- If no music is playing, status is cleared.
- Editable random emojis that are selected each time your status changes.

## Usage
1. Clone the repository
2. Go to api.slack.com/apps and press "Create New App". Select the workspace and give it a name.
3. With the app created, go to "OAuth & Permissions". Now under "Scopes" add these User Token Scopes: `users.profile:write`, `users.profile:read`.
4. Scroll to the top and click "Install/Reinstall to Workspace".
5. Copy the User OAuth Token and paste it next to `API_KEY` in the `.env.example` file.
6. Go to your `AM2Slack.py` file then copy its path and paste it next to `PROGRAM_DIR`.
7. Tweak the `.env.example` file as desired and rename it to `.env` when done.
8. Make the script executable by running the following command in your terminal `chmod +x AM2Slack.sh`.
9. (Optional but recommended) Create a virtual environment.
10. Install project dependencies `pip install -r requirements.txt`
11. Make sure `watch` command is installed. If it's not, install it with `brew install watch`
12. Run the program with `./AM2Slack.sh`