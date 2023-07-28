<?php

namespace ccxt\async;

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

use Exception; // a common import
use ccxt\async\abstract\independentreserve as Exchange;
use ccxt\Precise;
use React\Async;

class independentreserve extends Exchange {

    public function describe() {
        return $this->deep_extend(parent::describe(), array(
            'id' => 'independentreserve',
            'name' => 'Independent Reserve',
            'countries' => array( 'AU', 'NZ' ), // Australia, New Zealand
            'rateLimit' => 1000,
            'pro' => true,
            'has' => array(
                'CORS' => null,
                'spot' => true,
                'margin' => false,
                'swap' => false,
                'future' => false,
                'option' => false,
                'addMargin' => false,
                'cancelOrder' => true,
                'createOrder' => true,
                'createReduceOnlyOrder' => false,
                'createStopLimitOrder' => false,
                'createStopMarketOrder' => false,
                'createStopOrder' => false,
                'fetchBalance' => true,
                'fetchBorrowRate' => false,
                'fetchBorrowRateHistories' => false,
                'fetchBorrowRateHistory' => false,
                'fetchBorrowRates' => false,
                'fetchBorrowRatesPerSymbol' => false,
                'fetchClosedOrders' => true,
                'fetchFundingHistory' => false,
                'fetchFundingRate' => false,
                'fetchFundingRateHistory' => false,
                'fetchFundingRates' => false,
                'fetchIndexOHLCV' => false,
                'fetchLeverage' => false,
                'fetchLeverageTiers' => false,
                'fetchMarginMode' => false,
                'fetchMarkets' => true,
                'fetchMarkOHLCV' => false,
                'fetchMyTrades' => true,
                'fetchOpenInterestHistory' => false,
                'fetchOpenOrders' => true,
                'fetchOrder' => true,
                'fetchOrderBook' => true,
                'fetchPosition' => false,
                'fetchPositionMode' => false,
                'fetchPositions' => false,
                'fetchPositionsRisk' => false,
                'fetchPremiumIndexOHLCV' => false,
                'fetchTicker' => true,
                'fetchTrades' => true,
                'fetchTradingFee' => false,
                'fetchTradingFees' => true,
                'reduceMargin' => false,
                'setLeverage' => false,
                'setMarginMode' => false,
                'setPositionMode' => false,
            ),
            'urls' => array(
                'logo' => 'https://user-images.githubusercontent.com/51840849/87182090-1e9e9080-c2ec-11ea-8e49-563db9a38f37.jpg',
                'api' => array(
                    'public' => 'https://api.independentreserve.com/Public',
                    'private' => 'https://api.independentreserve.com/Private',
                ),
                'www' => 'https://www.independentreserve.com',
                'doc' => 'https://www.independentreserve.com/API',
            ),
            'api' => array(
                'public' => array(
                    'get' => array(
                        'GetValidPrimaryCurrencyCodes',
                        'GetValidSecondaryCurrencyCodes',
                        'GetValidLimitOrderTypes',
                        'GetValidMarketOrderTypes',
                        'GetValidOrderTypes',
                        'GetValidTransactionTypes',
                        'GetMarketSummary',
                        'GetOrderBook',
                        'GetAllOrders',
                        'GetTradeHistorySummary',
                        'GetRecentTrades',
                        'GetFxRates',
                        'GetOrderMinimumVolumes',
                        'GetCryptoWithdrawalFees',
                    ),
                ),
                'private' => array(
                    'post' => array(
                        'GetOpenOrders',
                        'GetClosedOrders',
                        'GetClosedFilledOrders',
                        'GetOrderDetails',
                        'GetAccounts',
                        'GetTransactions',
                        'GetFiatBankAccounts',
                        'GetDigitalCurrencyDepositAddress',
                        'GetDigitalCurrencyDepositAddresses',
                        'GetTrades',
                        'GetBrokerageFees',
                        'GetDigitalCurrencyWithdrawal',
                        'PlaceLimitOrder',
                        'PlaceMarketOrder',
                        'CancelOrder',
                        'SynchDigitalCurrencyDepositAddressWithBlockchain',
                        'RequestFiatWithdrawal',
                        'WithdrawFiatCurrency',
                        'WithdrawDigitalCurrency',
                    ),
                ),
            ),
            'fees' => array(
                'trading' => array(
                    'taker' => $this->parse_number('0.005'),
                    'maker' => $this->parse_number('0.005'),
                    'percentage' => true,
                    'tierBased' => false,
                ),
            ),
            'commonCurrencies' => array(
                'PLA' => 'PlayChip',
            ),
            'precisionMode' => TICK_SIZE,
        ));
    }

