const req = require("superagent");

const currentDate = new Date();
const interval = "1d";
const timespan = 7;
const periods = getPeriods();
const exchangePostfix = "AX";
const defaultParams = {
    formatted: false,
    crumb: ".x9Fjg.rAfj",
    lang: "en-AU",
    region: "AU"
}
const api = {
    list: {
        url: "https://asx.api.markitdigital.com/asx-research/1.0/companies/directory",
        params: {
            page: 0,
            itemsPerPage: 3000,
            order: "ascending",
            orderBy: "companyName",
            includeFilterOptions: false,
            recentListingsOnly: false
        }
    },
    bulk: {
        url: "https://query1.finance.yahoo.com/v7/finance/quote",
        params: {
            formatted: defaultParams.formatted,
            crumb: defaultParams.crumb,
            lang: defaultParams.lang,
            region: defaultParams.region,
            fields: [
                "regularMarketPrice",
                "regularMarketChange",
                "regularMarketChangePercent",
                "regularMarketVolume",
                "marketCap",
                "regularMarketOpen",
                "fiftyTwoWeekLow",
                "fiftyTwoWeekHigh",
                "toCurrency",
                "fromCurrency"
            ]
        }
    },
    historical: {
        url: "https://query2.finance.yahoo.com/v8/finance/chart/",
        params: {
            formatted: defaultParams.formatted,
            crumb: defaultParams.crumb,
            lang: defaultParams.lang,
            region: defaultParams.region,
            includeAdjustedClose: false,
            //useYfid: true,
            interval: interval,
            period1: periods.period1,
            period2: periods.period2
        }
    }
}
const stocks = getDetails();

function getTickers() {
    return req
        .get(api.list.url)
        .query(api.list.params)
        .set('Accept', 'application/json')
    ;
    return ['ABB', 'WOW']
}

function getAggregateDetails(tickers){
    let params = api.bulk.params;
    params.fields = params.fields.join();
    params.symbols = tickers.map(t => addPostfix(t)).join();
    JSON.stringify(params);
    console.log(JSON.stringify(params).length);

    return req
        .get(api.bulk.url)
        .query(params)
        .set('Accept', 'application/json')
    ;
}

function getStockDetail(ticker){
    return req
        .get(api.historical.url + addPostfix(ticker))
        .query(api.historical.params)
        .set('Accept', 'application/json')
        .catch(err => console.log("Request failed for " + ticker + " : " + err))
    ;
}

function processData (tickers, historicalDataResponses){
    let data = {};
    historicalDataResponses
        .map(res => res.body.chart.result[0])
        .filter(stock => Object.keys(stock.indicators.quote[0]).length > 0)
        .forEach(stock => {
            data[removePostfix(stock.meta.symbol)] = {
                meta: stock.meta,
                historical: stock.indicators.quote[0]
            };
        });
    for(const [key, stock] of Object.entries(data)){
        data[key].analysis = analyseStock(stock);
    }
    return data;
}

function getDetails(){
    let stockData = {};
    let promises = {};

    promises.tickers = getTickers();
    
    promises.tickers.then(tickersResponse => {
        let tickers = tickersResponse.body.data.items.map(ticker => ticker.symbol)//.slice(0, 800);//.filter(tick => tick == "EME");

        promises.historical = [];
        tickers.forEach(
            (ticker) => promises.historical.push(
                getStockDetail(ticker)
            )
        );
        Promise
            .allSettled(promises.historical)
            .then(settledValues => {
                let values = settledValues.filter(sv => !!sv.value).map(sv => sv.value);
                console.log("All calls complete");
                stockData = processData(tickers, values);
                console.log(
                    Object.values(stockData)
                    .map(stock => {
                        return {
                            symbol: removePostfix(stock.meta.symbol),
                            buy: stock.analysis.buy
                            ,rating: stock.analysis.rating
                            //,analysis: stock.analysis
                        };
                    })
                    .filter(stock => stock.buy)
                    .sort((a, b) => b.rating - a.rating)
                );
            })
            .catch(err => {
                console.log("One or more historical calls failed with error: " + err);
            })
        ;
    });
}

function addPostfix (ticker) {
    return ticker + '.' + exchangePostfix;
}

function removePostfix(ticker) {
    return ticker.substr(0,3);
}

function getPeriods(){
    let periods = {
        period2: Date.UTC(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate()) / 1000,
        period1: Date.UTC(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() - (timespan + 5)) / 1000
    };

    return periods;
}

function analyseStock(stockDetails){

    //Volume
    let allVolumes = stockDetails.historical.volume;
    let volumes = allVolumes.slice(allVolumes-timespan);
    //console.log(volumes)
    let totalVolumeExcludingToday = volumes.slice(0, volumes.length-2).reduce(function(acc, curr){return acc + curr}, 0);
    //console.log(volumes.slice(0, volumes.length-2))
    let averageVolume = totalVolumeExcludingToday/(timespan-1)
    let todaysVolume = volumes[volumes.length-1];
    let volumeChangePercentageOverAverage = ((todaysVolume/averageVolume)*100);

    
    let marketState = stockDetails.marketState;
    //Set price assuming market is open
    let price = stockDetails.historical.open[stockDetails.historical.open.length-1]
    let previousPrice = stockDetails.historical.open[stockDetails.historical.open.length-2]
    if(marketState == "PREPRE"){
        //If market is not yet open, set price to most recent close
        price = stockDetails.historical.close[stockDetails.historical.close.length-1]
    }
    let priceChangePercentage = ((price / previousPrice) * 100);


    return {
        stats: {
            totalVolumeExcludingToday: totalVolumeExcludingToday,
            averageVolume: averageVolume,
            todaysVolume: todaysVolume,
            volumeChangePercentageOverAverage: volumeChangePercentageOverAverage,
            marketState: marketState,
            price: price,
            previousPrice: previousPrice,
            priceChangePercentage: priceChangePercentage
        },
        rating: volumeChangePercentageOverAverage/4 + priceChangePercentage,
        buy : (
            volumeChangePercentageOverAverage >= 400
            && priceChangePercentage >= 105
        )
    };
}

module.exports = {stocks};