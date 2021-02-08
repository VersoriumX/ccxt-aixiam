# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxtpro.base.exchange import Exchange
import ccxt.async_support as ccxt
from ccxtpro.base.cache import ArrayCache, ArrayCacheById
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import NotSupported


class kraken(Exchange, ccxt.kraken):

    def describe(self):
        return self.deep_extend(super(kraken, self).describe(), {
            'has': {
                'ws': True,
                'watchBalance': False,  # no such type of subscription as of 2021-01-05
                'watchMyTrades': True,
                'watchOHLCV': True,
                'watchOrderBook': True,
                'watchOrders': True,
                'watchTicker': True,
                'watchTickers': False,  # for now
                'watchTrades': True,
                # 'watchHeartbeat': True,
                # 'watchStatus': True,
            },
            'urls': {
                'api': {
                    'ws': {
                        'public': 'wss://ws.kraken.com',
                        'private': 'wss://ws-auth.kraken.com',
                        'beta': 'wss://beta-ws.kraken.com',
                    },
                },
            },
            'versions': {
                'ws': '0.2.0',
            },
            'options': {
                'tradesLimit': 1000,
                'OHLCVLimit': 1000,
            },
            'exceptions': {
                'ws': {
                    'exact': {
                        'Event(s) not found': BadRequest,
                    },
                    'broad': {
                        'Currency pair not in ISO 4217-A3 format': BadSymbol,
                    },
                },
            },
        })

    def handle_ticker(self, client, message, subscription):
        #
        #     [
        #         0,  # channelID
        #         {
        #             "a": ["5525.40000", 1, "1.000"],  # ask, wholeAskVolume, askVolume
        #             "b": ["5525.10000", 1, "1.000"],  # bid, wholeBidVolume, bidVolume
        #             "c": ["5525.10000", "0.00398963"],  # closing price, volume
        #             "h": ["5783.00000", "5783.00000"],  # high price today, high price 24h ago
        #             "l": ["5505.00000", "5505.00000"],  # low price today, low price 24h ago
        #             "o": ["5760.70000", "5763.40000"],  # open price today, open price 24h ago
        #             "p": ["5631.44067", "5653.78939"],  # vwap today, vwap 24h ago
        #             "t": [11493, 16267],  # number of trades today, 24 hours ago
        #             "v": ["2634.11501494", "3591.17907851"],  # volume today, volume 24 hours ago
        #         },
        #         "ticker",
        #         "XBT/USD"
        #     ]
        #
        wsName = message[3]
        name = 'ticker'
        messageHash = name + ':' + wsName
        market = self.safe_value(self.options['marketsByWsName'], wsName)
        symbol = market['symbol']
        ticker = message[1]
        vwap = self.safe_float(ticker['p'], 0)
        quoteVolume = None
        baseVolume = self.safe_float(ticker['v'], 0)
        if baseVolume is not None and vwap is not None:
            quoteVolume = baseVolume * vwap
        last = self.safe_float(ticker['c'], 0)
        timestamp = self.milliseconds()
        result = {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker['h'], 0),
            'low': self.safe_float(ticker['l'], 0),
            'bid': self.safe_float(ticker['b'], 0),
            'bidVolume': self.safe_float(ticker['b'], 2),
            'ask': self.safe_float(ticker['a'], 0),
            'askVolume': self.safe_float(ticker['a'], 2),
            'vwap': vwap,
            'open': self.safe_float(ticker['o'], 0),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }
        # todo add support for multiple tickers(may be tricky)
        # kraken confirms multi-pair subscriptions separately one by one
        # trigger correct watchTickers calls upon receiving any of symbols
        self.tickers[symbol] = result
        client.resolve(result, messageHash)

    def handle_trades(self, client, message, subscription):
        #
        #     [
        #         0,  # channelID
        #         [ #     price        volume         time             side type misc
        #             ["5541.20000", "0.15850568", "1534614057.321597", "s", "l", ""],
        #             ["6060.00000", "0.02455000", "1534614057.324998", "b", "l", ""],
        #         ],
        #         "trade",
        #         "XBT/USD"
        #     ]
        #
        wsName = self.safe_string(message, 3)
        name = self.safe_string(message, 2)
        messageHash = name + ':' + wsName
        market = self.safe_value(self.options['marketsByWsName'], wsName)
        symbol = market['symbol']
        stored = self.safe_value(self.trades, symbol)
        if stored is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            stored = ArrayCache(limit)
            self.trades[symbol] = stored
        trades = self.safe_value(message, 1, [])
        parsed = self.parse_trades(trades, market)
        for i in range(0, len(parsed)):
            stored.append(parsed[i])
        client.resolve(stored, messageHash)

    def handle_ohlcv(self, client, message, subscription):
        #
        #     [
        #         216,  # channelID
        #         [
        #             '1574454214.962096',  # Time, seconds since epoch
        #             '1574454240.000000',  # End timestamp of the interval
        #             '0.020970',  # Open price at midnight UTC
        #             '0.020970',  # Intraday high price
        #             '0.020970',  # Intraday low price
        #             '0.020970',  # Closing price at midnight UTC
        #             '0.020970',  # Volume weighted average price
        #             '0.08636138',  # Accumulated volume today
        #             1,  # Number of trades today
        #         ],
        #         'ohlc-1',  # Channel Name of subscription
        #         'ETH/XBT',  # Asset pair
        #     ]
        #
        info = self.safe_value(subscription, 'subscription', {})
        interval = self.safe_integer(info, 'interval')
        name = self.safe_string(info, 'name')
        wsName = self.safe_string(message, 3)
        market = self.safe_value(self.options['marketsByWsName'], wsName)
        symbol = market['symbol']
        timeframe = self.find_timeframe(interval)
        duration = self.parse_timeframe(timeframe)
        if timeframe is not None:
            candle = self.safe_value(message, 1)
            messageHash = name + ':' + timeframe + ':' + wsName
            timestamp = self.safe_float(candle, 1)
            timestamp -= duration
            result = [
                int(timestamp * 1000),
                self.safe_float(candle, 2),
                self.safe_float(candle, 3),
                self.safe_float(candle, 4),
                self.safe_float(candle, 5),
                self.safe_float(candle, 7),
            ]
            self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
            stored = self.safe_value(self.ohlcvs[symbol], timeframe)
            if stored is None:
                limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
                stored = ArrayCache(limit)
                self.ohlcvs[symbol][timeframe] = stored
            length = len(stored)
            if length and result[0] == stored[length - 1][0]:
                stored[length - 1] = result
            else:
                stored.append(result)
            client.resolve(stored, messageHash)

    def request_id(self):
        # their support said that reqid must be an int32, not documented
        reqid = self.sum(self.safe_integer(self.options, 'reqid', 0), 1)
        self.options['reqid'] = reqid
        return reqid

    async def watch_public(self, name, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        wsName = self.safe_value(market['info'], 'wsname')
        messageHash = name + ':' + wsName
        url = self.urls['api']['ws']['public']
        requestId = self.request_id()
        subscribe = {
            'event': 'subscribe',
            'reqid': requestId,
            'pair': [
                wsName,
            ],
            'subscription': {
                'name': name,
            },
        }
        request = self.deep_extend(subscribe, params)
        return await self.watch(url, messageHash, request, messageHash)

    async def watch_ticker(self, symbol, params={}):
        return await self.watch_public('ticker', symbol, params)

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        name = 'trade'
        trades = await self.watch_public(name, symbol, params)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    async def watch_order_book(self, symbol, limit=None, params={}):
        name = 'book'
        request = {}
        if limit is not None:
            if (limit == 10) or (limit == 25) or (limit == 100) or (limit == 500) or (limit == 1000):
                request['subscription'] = {
                    'depth': limit,  # default 10, valid options 10, 25, 100, 500, 1000
                }
            else:
                raise NotSupported(self.id + ' watchOrderBook accepts limit values of 10, 25, 100, 500 and 1000 only')
        orderbook = await self.watch_public(name, symbol, self.extend(request, params))
        return self.limit_order_book(orderbook, symbol, limit, params)

    async def watch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        name = 'ohlc'
        market = self.market(symbol)
        wsName = self.safe_value(market['info'], 'wsname')
        messageHash = name + ':' + timeframe + ':' + wsName
        url = self.urls['api']['ws']['public']
        requestId = self.request_id()
        subscribe = {
            'event': 'subscribe',
            'reqid': requestId,
            'pair': [
                wsName,
            ],
            'subscription': {
                'name': name,
                'interval': self.timeframes[timeframe],
            },
        }
        request = self.deep_extend(subscribe, params)
        ohlcv = await self.watch(url, messageHash, request, messageHash)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    async def load_markets(self, reload=False, params={}):
        markets = await super(kraken, self).load_markets(reload, params)
        marketsByWsName = self.safe_value(self.options, 'marketsByWsName')
        if (marketsByWsName is None) or reload:
            marketsByWsName = {}
            for i in range(0, len(self.symbols)):
                symbol = self.symbols[i]
                market = self.markets[symbol]
                if not market['darkpool']:
                    info = self.safe_value(market, 'info', {})
                    wsName = self.safe_string(info, 'wsname')
                    marketsByWsName[wsName] = market
            self.options['marketsByWsName'] = marketsByWsName
        return markets

    async def watch_heartbeat(self, params={}):
        await self.load_markets()
        event = 'heartbeat'
        url = self.urls['api']['ws']['public']
        return await self.watch(url, event)

    def handle_heartbeat(self, client, message):
        #
        # every second(approx) if no other updates are sent
        #
        #     {"event": "heartbeat"}
        #
        event = self.safe_string(message, 'event')
        client.resolve(message, event)

    def handle_order_book(self, client, message, subscription):
        #
        # first message(snapshot)
        #
        #     [
        #         1234,  # channelID
        #         {
        #             "as": [
        #                 ["5541.30000", "2.50700000", "1534614248.123678"],
        #                 ["5541.80000", "0.33000000", "1534614098.345543"],
        #                 ["5542.70000", "0.64700000", "1534614244.654432"]
        #             ],
        #             "bs": [
        #                 ["5541.20000", "1.52900000", "1534614248.765567"],
        #                 ["5539.90000", "0.30000000", "1534614241.769870"],
        #                 ["5539.50000", "5.00000000", "1534613831.243486"]
        #             ]
        #         },
        #         "book-10",
        #         "XBT/USD"
        #     ]
        #
        # subsequent updates
        #
        #     [
        #         1234,
        #         { # optional
        #             "a": [
        #                 ["5541.30000", "2.50700000", "1534614248.456738"],
        #                 ["5542.50000", "0.40100000", "1534614248.456738"]
        #             ]
        #         },
        #         { # optional
        #             "b": [
        #                 ["5541.30000", "0.00000000", "1534614335.345903"]
        #             ]
        #         },
        #         "book-10",
        #         "XBT/USD"
        #     ]
        #
        messageLength = len(message)
        wsName = message[messageLength - 1]
        bookDepthString = message[messageLength - 2]
        parts = bookDepthString.split('-')
        depth = self.safe_integer(parts, 1, 10)
        market = self.safe_value(self.options['marketsByWsName'], wsName)
        symbol = market['symbol']
        timestamp = None
        messageHash = 'book:' + wsName
        # if self is a snapshot
        if 'as' in message[1]:
            # todo get depth from marketsByWsName
            self.orderbooks[symbol] = self.order_book({}, depth)
            orderbook = self.orderbooks[symbol]
            sides = {
                'as': 'asks',
                'bs': 'bids',
            }
            keys = list(sides.keys())
            for i in range(0, len(keys)):
                key = keys[i]
                side = sides[key]
                bookside = orderbook[side]
                deltas = self.safe_value(message[1], key, [])
                timestamp = self.handle_deltas(bookside, deltas, timestamp)
            orderbook['timestamp'] = timestamp
            orderbook['datetime'] = self.iso8601(timestamp)
            client.resolve(orderbook, messageHash)
        else:
            orderbook = self.orderbooks[symbol]
            # else, if self is an orderbook update
            a = None
            b = None
            if messageLength == 5:
                a = self.safe_value(message[1], 'a', [])
                b = self.safe_value(message[2], 'b', [])
            else:
                if 'a' in message[1]:
                    a = self.safe_value(message[1], 'a', [])
                else:
                    b = self.safe_value(message[1], 'b', [])
            if a is not None:
                timestamp = self.handle_deltas(orderbook['asks'], a, timestamp)
            if b is not None:
                timestamp = self.handle_deltas(orderbook['bids'], b, timestamp)
            orderbook['timestamp'] = timestamp
            orderbook['datetime'] = self.iso8601(timestamp)
            client.resolve(orderbook, messageHash)

    def handle_deltas(self, bookside, deltas, timestamp):
        for j in range(0, len(deltas)):
            delta = deltas[j]
            price = float(delta[0])
            amount = float(delta[1])
            timestamp = max(timestamp or 0, int(float(delta[2]) * 1000))
            bookside.store(price, amount)
        return timestamp

    def handle_system_status(self, client, message):
        #
        # todo: answer the question whether handleSystemStatus should be renamed
        # and unified as handleStatus for any usage pattern that
        # involves system status and maintenance updates
        #
        #     {
        #         connectionID: 15527282728335292000,
        #         event: 'systemStatus',
        #         status: 'online',  # online|maintenance|(custom status tbd)
        #         version: '0.2.0'
        #     }
        #
        return message

    async def authenticate(self, params={}):
        url = self.urls['api']['ws']['private']
        client = self.client(url)
        authenticated = 'authenticated'
        subscription = self.safe_value(client.subscriptions, authenticated)
        if subscription is None:
            response = await self.privatePostGetWebSocketsToken(params)
            #
            #     {
            #         "error":[],
            #         "result":{
            #             "token":"xeAQ\/RCChBYNVh53sTv1yZ5H4wIbwDF20PiHtTF+4UI",
            #             "expires":900
            #         }
            #     }
            #
            subscription = self.safe_value(response, 'result')
            client.subscriptions[authenticated] = subscription
        return self.safe_string(subscription, 'token')

    async def watch_private(self, name, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        token = await self.authenticate()
        subscriptionHash = name
        messageHash = name
        if symbol is not None:
            messageHash += ':' + symbol
        url = self.urls['api']['ws']['private']
        requestId = self.request_id()
        subscribe = {
            'event': 'subscribe',
            'reqid': requestId,
            'subscription': {
                'name': name,
                'token': token,
            },
        }
        request = self.deep_extend(subscribe, params)
        result = await self.watch(url, messageHash, request, subscriptionHash)
        return self.filter_by_symbol_since_limit(result, symbol, since, limit)

    async def watch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        return await self.watch_private('ownTrades', symbol, since, limit, params)

    def handle_my_trades(self, client, message, subscription=None):
        #
        #     [
        #         [
        #             {
        #                 'TT5UC3-GOIRW-6AZZ6R': {
        #                     cost: '1493.90107',
        #                     fee: '3.88415',
        #                     margin: '0.00000',
        #                     ordertxid: 'OTLAS3-RRHUF-NDWH5A',
        #                     ordertype: 'market',
        #                     pair: 'XBT/USDT',
        #                     postxid: 'TKH2SE-M7IF5-CFI7LT',
        #                     price: '6851.50005',
        #                     time: '1586822919.335498',
        #                     type: 'sell',
        #                     vol: '0.21804000'
        #                 }
        #             },
        #             {
        #                 'TIY6G4-LKLAI-Y3GD4A': {
        #                     cost: '22.17134',
        #                     fee: '0.05765',
        #                     margin: '0.00000',
        #                     ordertxid: 'ODQXS7-MOLK6-ICXKAA',
        #                     ordertype: 'market',
        #                     pair: 'ETH/USD',
        #                     postxid: 'TKH2SE-M7IF5-CFI7LT',
        #                     price: '169.97999',
        #                     time: '1586340530.895739',
        #                     type: 'buy',
        #                     vol: '0.13043500'
        #                 }
        #             },
        #         ],
        #         'ownTrades',
        #         {sequence: 1}
        #     ]
        #
        allTrades = self.safe_value(message, 0, [])
        allTradesLength = len(allTrades)
        if allTradesLength > 0:
            if self.myTrades is None:
                limit = self.safe_integer(self.options, 'tradesLimit', 1000)
                self.myTrades = ArrayCache(limit)
            stored = self.myTrades
            symbols = {}
            for i in range(0, len(allTrades)):
                trades = self.safe_value(allTrades, i, {})
                ids = list(trades.keys())
                for j in range(0, len(ids)):
                    id = ids[j]
                    trade = trades[id]
                    parsed = self.parse_ws_trade(self.extend({'id': id}, trade))
                    stored.append(parsed)
                    symbol = parsed['symbol']
                    symbols[symbol] = True
            name = 'ownTrades'
            client.resolve(self.myTrades, name)
            keys = list(symbols.keys())
            for i in range(0, len(keys)):
                messageHash = name + ':' + keys[i]
                client.resolve(self.myTrades, messageHash)

    def parse_ws_trade(self, trade, market=None):
        #
        #     {
        #         id: 'TIMIRG-WUNNE-RRJ6GT',  # injected from outside
        #         ordertxid: 'OQRPN2-LRHFY-HIFA7D',
        #         postxid: 'TKH2SE-M7IF5-CFI7LT',
        #         pair: 'USDCUSDT',
        #         time: 1586340086.457,
        #         type: 'sell',
        #         ordertype: 'market',
        #         price: '0.99860000',
        #         cost: '22.16892001',
        #         fee: '0.04433784',
        #         vol: '22.20000000',
        #         margin: '0.00000000',
        #         misc: ''
        #     }
        #
        #     {
        #         id: 'TIY6G4-LKLAI-Y3GD4A',
        #         cost: '22.17134',
        #         fee: '0.05765',
        #         margin: '0.00000',
        #         ordertxid: 'ODQXS7-MOLK6-ICXKAA',
        #         ordertype: 'market',
        #         pair: 'ETH/USD',
        #         postxid: 'TKH2SE-M7IF5-CFI7LT',
        #         price: '169.97999',
        #         time: '1586340530.895739',
        #         type: 'buy',
        #         vol: '0.13043500'
        #     }
        #
        wsName = self.safe_string(trade, 'pair')
        market = self.safe_value(self.options['marketsByWsName'], wsName, market)
        symbol = None
        orderId = self.safe_string(trade, 'ordertxid')
        id = self.safe_string_2(trade, 'id', 'postxid')
        timestamp = self.safe_timestamp(trade, 'time')
        side = self.safe_string(trade, 'type')
        type = self.safe_string(trade, 'ordertype')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'vol')
        cost = None
        fee = None
        if 'fee' in trade:
            currency = None
            if market is not None:
                currency = market['quote']
            fee = {
                'cost': self.safe_float(trade, 'fee'),
                'currency': currency,
            }
        if market is not None:
            symbol = market['symbol']
        if price is not None:
            if amount is not None:
                cost = price * amount
        return {
            'id': id,
            'order': orderId,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    async def watch_orders(self, symbol=None, since=None, limit=None, params={}):
        return await self.watch_private('openOrders', symbol, since, limit, params)

    def handle_orders(self, client, message, subscription=None):
        #
        #     [
        #         [
        #             {
        #                 "OGTT3Y-C6I3P-XRI6HX": {
        #                     "cost": "0.00000",
        #                     "descr": {
        #                         "close": "",
        #                         "leverage": "0:1",
        #                         "order": "sell 10.00345345 XBT/EUR @ limit 34.50000 with 0:1 leverage",
        #                         "ordertype": "limit",
        #                         "pair": "XBT/EUR",
        #                         "price": "34.50000",
        #                         "price2": "0.00000",
        #                         "type": "sell"
        #                     },
        #                     "expiretm": "0.000000",
        #                     "fee": "0.00000",
        #                     "limitprice": "34.50000",
        #                     "misc": "",
        #                     "oflags": "fcib",
        #                     "opentm": "0.000000",
        #                     "price": "34.50000",
        #                     "refid": "OKIVMP-5GVZN-Z2D2UA",
        #                     "starttm": "0.000000",
        #                     "status": "open",
        #                     "stopprice": "0.000000",
        #                     "userref": 0,
        #                     "vol": "10.00345345",
        #                     "vol_exec": "0.00000000"
        #                 }
        #             },
        #             {
        #                 "OGTT3Y-C6I3P-XRI6HX": {
        #                     "cost": "0.00000",
        #                     "descr": {
        #                         "close": "",
        #                         "leverage": "0:1",
        #                         "order": "sell 0.00000010 XBT/EUR @ limit 5334.60000 with 0:1 leverage",
        #                         "ordertype": "limit",
        #                         "pair": "XBT/EUR",
        #                         "price": "5334.60000",
        #                         "price2": "0.00000",
        #                         "type": "sell"
        #                     },
        #                     "expiretm": "0.000000",
        #                     "fee": "0.00000",
        #                     "limitprice": "5334.60000",
        #                     "misc": "",
        #                     "oflags": "fcib",
        #                     "opentm": "0.000000",
        #                     "price": "5334.60000",
        #                     "refid": "OKIVMP-5GVZN-Z2D2UA",
        #                     "starttm": "0.000000",
        #                     "status": "open",
        #                     "stopprice": "0.000000",
        #                     "userref": 0,
        #                     "vol": "0.00000010",
        #                     "vol_exec": "0.00000000"
        #                 }
        #             },
        #         ],
        #         "openOrders",
        #         {"sequence": 234}
        #     ]
        #
        # status-change
        #
        #     [
        #         [
        #             {"OGTT3Y-C6I3P-XRI6HX": {"status": "closed"}},
        #             {"OGTT3Y-C6I3P-XRI6HX": {"status": "closed"}},
        #         ],
        #         "openOrders",
        #         {"sequence": 59342}
        #     ]
        #
        allOrders = self.safe_value(message, 0, [])
        allOrdersLength = len(allOrders)
        if allOrdersLength > 0:
            if self.orders is None:
                limit = self.safe_integer(self.options, 'ordersLimit', 1000)
                self.orders = ArrayCacheById(limit)
            stored = self.orders
            symbols = {}
            for i in range(0, len(allOrders)):
                orders = self.safe_value(allOrders, i, {})
                ids = list(orders.keys())
                for j in range(0, len(ids)):
                    id = ids[j]
                    order = orders[id]
                    previousOrder = self.safe_value(stored.hashmap, id)
                    if previousOrder is not None:
                        order = self.extend(previousOrder['info'], order)
                    parsed = self.parse_ws_order(self.extend({'id': id}, order))
                    stored.append(parsed)
                    symbol = parsed['symbol']
                    symbols[symbol] = True
            name = 'openOrders'
            client.resolve(self.orders, name)
            keys = list(symbols.keys())
            for i in range(0, len(keys)):
                messageHash = name + ':' + keys[i]
                client.resolve(self.orders, messageHash)

    def parse_ws_order(self, order, market=None):
        #
        # createOrder
        #
        #     {
        #         descr: {order: 'buy 0.02100000 ETHUSDT @ limit 330.00'},
        #         txid: ['OEKVV2-IH52O-TPL6GZ']
        #     }
        #
        description = self.safe_value(order, 'descr', {})
        orderDescription = self.safe_string(description, 'order')
        side = None
        type = None
        wsName = None
        price = None
        amount = None
        if orderDescription is not None:
            parts = orderDescription.split(' ')
            side = self.safe_string(parts, 0)
            amount = self.safe_float(parts, 1)
            wsName = self.safe_string(parts, 2)
            type = self.safe_string(parts, 4)
            price = self.safe_float(parts, 5)
        side = self.safe_string(description, 'type', side)
        type = self.safe_string(description, 'ordertype', type)
        wsName = self.safe_string(description, 'pair', wsName)
        market = self.safe_value(self.options['marketsByWsName'], wsName, market)
        symbol = None
        timestamp = self.safe_timestamp(order, 'opentm')
        amount = self.safe_float(order, 'vol', amount)
        filled = self.safe_float(order, 'vol_exec')
        remaining = None
        if (amount is not None) and (filled is not None):
            remaining = amount - filled
        fee = None
        cost = self.safe_float(order, 'cost')
        price = self.safe_float(description, 'price', price)
        if (price is None) or (price == 0.0):
            price = self.safe_float(description, 'price2')
        if (price is None) or (price == 0.0):
            price = self.safe_float(order, 'price', price)
        average = self.safe_float(order, 'price')
        if market is not None:
            symbol = market['symbol']
            if 'fee' in order:
                flags = order['oflags']
                feeCost = self.safe_float(order, 'fee')
                fee = {
                    'cost': feeCost,
                    'rate': None,
                }
                if flags.find('fciq') >= 0:
                    fee['currency'] = market['quote']
                elif flags.find('fcib') >= 0:
                    fee['currency'] = market['base']
        status = self.parse_order_status(self.safe_string(order, 'status'))
        id = self.safe_string(order, 'id')
        if id is None:
            txid = self.safe_value(order, 'txid')
            id = self.safe_string(txid, 0)
        clientOrderId = self.safe_string(order, 'userref')
        rawTrades = self.safe_value(order, 'trades')
        trades = None
        if rawTrades is not None:
            trades = self.parse_trades(rawTrades, market, None, None, {'order': id})
        stopPrice = self.safe_float(order, 'stopprice')
        return {
            'id': id,
            'clientOrderId': clientOrderId,
            'info': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': stopPrice,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'average': average,
            'remaining': remaining,
            'fee': fee,
            'trades': trades,
        }

    def handle_subscription_status(self, client, message):
        #
        # public
        #
        #     {
        #         channelID: 210,
        #         channelName: 'book-10',
        #         event: 'subscriptionStatus',
        #         reqid: 1574146735269,
        #         pair: 'ETH/XBT',
        #         status: 'subscribed',
        #         subscription: {depth: 10, name: 'book'}
        #     }
        #
        # private
        #
        #     {
        #         channelName: 'openOrders',
        #         event: 'subscriptionStatus',
        #         reqid: 1,
        #         status: 'subscribed',
        #         subscription: {maxratecount: 125, name: 'openOrders'}
        #     }
        #
        channelId = self.safe_string(message, 'channelID')
        if channelId is not None:
            client.subscriptions[channelId] = message
        # requestId = self.safe_string(message, 'reqid')
        # if requestId in client.futures:
        #     del client.futures[requestId]
        # }

    def handle_error_message(self, client, message):
        #
        #     {
        #         errorMessage: 'Currency pair not in ISO 4217-A3 format foobar',
        #         event: 'subscriptionStatus',
        #         pair: 'foobar',
        #         reqid: 1574146735269,
        #         status: 'error',
        #         subscription: {name: 'ticker'}
        #     }
        #
        errorMessage = self.safe_value(message, 'errorMessage')
        if errorMessage is not None:
            requestId = self.safe_value(message, 'reqid')
            if requestId is not None:
                broad = self.exceptions['ws']['broad']
                broadKey = self.find_broadly_matched_key(broad, errorMessage)
                exception = None
                if broadKey is None:
                    exception = ExchangeError(errorMessage)
                else:
                    exception = broad[broadKey](errorMessage)
                client.reject(exception, requestId)
                return False
        return True

    def handle_message(self, client, message):
        if isinstance(message, list):
            channelId = self.safe_string(message, 0)
            subscription = self.safe_value(client.subscriptions, channelId, {})
            info = self.safe_value(subscription, 'subscription', {})
            messageLength = len(message)
            channelName = self.safe_string(message, messageLength - 2)
            name = self.safe_string(info, 'name')
            methods = {
                # public
                'book': self.handle_order_book,
                'ohlc': self.handle_ohlcv,
                'ticker': self.handle_ticker,
                'trade': self.handle_trades,
                # private
                'openOrders': self.handle_orders,
                'ownTrades': self.handle_my_trades,
            }
            method = self.safe_value_2(methods, name, channelName)
            if method is None:
                return message
            else:
                return method(client, message, subscription)
        else:
            if self.handle_error_message(client, message):
                event = self.safe_string(message, 'event')
                methods = {
                    'heartbeat': self.handle_heartbeat,
                    'systemStatus': self.handle_system_status,
                    'subscriptionStatus': self.handle_subscription_status,
                }
                method = self.safe_value(methods, event)
                if method is None:
                    return message
                else:
                    return method(client, message)