    public function fetch_markets($params = array ()) {
        return Async\async(function () use ($params) {
            /**
             * retrieves data on all markets for independentreserve
             * @param {array} [$params] extra parameters specific to the exchange api endpoint
             * @return {array[]} an array of objects representing market data
             */
            $baseCurrencies = Async\await($this->publicGetGetValidPrimaryCurrencyCodes ($params));
            //     ['Xbt', 'Eth', 'Usdt', ...]
            $quoteCurrencies = Async\await($this->publicGetGetValidSecondaryCurrencyCodes ($params));
            //     ['Aud', 'Usd', 'Nzd', 'Sgd']
            $limits = Async\await($this->publicGetGetOrderMinimumVolumes ($params));
            //
            //     {
            //         "Xbt" => 0.0001,
            //         "Eth" => 0.001,
            //         "Ltc" => 0.01,
            //         "Xrp" => 1.0,
            //     }
            //
            $result = array();
            for ($i = 0; $i < count($baseCurrencies); $i++) {
                $baseId = $baseCurrencies[$i];
                $base = $this->safe_currency_code($baseId);
                $minAmount = $this->safe_number($limits, $baseId);
                for ($j = 0; $j < count($quoteCurrencies); $j++) {
                    $quoteId = $quoteCurrencies[$j];
                    $quote = $this->safe_currency_code($quoteId);
                    $id = $baseId . '/' . $quoteId;
                    $result[] = array(
                        'id' => $id,
                        'symbol' => $base . '/' . $quote,
                        'base' => $base,
                        'quote' => $quote,
                        'settle' => null,
                        'baseId' => $baseId,
                        'quoteId' => $quoteId,
                        'settleId' => null,
                        'type' => 'spot',
                        'spot' => true,
                        'margin' => false,
                        'swap' => false,
                        'future' => false,
                        'option' => false,
                        'active' => null,
                        'contract' => false,
                        'linear' => null,
                        'inverse' => null,
                        'contractSize' => null,
                        'expiry' => null,
                        'expiryDatetime' => null,
                        'strike' => null,
                        'optionType' => null,
                        'precision' => array(
                            'amount' => null,
                            'price' => null,
                        ),
                        'limits' => array(
                            'leverage' => array(
                                'min' => null,
                                'max' => null,
                            ),
                            'amount' => array(
                                'min' => $minAmount,
                                'max' => null,
                            ),
                            'price' => array(
                                'min' => null,
                                'max' => null,
                            ),
                            'cost' => array(
                                'min' => null,
                                'max' => null,
                            ),
                        ),
                        'info' => $id,
                    );
                }
            }
            return $result;
        }) ();
    }

    public function parse_balance($response) {
        $result = array( 'info' => $response );
        for ($i = 0; $i < count($response); $i++) {
            $balance = $response[$i];
            $currencyId = $this->safe_string($balance, 'CurrencyCode');
            $code = $this->safe_currency_code($currencyId);
            $account = $this->account();
            $account['free'] = $this->safe_string($balance, 'AvailableBalance');
            $account['total'] = $this->safe_string($balance, 'TotalBalance');
            $result[$code] = $account;
        }
        return $this->safe_balance($result);
    }

    public function fetch_balance($params = array ()) {
        return Async\async(function () use ($params) {
            /**
             * query for balance and get the amount of funds available for trading or funds locked in orders
             * @param {array} [$params] extra parameters specific to the independentreserve api endpoint
             * @return {array} a ~@link https://docs.ccxt.com/en/latest/manual.html?#balance-structure balance structure~
             */
            Async\await($this->load_markets());
            $response = Async\await($this->privatePostGetAccounts ($params));
            return $this->parse_balance($response);
        }) ();
    }

