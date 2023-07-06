// -------------------------------------------------------------------------------

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

// -------------------------------------------------------------------------------

import { implicitReturnType } from '../base/types.js';
import { Exchange as _Exchange } from '../base/Exchange.js';

interface Exchange {
    publicGetOpenapiV1Ping (params?: {}): Promise<implicitReturnType>;
    publicGetOpenapiV1Time (params?: {}): Promise<implicitReturnType>;
    publicGetOpenapiQuoteV1Ticker24hr (params?: {}): Promise<implicitReturnType>;
    publicGetOpenapiQuoteV1TickerPrice (params?: {}): Promise<implicitReturnType>;
    publicGetOpenapiQuoteV1TickerBookTicker (params?: {}): Promise<implicitReturnType>;
    publicGetOpenapiV1ExchangeInfo (params?: {}): Promise<implicitReturnType>;
    publicGetOpenapiQuoteV1Depth (params?: {}): Promise<implicitReturnType>;
    publicGetOpenapiQuoteV1Klines (params?: {}): Promise<implicitReturnType>;
    publicGetOpenapiQuoteV1Trades (params?: {}): Promise<implicitReturnType>;
    publicGetOpenapiV1Pairs (params?: {}): Promise<implicitReturnType>;
    publicGetOpenapiQuoteV1AvgPrice (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiWalletV1ConfigGetall (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiWalletV1DepositAddress (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiWalletV1DepositHistory (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiWalletV1WithdrawHistory (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiV1Account (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiV1OpenOrders (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiV1AssetTradeFee (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiV1Order (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiV1HistoryOrders (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiV1MyTrades (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiV1CapitalDepositHistory (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiV1CapitalWithdrawHistory (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiV3PaymentRequestGetPaymentRequest (params?: {}): Promise<implicitReturnType>;
    privateGetMerchantApiV1GetInvoices (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiAccountV3CryptoAccounts (params?: {}): Promise<implicitReturnType>;
    privateGetOpenapiTransferV3TransfersId (params?: {}): Promise<implicitReturnType>;
    privatePostOpenapiWalletV1WithdrawApply (params?: {}): Promise<implicitReturnType>;
    privatePostOpenapiV1OrderTest (params?: {}): Promise<implicitReturnType>;
    privatePostOpenapiV1Order (params?: {}): Promise<implicitReturnType>;
    privatePostOpenapiV1CapitalWithdrawApply (params?: {}): Promise<implicitReturnType>;
    privatePostOpenapiV1CapitalDepositApply (params?: {}): Promise<implicitReturnType>;
    privatePostOpenapiV3PaymentRequestPaymentRequests (params?: {}): Promise<implicitReturnType>;
    privatePostOpenapiV3PaymentRequestDeletePaymentRequest (params?: {}): Promise<implicitReturnType>;
    privatePostOpenapiV3PaymentRequestPaymentRequestReminder (params?: {}): Promise<implicitReturnType>;
    privatePostOpenapiV1UserDataStream (params?: {}): Promise<implicitReturnType>;
    privatePostMerchantApiV1Invoices (params?: {}): Promise<implicitReturnType>;
    privatePostMerchantApiV1InvoicesCancel (params?: {}): Promise<implicitReturnType>;
    privatePostOpenapiConvertV1GetSupportedTradingPairs (params?: {}): Promise<implicitReturnType>;
    privatePostOpenapiConvertV1GetQuote (params?: {}): Promise<implicitReturnType>;
    privatePostOpenapiConvertV1AccpetQuote (params?: {}): Promise<implicitReturnType>;
    privatePostOpenapiTransferV3Transfers (params?: {}): Promise<implicitReturnType>;
    privateDeleteOpenapiV1Order (params?: {}): Promise<implicitReturnType>;
    privateDeleteOpenapiV1OpenOrders (params?: {}): Promise<implicitReturnType>;
    privateDeleteOpenapiV1UserDataStream (params?: {}): Promise<implicitReturnType>;
}
abstract class Exchange extends _Exchange {}

export default Exchange
