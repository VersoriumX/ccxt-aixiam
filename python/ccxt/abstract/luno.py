from ccxt.base.types import Entry


class ImplicitAPI:
    exchange_get_markets = exchangeGetMarkets = Entry('markets', 'exchange', 'GET', {'cost': 1})
    public_get_orderbook = publicGetOrderbook = Entry('orderbook', 'public', 'GET', {'cost': 1})
    public_get_orderbook_top = publicGetOrderbookTop = Entry('orderbook_top', 'public', 'GET', {'cost': 1})
    public_get_ticker = publicGetTicker = Entry('ticker', 'public', 'GET', {'cost': 1})
    public_get_tickers = publicGetTickers = Entry('tickers', 'public', 'GET', {'cost': 1})
    public_get_trades = publicGetTrades = Entry('trades', 'public', 'GET', {'cost': 1})
    private_get_accounts_id_pending = privateGetAccountsIdPending = Entry('accounts/{id}/pending', 'private', 'GET', {'cost': 1})
    private_get_accounts_id_transactions = privateGetAccountsIdTransactions = Entry('accounts/{id}/transactions', 'private', 'GET', {'cost': 1})
    private_get_balance = privateGetBalance = Entry('balance', 'private', 'GET', {'cost': 1})
    private_get_beneficiaries = privateGetBeneficiaries = Entry('beneficiaries', 'private', 'GET', {'cost': 1})
    private_get_fee_info = privateGetFeeInfo = Entry('fee_info', 'private', 'GET', {'cost': 1})
    private_get_funding_address = privateGetFundingAddress = Entry('funding_address', 'private', 'GET', {'cost': 1})
    private_get_listorders = privateGetListorders = Entry('listorders', 'private', 'GET', {'cost': 1})
    private_get_listtrades = privateGetListtrades = Entry('listtrades', 'private', 'GET', {'cost': 1})
    private_get_send_fee = privateGetSendFee = Entry('send_fee', 'private', 'GET', {'cost': 1})
    private_get_orders_id = privateGetOrdersId = Entry('orders/{id}', 'private', 'GET', {'cost': 1})
    private_get_withdrawals = privateGetWithdrawals = Entry('withdrawals', 'private', 'GET', {'cost': 1})
    private_get_withdrawals_id = privateGetWithdrawalsId = Entry('withdrawals/{id}', 'private', 'GET', {'cost': 1})
    private_get_transfers = privateGetTransfers = Entry('transfers', 'private', 'GET', {'cost': 1})
    private_post_accounts = privatePostAccounts = Entry('accounts', 'private', 'POST', {'cost': 1})
    private_post_address_validate = privatePostAddressValidate = Entry('address/validate', 'private', 'POST', {'cost': 1})
    private_post_postorder = privatePostPostorder = Entry('postorder', 'private', 'POST', {'cost': 1})
    private_post_marketorder = privatePostMarketorder = Entry('marketorder', 'private', 'POST', {'cost': 1})
    private_post_stoporder = privatePostStoporder = Entry('stoporder', 'private', 'POST', {'cost': 1})
    private_post_funding_address = privatePostFundingAddress = Entry('funding_address', 'private', 'POST', {'cost': 1})
    private_post_withdrawals = privatePostWithdrawals = Entry('withdrawals', 'private', 'POST', {'cost': 1})
    private_post_send = privatePostSend = Entry('send', 'private', 'POST', {'cost': 1})
    private_post_oauth2_grant = privatePostOauth2Grant = Entry('oauth2/grant', 'private', 'POST', {'cost': 1})
    private_put_accounts_id_name = privatePutAccountsIdName = Entry('accounts/{id}/name', 'private', 'PUT', {'cost': 1})
    private_delete_withdrawals_id = privateDeleteWithdrawalsId = Entry('withdrawals/{id}', 'private', 'DELETE', {'cost': 1})