    public function fetch_order_book(string $symbol, ?int $limit = null, $params = array ()) {
        return Async\async(function () use ($symbol, $limit, $params) {
            /**
             * fetches information on open orders with bid (buy) and ask (sell) prices, volumes and other data
             * @param {string} $symbol unified $symbol of the $market to fetch the order book for
             * @param {int} [$limit] the maximum amount of order book entries to return
             * @param {array} [$params] extra parameters specific to the independentreserve api endpoint
             * @return {array} A dictionary of ~@link https://docs.ccxt.com/#/?id=order-book-structure order book structures~ indexed by $market symbols
             */
            Async\await($this->load_markets());
            $market = $this->market($symbol);
            $request = array(
                'primaryCurrencyCode' => $market['baseId'],
                'secondaryCurrencyCode' => $market['quoteId'],
            );
            $response = Async\await($this->publicGetGetOrderBook (array_merge($request, $params)));
            $timestamp = $this->parse8601($this->safe_string($response, 'CreatedTimestampUtc'));
            return $this->parse_order_book($response, $market['symbol'], $timestamp, 'BuyOrders', 'SellOrders', 'Price', 'Volume');
        }) ();
    }

    public function parse_ticker($ticker, $market = null) {
        // {
        //     "DayHighestPrice":43489.49,
        //     "DayLowestPrice":41998.32,
        //     "DayAvgPrice":42743.9,
        //     "DayVolumeXbt":44.54515625000,
        //     "DayVolumeXbtInSecondaryCurrrency":0.12209818,
        //     "CurrentLowestOfferPrice":43619.64,
        //     "CurrentHighestBidPrice":43153.58,
        //     "LastPrice":43378.43,
        //     "PrimaryCurrencyCode":"Xbt",
        //     "SecondaryCurrencyCode":"Usd",
        //     "CreatedTimestampUtc":"2022-01-14T22:52:29.5029223Z"
        // }
        $timestamp = $this->parse8601($this->safe_string($ticker, 'CreatedTimestampUtc'));
        $baseId = $this->safe_string($ticker, 'PrimaryCurrencyCode');
        $quoteId = $this->safe_string($ticker, 'SecondaryCurrencyCode');
        $defaultMarketId = null;
        if (($baseId !== null) && ($quoteId !== null)) {
            $defaultMarketId = $baseId . '/' . $quoteId;
        }
        $market = $this->safe_market($defaultMarketId, $market, '/');
        $symbol = $market['symbol'];
        $last = $this->safe_string($ticker, 'LastPrice');
        return $this->safe_ticker(array(
            'symbol' => $symbol,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'high' => $this->safe_string($ticker, 'DayHighestPrice'),
            'low' => $this->safe_string($ticker, 'DayLowestPrice'),
            'bid' => $this->safe_string($ticker, 'CurrentHighestBidPrice'),
            'bidVolume' => null,
            'ask' => $this->safe_string($ticker, 'CurrentLowestOfferPrice'),
            'askVolume' => null,
            'vwap' => null,
            'open' => null,
            'close' => $last,
            'last' => $last,
            'previousClose' => null,
            'change' => null,
            'percentage' => null,
            'average' => $this->safe_string($ticker, 'DayAvgPrice'),
            'baseVolume' => $this->safe_string($ticker, 'DayVolumeXbtInSecondaryCurrrency'),
            'quoteVolume' => null,
            'info' => $ticker,
        ), $market);
    }

    public function fetch_ticker(string $symbol, $params = array ()) {
        return Async\async(function () use ($symbol, $params) {
            /**
             * fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific $market
             * @param {string} $symbol unified $symbol of the $market to fetch the ticker for
             * @param {array} [$params] extra parameters specific to the independentreserve api endpoint
             * @return {array} a ~@link https://docs.ccxt.com/#/?id=ticker-structure ticker structure~
             */
            Async\await($this->load_markets());
            $market = $this->market($symbol);
            $request = array(
                'primaryCurrencyCode' => $market['baseId'],
                'secondaryCurrencyCode' => $market['quoteId'],
            );
            $response = Async\await($this->publicGetGetMarketSummary (array_merge($request, $params)));
            // {
            //     "DayHighestPrice":43489.49,
            //     "DayLowestPrice":41998.32,
            //     "DayAvgPrice":42743.9,
            //     "DayVolumeXbt":44.54515625000,
            //     "DayVolumeXbtInSecondaryCurrrency":0.12209818,
            //     "CurrentLowestOfferPrice":43619.64,
            //     "CurrentHighestBidPrice":43153.58,
            //     "LastPrice":43378.43,
            //     "PrimaryCurrencyCode":"Xbt",
            //     "SecondaryCurrencyCode":"Usd",
            //     "CreatedTimestampUtc":"2022-01-14T22:52:29.5029223Z"
            // }
            return $this->parse_ticker($response, $market);
        }) ();
    }

