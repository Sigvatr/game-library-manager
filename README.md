# Games Library Manager

The project to creating and updating your pile of shame excel document. The list of all games which are waiting to be played at least once.

It connects with your game accounts (like Steam or Epic) and creates a list games. With additional information like how long games was played or how many achievements are missing.

It's also my pet project to experiment with function programming (in Python).

## Steam API

### Preapring

To use [Steam API](https://steamcommunity.com/dev) you will need **API Key**. You can generate one on the [Register Steam Web API Key](https://steamcommunity.com/dev/apikey) form. The site is asking for domian, but anything seems to work. We will not going to use on page, so enter whaterever you wish.

You alse needs the **Steam User ID**. The easiest way to find it, is look where *View profile* link leads (the number part of the URL). The other way are presented on page [How to Get Your Steam ID](https://www.wikihow.com/Get-Your-Steam-ID).

### Downloading data from Steam

We are going to use API method `GetOwnedGames` with `include_appinfo` paramater. It returns the whole collection of games, the name, time spend on title and achievements if game has them.

## Epic Games

Unfortunietly Epic doesn't have API for its game library. There is [Unoffical Epic Games Client](https://www.npmjs.com/package/epicgames-client), but it's not provide get all games. So, we need to improvise.

### Downloading data from Epic Games

The only way to get all games in Epic Store is on the Account [Transactions](https://www.epicgames.com/account/transactions) page. It is using query: `https://www.epicgames.com/account/v2/payment/ajaxGetOrderHistory?page=`.

The respose is JSON:

```json
{
    "count": 10,
    "orders": [],
    "start": 20,
    "total": 93
}
```

We will recived the collection list, but as JSON object. The page [JSON-CSV](https://json-csv.com/) can be usefull here.

## GOG

There is a [API for GOG](https://gogapidocs.readthedocs.io/en/latest/index.html). But it's required loggin via [GOG page](https://login.gog.com/auth?). So also we need to use browser to run a script.

## Uplay

Unfortunetly there is not API for Uplay, the list of games is not presented in any form on Uplay web page, or support page. The only thing which can be obtain is the number of own games or last played.
