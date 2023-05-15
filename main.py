from plaid import Client as PlaidClient
import os
import math
from typing import List

PLAID_CLIENT_ID='id'
PLAID_SECRET='secret'
PLAID_ENV='sandbox'

plaid_client = PlaidClient(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
                            environment=PLAID_ENV, api_version='2019-05-29')

# https://plaid.com/docs/api/#transactions
MAX_TRANSACTIONS_PER_PAGE = 500
OMIT_CATEGORIES = ["Deposit"]
# cd == Certificate of deposit
OMIT_ACCOUNT_SUBTYPES = ['cd', 'savings', '401a', '401k', '403b', '457b',
    '529', 'brokerage', 'cash isa', 'education savings account', 'fixed annuity',
    'gic', 'health reimbursement arrangement', 'hsa', 'ira', 'isa', 'keogh',
    'lif', 'lira', 'lrif', 'lrsp', 'mutual fund', 'non-taxable brokerage account',
    'pension', 'prif', 'profit sharing plan', 'qshr', 'rdsp', 'resp', 'retirement',
    'rlif', 'roth', 'roth 401k', 'rrif', 'rrsp', 'sarsep', 'sep ira', 'simple ira',
    'sipp', 'stock plan', 'tfsa', 'thrift savings plan', 'trust', 'ugma', 'utma',
    'variable annuity'
]

def get_transactions_resume(access_token: str, start_date: str, end_date: str) -> List[dict]:
    #get_public_access_token()
    account_ids = [account['account_id'] for account in plaid_client.Accounts.get(access_token)['accounts']
                   if account['subtype'] not in OMIT_ACCOUNT_SUBTYPES]

    num_available_transactions = plaid_client.Transactions.get(access_token, start_date, end_date,
                                                               account_ids=account_ids)['total_transactions']
    transactions = []

    transactions += [transaction
                    for transaction in plaid_client.Transactions.get(access_token, start_date, end_date,
                                                                      account_ids=account_ids,
                                                                      count=5)['transactions']
                    if transaction['category'] is None
                    or not any(category in OMIT_CATEGORIES
                              for category in transaction['category'])]

    #print(f"there are {len(transactions)} transactions")
    #pprint([transaction for transaction in transactions if transaction['amount'] < 0])

    return transactions

if __name__ == '__main__':
  token = 'access-sandbox-fc0c3ef0-4cba-421d-9163-31279528668e'
  transactions = get_some_transactions(token, '2020-12-01', '2021-01-26')

  print(len(transactions))