    public function parse_order($order, $market = null) {
        //
        // fetchOrder
        //
        //     {
        //         "OrderGuid" => "c7347e4c-b865-4c94-8f74-d934d4b0b177",
        //         "CreatedTimestampUtc" => "2014-09-23T12:39:34.3817763Z",
        //         "Type" => "MarketBid",
        //         "VolumeOrdered" => 5.0,
        //         "VolumeFilled" => 5.0,
        //         "Price" => null,
        //         "AvgPrice" => 100.0,
        //         "ReservedAmount" => 0.0,
        //         "Status" => "Filled",
        //         "PrimaryCurrencyCode" => "Xbt",
        //         "SecondaryCurrencyCode" => "Usd"
        //     }
        //
        // fetchOpenOrders & fetchClosedOrders
        //
        //     {
        //         "OrderGuid" => "b8f7ad89-e4e4-4dfe-9ea3-514d38b5edb3",
        //         "CreatedTimestampUtc" => "2020-09-08T03:04:18.616367Z",
        //         "OrderType" => "LimitOffer",
        //         "Volume" => 0.0005,
        //         "Outstanding" => 0.0005,
        //         "Price" => 113885.83,
        //         "AvgPrice" => 113885.83,
        //         "Value" => 56.94,
        //         "Status" => "Open",
        //         "PrimaryCurrencyCode" => "Xbt",
        //         "SecondaryCurrencyCode" => "Usd",
        //         "FeePercent" => 0.005,
        //     }
        //
        $symbol = null;
        $baseId = $this->safe_string($order, 'PrimaryCurrencyCode');
        $quoteId = $this->safe_string($order, 'SecondaryCurrencyCode');
        $base = null;
        $quote = null;
        if (($baseId !== null) && ($quoteId !== null)) {
            $base = $this->safe_currency_code($baseId);
            $quote = $this->safe_currency_code($quoteId);
            $symbol = $base . '/' . $quote;
        } elseif ($market !== null) {
            $symbol = $market['symbol'];
            $base = $market['base'];
            $quote = $market['quote'];
        }
        $orderType = $this->safe_string_2($order, 'Type', 'OrderType');
        $side = null;
        if ($orderType !== null) {
            if (mb_strpos($orderType, 'Bid') !== false) {
                $side = 'buy';
            } elseif (mb_strpos($orderType, 'Offer') !== false) {
                $side = 'sell';
            }
            if (mb_strpos($orderType, 'Market') !== false) {
                $orderType = 'market';
            } elseif (mb_strpos($orderType, 'Limit') !== false) {
                $orderType = 'limit';
            }
        }
        $timestamp = $this->parse8601($this->safe_string($order, 'CreatedTimestampUtc'));
        $filled = $this->safe_string($order, 'VolumeFilled');
        $feeRate = $this->safe_string($order, 'FeePercent');
        $feeCost = null;
        if ($feeRate !== null && $filled !== null) {
            $feeCost = Precise::string_mul($feeRate, $filled);
        }
        return $this->safe_order(array(
            'info' => $order,
            'id' => $this->safe_string($order, 'OrderGuid'),
            'clientOrderId' => null,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'lastTradeTimestamp' => null,
            'symbol' => $symbol,
            'type' => $orderType,
            'timeInForce' => null,
            'postOnly' => null,
            'side' => $side,
            'price' => $this->safe_string($order, 'Price'),
            'stopPrice' => null,
            'triggerPrice' => null,
            'cost' => $this->safe_string($order, 'Value'),
            'average' => $this->safe_string($order, 'AvgPrice'),
            'amount' => $this->safe_string_2($order, 'VolumeOrdered', 'Volume'),
            'filled' => $filled,
            'remaining' => $this->safe_string($order, 'Outstanding'),
            'status' => $this->parse_order_status($this->safe_string($order, 'Status')),
            'fee' => array(
                'rate' => $feeRate,
                'cost' => $feeCost,
                'currency' => $base,
            ),
            'trades' => null,
        ), $market);
    }

