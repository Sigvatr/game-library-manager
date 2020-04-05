# Games Library Manager

The project to creating and updating your pile of shame excel document. The list of all games which are waiting to be played at least once.

It connects with your game accounts (like Steam or Epic) and creates a list games. With additional information like how long games was played or how many achievements are missing.

It's also my pet project to experiment with function programming (in Python).

## Steam API

### Preapring

To use [Steam API](https://steamcommunity.com/dev) you will need **API Key**. You can generate one on the [Register Steam Web API Key](https://steamcommunity.com/dev/apikey) form. The site is asking for domian, but anything seems to work. We will not going to use on page, so enter whaterever you wish.

You alse needs the **Steam User ID**. The easiest way to find it, is look where *View profile* link leads (the number part of the URL). The other way are presented on page [How to Get Your Steam ID](https://www.wikihow.com/Get-Your-Steam-ID).

### Downloading data

We are going to use API method `GetOwnedGames` with `include_appinfo` paramater. It returns the whole collection of games, the name, time spend on title and achievements if game has them.
