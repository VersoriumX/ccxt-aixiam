import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------
# -*- coding: utf-8 -*-


from ccxt.test.base import test_ledger_entry  # noqa E402


async def test_fetch_ledger_entry(exchange, skipped_properties, code):
    method = 'fetchLedgerEntry'
    items = await exchange.fetch_ledger(code)
    length = len(items)
    if length > 0:
        item = await exchange.fetch_ledger_entry(items[0].id)
        now = exchange.milliseconds()
        test_ledger_entry(exchange, skipped_properties, method, item, code, now)