    public function parse_order_status($status) {
        $statuses = array(
            'Open' => 'open',
            'PartiallyFilled' => 'open',
            'Filled' => 'closed',
            'PartiallyFilledAndCancelled' => 'canceled',
            'Cancelled' => 'canceled',
            'PartiallyFilledAndExpired' => 'canceled',
            'Expired' => 'canceled',
        );
        return $this->safe_string($statuses, $status, $status);
    }

    public function fetch_order(string $id, ?string $symbol = null, $params = array ()) {
        return Async\async(function () use ($id, $symbol, $params) {
            /**
             * fetches information on an order made by the user
             * @param {string} $symbol unified $symbol of the $market the order was made in
             * @param {array} [$params] extra parameters specific to the independentreserve api endpoint
             * @return {array} An ~@link https://docs.ccxt.com/#/?$id=order-structure order structure~
             */
            Async\await($this->load_markets());
            $response = Async\await($this->privatePostGetOrderDetails (array_merge(array(
                'orderGuid' => $id,
            ), $params)));
            $market = null;
            if ($symbol !== null) {
                $market = $this->market($symbol);
            }
            return $this->parse_order($response, $market);
        }) ();
    }

    public function fetch_open_orders(?string $symbol = null, ?int $since = null, ?int $limit = null, $params = array ()) {
        return Async\async(function () use ($symbol, $since, $limit, $params) {
            /**
             * fetch all unfilled currently open orders
             * @param {string} $symbol unified $market $symbol
             * @param {int} [$since] the earliest time in ms to fetch open orders for
             * @param {int} [$limit] the maximum number of  open orders structures to retrieve
             * @param {array} [$params] extra parameters specific to the independentreserve api endpoint
             * @return {Order[]} a list of ~@link https://docs.ccxt.com/#/?id=order-structure order structures~
             */
            Async\await($this->load_markets());
            $request = $this->ordered(array());
            $market = null;
            if ($symbol !== null) {
                $market = $this->market($symbol);
                $request['primaryCurrencyCode'] = $market['baseId'];
                $request['secondaryCurrencyCode'] = $market['quoteId'];
            }
            if ($limit === null) {
                $limit = 50;
            }
            $request['pageIndex'] = 1;
            $request['pageSize'] = $limit;
            $response = Async\await($this->privatePostGetOpenOrders (array_merge($request, $params)));
            $data = $this->safe_value($response, 'Data', array());
            return $this->parse_orders($data, $market, $since, $limit);
        }) ();
    }

    public function fetch_closed_orders(?string $symbol = null, ?int $since = null, ?int $limit = null, $params = array ()) {
        return Async\async(function () use ($symbol, $since, $limit, $params) {
            /**
             * fetches information on multiple closed orders made by the user
             * @param {string} $symbol unified $market $symbol of the $market orders were made in
             * @param {int} [$since] the earliest time in ms to fetch orders for
             * @param {int} [$limit] the maximum number of  orde structures to retrieve
             * @param {array} [$params] extra parameters specific to the independentreserve api endpoint
             * @return {Order[]} a list of ~@link https://docs.ccxt.com/#/?id=order-structure order structures~
             */
            Async\await($this->load_markets());
            $request = $this->ordered(array());
            $market = null;
            if ($symbol !== null) {
                $market = $this->market($symbol);
                $request['primaryCurrencyCode'] = $market['baseId'];
                $request['secondaryCurrencyCode'] = $market['quoteId'];
            }
            if ($limit === null) {
                $limit = 50;
            }
            $request['pageIndex'] = 1;
            $request['pageSize'] = $limit;
            $response = Async\await($this->privatePostGetClosedOrders (array_merge($request, $params)));
            $data = $this->safe_value($response, 'Data', array());
            return $this->parse_orders($data, $market, $since, $limit);
        }) ();
    }

