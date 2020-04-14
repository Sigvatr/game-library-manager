const compose = (...funcs) => initialArg => funcs.reduceRight((acc, func) => func(acc), initialArg);
const get = url => fetch(url);
const getAllGames = _ => get('/user/data/games');
const asJSON = promise => promise.then(s => s.json());
const getOwned = promise => promise.then(s => s.owned);
const getAllUserGames = compose(getOwned, asJSON, getAllGames);
const getTitle = promise => promise.then(gameDetial => gameDetial.title);
const getGameDetailUrl = id => `/account/gameDetails/${id}.json`;
const getGameTitle = compose(getTitle, asJSON, get, getGameDetailUrl);
const getGameDetails = async gameId => ({
    id: gameId,
    name: await getGameTitle(gameId)
});

await getAllUserGames()
    .then(gamesIds => Promise.all(gamesIds.map(getGameDetails)))
    .then(gameDetials => gameDetials.filter(gameDetial => gameDetial.name))
