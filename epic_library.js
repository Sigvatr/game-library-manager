const compose = (...funcs) => initialArg => funcs.reduceRight((acc, func) => func(acc), initialArg);
const range = end => [...Array(end).keys()];
const getPage = pageNumber => fetch(`https://www.epicgames.com/account/v2/payment/ajaxGetOrderHistory?page=${pageNumber}`);
const getData = pagePromise => pagePromise.then(response => response.json());
const getReqestForData = compose(getData, getPage);
const getCount = data => data.count;
const getTotal = data => data.total;
const getOrders = data => data.orders;
const getNumberOfPages = data => Math.ceil(getTotal(data) / getCount(data));
const getOrderItem = orders => orders.items[0];
const getGameName = orderItem => orderItem.description;

getData(getPage(0))
    .then(data =>
        Promise.all(
            range(getNumberOfPages(data)).map(getReqestForData)
        )
            .then(allResponse => allResponse
                .map(getOrders)
                .reduce((previous, current) => [...previous, ...current], [])
            )
    )
    .then(allOrders => allOrders
        .map(getOrderItem)
        .map(getGameName)
    )
    .then(gamesList => console.log(gamesList))