    public function fetch_my_trades(?string $symbol = null, ?int $since = null, $limit = 50, $params = array ()) {
        return Async\async(function () use ($symbol, $since, $limit, $params) {
            /**
             * fetch all trades made by the user
             * @param {string} $symbol unified $market $symbol
             * @param {int} [$since] the earliest time in ms to fetch trades for
             * @param {int} [$limit] the maximum number of trades structures to retrieve
             * @param {array} [$params] extra parameters specific to the independentreserve api endpoint
             * @return {Trade[]} a list of ~@link https://docs.ccxt.com/#/?id=trade-structure trade structures~
             */
            Async\await($this->load_markets());
            $pageIndex = $this->safe_integer($params, 'pageIndex', 1);
            if ($limit === null) {
                $limit = 50;
            }
            $request = $this->ordered(array(
                'pageIndex' => $pageIndex,
                'pageSize' => $limit,
            ));
            $response = Async\await($this->privatePostGetTrades (array_merge($request, $params)));
            $market = null;
            if ($symbol !== null) {
                $market = $this->market($symbol);
            }
            return $this->parse_trades($response['Data'], $market, $since, $limit);
        }) ();
    }

    public function parse_trade($trade, $market = null) {
        $timestamp = $this->parse8601($trade['TradeTimestampUtc']);
        $id = $this->safe_string($trade, 'TradeGuid');
        $orderId = $this->safe_string($trade, 'OrderGuid');
        $priceString = $this->safe_string_2($trade, 'Price', 'SecondaryCurrencyTradePrice');
        $amountString = $this->safe_string_2($trade, 'VolumeTraded', 'PrimaryCurrencyAmount');
        $price = $this->parse_number($priceString);
        $amount = $this->parse_number($amountString);
        $cost = $this->parse_number(Precise::string_mul($priceString, $amountString));
        $baseId = $this->safe_string($trade, 'PrimaryCurrencyCode');
        $quoteId = $this->safe_string($trade, 'SecondaryCurrencyCode');
        $marketId = null;
        if (($baseId !== null) && ($quoteId !== null)) {
            $marketId = $baseId . '/' . $quoteId;
        }
        $symbol = $this->safe_symbol($marketId, $market, '/');
        $side = $this->safe_string($trade, 'OrderType');
        if ($side !== null) {
            if (mb_strpos($side, 'Bid') !== false) {
                $side = 'buy';
            } elseif (mb_strpos($side, 'Offer') !== false) {
                $side = 'sell';
            }
        }
        return $this->safe_trade(array(
            'id' => $id,
            'info' => $trade,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'symbol' => $symbol,
            'order' => $orderId,
            'type' => null,
            'side' => $side,
            'takerOrMaker' => null,
            'price' => $price,
            'amount' => $amount,
            'cost' => $cost,
            'fee' => null,
        ), $market);
    }

    public function fetch_trades(string $symbol, ?int $since = null, ?int $limit = null, $params = array ()) {
        return Async\async(function () use ($symbol, $since, $limit, $params) {
            /**
             * get the list of most recent trades for a particular $symbol
             * @param {string} $symbol unified $symbol of the $market to fetch trades for
             * @param {int} [$since] timestamp in ms of the earliest trade to fetch
             * @param {int} [$limit] the maximum amount of trades to fetch
             * @param {array} [$params] extra parameters specific to the independentreserve api endpoint
             * @return {Trade[]} a list of ~@link https://docs.ccxt.com/en/latest/manual.html?#public-trades trade structures~
             */
            Async\await($this->load_markets());
            $market = $this->market($symbol);
            $request = array(
                'primaryCurrencyCode' => $market['baseId'],
                'secondaryCurrencyCode' => $market['quoteId'],
                'numberOfRecentTradesToRetrieve' => 50, // max = 50
            );
            $response = Async\await($this->publicGetGetRecentTrades (array_merge($request, $params)));
            return $this->parse_trades($response['Trades'], $market, $since, $limit);
        }) ();
    }

    public function fetch_trading_fees($params = array ()) {
        return Async\async(function () use ($params) {
            /**
             * fetch the trading $fees for multiple markets
             * @param {array} [$params] extra parameters specific to the independentreserve api endpoint
             * @return {array} a dictionary of ~@link https://docs.ccxt.com/#/?id=$fee-structure $fee structures~ indexed by $market symbols
             */
            Async\await($this->load_markets());
            $response = Async\await($this->privatePostGetBrokerageFees ($params));
            //
            //     array(
            //         {
            //             "CurrencyCode" => "Xbt",
            //             "Fee" => 0.005
            //         }
            //         ...
            //     )
            //
            $fees = array();
            for ($i = 0; $i < count($response); $i++) {
                $fee = $response[$i];
                $currencyId = $this->safe_string($fee, 'CurrencyCode');
                $code = $this->safe_currency_code($currencyId);
                $tradingFee = $this->safe_number($fee, 'Fee');
                $fees[$code] = array(
                    'info' => $fee,
                    'fee' => $tradingFee,
                );
            }
            $result = array();
            for ($i = 0; $i < count($this->symbols); $i++) {
                $symbol = $this->symbols[$i];
                $market = $this->market($symbol);
                $fee = $this->safe_value($fees, $market['base'], array());
                $result[$symbol] = array(
                    'info' => $this->safe_value($fee, 'info'),
                    'symbol' => $symbol,
                    'maker' => $this->safe_number($fee, 'fee'),
                    'taker' => $this->safe_number($fee, 'fee'),
                    'percentage' => true,
                    'tierBased' => true,
                );
            }
            return $result;
        }) ();
    }

