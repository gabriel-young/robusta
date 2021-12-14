"""Payments engine that reads a series of transactions from a CSV file, handles disputes
and chargebacks, and then outputs the state of clients accounts."""

import argparse
import csv

# Constants
import sys

DEPOSIT = 'deposit'
WITHDRAWAL = 'withdrawal'
AVAILABLE = 'available'
DISPUTE = 'dispute'
RESOLVE = 'resolve'
CHARGEBACK = 'chargeback'
TOTAL = 'total'
HELD = 'held'
LOCKED = 'locked'


def get_client_transactions_from_csv_file(input_file):
    """ Get client transactions as stored as a dict, given a csv as an input_file
    :param input_file: CSV File containing client transactions
    :return: Dict
    """
    transactions = {}
    try:
        with open(input_file, newline='', encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(
                csv_file, skipinitialspace=True, delimiter=',', quoting=csv.QUOTE_NONE)
            for row in reader:
                transaction_type, client, transaction_id, amount = list(row.values())
                amount = amount if amount else '0'

                if transaction_id:
                    try:
                        client = int(client) % 2**16
                        transaction_id = int(transaction_id) % 2 ** 32
                        transaction_type = str(transaction_type)
                        amount = float(f'{float(amount):.4f}')
                    except ValueError:
                        sys.exit(
                            f"DataType for type must be a string. Value: {transaction_type}\n"
                            f"DataType for client must be an integer. Value: {client}\n"
                            f"DataType for tx must be an integer. Value: {transaction_id}\n"
                            f"DataType for amount must be a float. Value: {amount}"
                        )

                    if client not in transactions:
                        transactions[client] = []

                    transactions[client].append([
                        transaction_id,
                        transaction_type,
                        amount
                    ])
    except FileNotFoundError:
        print(f"Input File:{input_file} not found")

    return transactions


def deposit(accounts, amount, client):
    """Deposit action into client account

    :param accounts: Dictionary containing all accounts
    :param amount: Amount specified for deposit
    :param client: Specified client for deposit action
    :return: Dict
    """

    if amount:
        if client not in accounts:
            accounts[client] = {
                AVAILABLE: 0.0,
                HELD: 0.0,
                TOTAL: 0.0,
                LOCKED: False
            }

        accounts[client][AVAILABLE] += amount
        accounts[client][TOTAL] += amount
    return accounts


def withdrawal(accounts, amount, client):
    """Withdrawal action into client account

    :param accounts: Dictionary containing all accounts
    :param amount: Amount specified for withdrawal
    :param client: Specified client for withdrawal action
    :return: Dictionary containing all accounts after update
    """
    if accounts[client][AVAILABLE] - amount >= 0:
        accounts[client][AVAILABLE] -= amount
        accounts[client][TOTAL] -= amount
    return accounts


def dispute(accounts, client, prior_amount, prior_transaction_type):
    """Dispute action by client from prior transaction

    :param accounts: Dictionary containing all accounts
    :param client: Client specified for dispute
    :param prior_amount: Amount specified for dispute
    :param prior_transaction_type: Prior transaction referencing dispute
    :return: Dict
    """
    if prior_transaction_type == DEPOSIT:
        accounts[client][AVAILABLE] -= prior_amount
    elif prior_transaction_type == WITHDRAWAL:
        accounts[client][AVAILABLE] += prior_amount
    accounts[client][HELD] += prior_amount

    return accounts


def resolve(accounts, client, prior_transaction):
    """Resolve action to disregard dispute action

    :param accounts: Dictionary containing all accounts
    :param client: Client specified for resolve
    :param prior_transaction: List having amount to be resolved, and transaction type
    :return: Dict
    """
    _, prior_transaction_type, prior_amount, referenced_transaction = prior_transaction

    if prior_transaction_type == DISPUTE:
        if referenced_transaction == DEPOSIT:
            accounts[client][AVAILABLE] += prior_amount
        elif referenced_transaction == WITHDRAWAL:
            accounts[client][AVAILABLE] -= prior_amount
        accounts[client][HELD] -= prior_amount

    return accounts


def chargeback(accounts, client, prior_transaction):
    """Chargeback action to reverse transaction regarding dispute action

    :param accounts: Dictionary containing all accounts
    :param client: Client specified for chargeback
    :param prior_transaction: List having amount to be resolved, and transaction type
    :return: Dict
    """
    _, prior_transaction_type, prior_amount, referenced_transaction = prior_transaction

    if prior_transaction_type == DISPUTE:
        if referenced_transaction == DEPOSIT:
            accounts[client][TOTAL] -= prior_amount
        elif referenced_transaction == WITHDRAWAL:
            accounts[client][TOTAL] += prior_amount
        accounts[client][HELD] -= prior_amount
        accounts[client][LOCKED] = True

    return accounts


def get_client_accounts(client_transactions):
    """Get client accounts summarized by client_transactions
    :param client_transactions: Dictionary containing list of client of transactions
    :return: Dict
    """
    accounts = {}
    transaction_id_list = []
    for client, transactions in client_transactions.items():
        for index, transaction in enumerate(transactions):
            transaction_id, transaction_type, amount = transaction

            if transaction_type == DEPOSIT and transaction_id not in transaction_id_list:
                accounts = deposit(accounts, amount, client)
                transaction_id_list.append(transaction_id)
            elif transaction_type == WITHDRAWAL and transaction_id not in transaction_id_list:
                accounts = withdrawal(accounts, amount, client)
                transaction_id_list.append(transaction_id)
            elif transaction_type == DISPUTE:
                prior_transaction = next((t for t in transactions[:index][::-1]
                                          if t[0] == transaction_id), None)
                if prior_transaction:
                    _, prior_transaction_type, prior_amount = prior_transaction

                    accounts = dispute(accounts, client, prior_amount, prior_transaction_type)

                    transactions[index][2] = prior_amount
                    transactions[index].append(prior_transaction_type)
            elif transaction_type in (RESOLVE, CHARGEBACK):
                prior_transaction = next((t for t in transactions[:index][::-1]
                                          if t[0] == transaction_id), None)

                if prior_transaction:
                    if transaction_type == RESOLVE:
                        accounts = resolve(accounts, client, prior_transaction)
                    elif transaction_type == CHARGEBACK:
                        accounts = chargeback(accounts, client, prior_transaction)
    return accounts


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Payments engine that reads a series of transactions from a CSV file, "
                    "handles disputes and chargebacks, and then outputs the state"
                    " of clients accounts.")
    parser.add_argument("input_file")
    args = parser.parse_args()

    client_transactions = get_client_transactions_from_csv_file(args.input_file)
    accounts = get_client_accounts(client_transactions)

    if accounts:
        print('client,available,held,total,locked')
        for client, account in accounts.items():
            print(f"{client},{account[AVAILABLE]},{account[HELD]},"
                  f"{account[TOTAL]},{account[LOCKED]}")


if __name__ == '__main__':
    main()
