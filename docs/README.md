<div id="title" align="center">
    <h1><a href="https://discord.com/api/oauth2/authorize?client_id=1174796137862021190&permissions=1376604515526&scope=bot">AutoKicker</a></h1>
    <p>a Discord bot that auto kicks new members until a member is whitelisted via <b>/whitelist</b> command. See more with <b>/help</b></p>
    <a href="https://github.com/ibnaleem/AutoKicker/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ibnaleem/AutoKicker?style=for-the-badge"></a>
    <a href="https://discord.gg/Z38zqxHRFQ"><img src="https://img.shields.io/discord/1174803169168085132?style=for-the-badge"></a>
    <a href="https://github.com/ibnaleem/AutoKicker/stargazers"><img src="https://img.shields.io/github/stars/ibnaleem/AutoKicker.svg?style=for-the-badge"></a>
</div>

## Disclaimer
#### This repository has no affiliation with, authorization from, maintenance by, sponsorship from, or endorsement by Discord Inc. (discord.com) or any of its affiliates or subsidiaries.

## Invite
#### [Click here to invite bot](https://discord.com/api/oauth2/authorize?client_id=1174796137862021190&permissions=1376604515526&scope=bot) ([PGP Signature](https://pastebin.com/3VdascnY))

## Purpose
[Ninja](https://www.youtube.com/channel/UCAW-NpUFkMyCNrvRSSGIvDQ) and his friends use a private Discord for party-chats and group-chats. However, [Speed](https://www.youtube.com/@IShowSpeed) accidentally leaked the Discord server link which resulted in nuking the server (too many members to bulk ban + channels were likely not privated). I decided to create this bot so Ninja and other streamers can have good security on their private servers.

Some advice: always permission lock channels in-case of a leak.

## Usage
There are 3 methods to whitelisting a member.

### Default using Member ID
```
/whitelist [member-id]
```

### Mention
If a member has joined the server before AutoKicker (or during the time autokick was disabled), you can mention the member to /whitelist them:
```
/whitelist @member-mention
```

### Risky (Disable AutoKick)
```
/disable
```

Remember that you must run `/enable` to re-enable auto-kicking. You check this using `/status`.

## Errors & Support 
[Join my support server](https://discord.gg/Z38zqxHRFQ) or [open an issue here.](https://github.com/ibnaleem/AutoKicker/issues)

## Authors
- [Ibn Aleem](https:///github.com/ibnaleem)

## Built With
- [Discord.py](https://github.com/Rapptz/discord.py)

## License
This project is licensed under the GPL-3.0 License - see the [LICENSE.md](https://github.com/ibnaleem/AutoKicker/blob/main/docs/LICENSE) file for details

## Contributions 
I welcome contributions from the community and appreciate the time and effort put into making this project better. To contribute, please follow the guidelines and steps outlined below:

### Fork the Repository
Start by [forking this repository](https://github.com/ibnaleem/AutoKicker/fork). You can do this by clicking on the ["Fork"](https://github.com/ibnaleem/AutoKicker/fork) button located at the top right corner of the GitHub page. This will create a personal copy of the repository under your own GitHub account.

### Clone the Repository
Next, clone the forked repository to your local machine using the following command:
```bash
$ git clone https://github.com/yourusername/AutoKicker.git
```
Navigate to the cloned directory:
```bash 
$ cd AutoKicker
```
### Create a New Branch
Before making any changes, it's recommended to create a new branch. This ensures that your changes won't interfere with other contributions and keeps the main branch clean. Use the following command to create and switch to a new branch:
```bash
$ git checkout -b branch-name
```
### Make the Desired Changes
Now, you can proceed to make your desired changes to the project. Whether it's fixing bugs, adding new features, improving documentation, or optimizing code, your efforts will be instrumental in enhancing the project.

### Commit and Push Changes
Once you have made the necessary changes, commit your work using the following commands:
```bash
$ git add .
$ git commit -m "Your commit message"
```
Push the changes to your forked repository:
```bash
$ git push origin branch-name
```
### Submit a Pull Request
Head over to the [original repository](https://github.com/ibnaleem/AutoKicker) on GitHub and go to the ["Pull requests"](https://github.com/ibnaleem/AutoKicker/pulls) tab.
1. Click on the "New pull request" button.
2. Select your forked repository and the branch containing your changes.
3. Provide a clear and informative title for your pull request, and use the description box to explain the modifications you have made.
4. Finally, click on the "Create pull request" button to submit your changes.