    public function create_order(string $symbol, string $type, string $side, $amount, $price = null, $params = array ()) {
        return Async\async(function () use ($symbol, $type, $side, $amount, $price, $params) {
            /**
             * create a trade order
             * @param {string} $symbol unified $symbol of the $market to create an order in
             * @param {string} $type 'market' or 'limit'
             * @param {string} $side 'buy' or 'sell'
             * @param {float} $amount how much of currency you want to trade in units of base currency
             * @param {float} $price the $price at which the order is to be fullfilled, in units of the quote currency, ignored in $market orders
             * @param {array} [$params] extra parameters specific to the independentreserve api endpoint
             * @return {array} an ~@link https://docs.ccxt.com/#/?id=order-structure order structure~
             */
            Async\await($this->load_markets());
            $market = $this->market($symbol);
            $capitalizedOrderType = $this->capitalize($type);
            $method = 'privatePostPlace' . $capitalizedOrderType . 'Order';
            $orderType = $capitalizedOrderType;
            $orderType .= ($side === 'sell') ? 'Offer' : 'Bid';
            $request = $this->ordered(array(
                'primaryCurrencyCode' => $market['baseId'],
                'secondaryCurrencyCode' => $market['quoteId'],
                'orderType' => $orderType,
            ));
            if ($type === 'limit') {
                $request['price'] = $price;
            }
            $request['volume'] = $amount;
            $response = Async\await($this->$method (array_merge($request, $params)));
            return $this->safe_order(array(
                'info' => $response,
                'id' => $response['OrderGuid'],
            ), $market);
        }) ();
    }

    public function cancel_order(string $id, ?string $symbol = null, $params = array ()) {
        return Async\async(function () use ($id, $symbol, $params) {
            /**
             * cancels an open order
             * @param {string} $id order $id
             * @param {string} $symbol unified $symbol of the market the order was made in
             * @param {array} [$params] extra parameters specific to the independentreserve api endpoint
             * @return {array} An ~@link https://docs.ccxt.com/#/?$id=order-structure order structure~
             */
            Async\await($this->load_markets());
            $request = array(
                'orderGuid' => $id,
            );
            return Async\await($this->privatePostCancelOrder (array_merge($request, $params)));
        }) ();
    }

    public function sign($path, $api = 'public', $method = 'GET', $params = array (), $headers = null, $body = null) {
        $url = $this->urls['api'][$api] . '/' . $path;
        if ($api === 'public') {
            if ($params) {
                $url .= '?' . $this->urlencode($params);
            }
        } else {
            $this->check_required_credentials();
            $nonce = $this->nonce();
            $auth = array(
                $url,
                'apiKey=' . $this->apiKey,
                'nonce=' . (string) $nonce,
            );
            $keys = is_array($params) ? array_keys($params) : array();
            for ($i = 0; $i < count($keys); $i++) {
                $key = $keys[$i];
                $value = (string) $params[$key];
                $auth[] = $key . '=' . $value;
            }
            $message = implode(',', $auth);
            $signature = $this->hmac($this->encode($message), $this->encode($this->secret), 'sha256');
            $query = $this->ordered(array());
            $query['apiKey'] = $this->apiKey;
            $query['nonce'] = $nonce;
            $query['signature'] = strtoupper($signature);
            for ($i = 0; $i < count($keys); $i++) {
                $key = $keys[$i];
                $query[$key] = $params[$key];
            }
            $body = $this->json($query);
            $headers = array( 'Content-Type' => 'application/json' );
        }
        return array( 'url' => $url, 'method' => $method, 'body' => $body, 'headers' => $headers );
    }
}
