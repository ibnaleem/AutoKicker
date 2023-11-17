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
[Ninja](https://www.youtube.com/channel/UCAW-NpUFkMyCNrvRSSGIvDQ) and his friends use a private Discord for party-chats and group-chats. However, [Speed](https://www.youtube.com/@IShowSpeed) accidentally leaked the Discord server link which resulted in the server being nuked (too many members to bulk ban + channels are likely not privated). I decided to create this bot so Ninja and other streamers can have good security on their private servers.

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
