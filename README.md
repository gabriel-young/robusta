## Headline

This is a coding challenge to implement a payment engine script reading transactions from a CSV, updating client accounts, 
handle disputes and chargebacks, and finally produce standard output the state of clients accounts.

## CLI usage

```shell
usage: payment_engine.py [-h] input_file

Payments engine that reads a series of transactions from a CSV file, handles disputes
and chargebacks, and then outputs the state of clients accounts.

positional arguments:
  input_file

options:
  -h, --help  show this help message and exit
```

## Details

Given a CSV having a collection of transactions, the script will produce a summary of client accounts. Each client account will provide their overall balance as standard output.

The script will be executed like so:

```shell
python payment_engine.py sample.csv 
```

You may store the output to file like so:

```shell
python payment_engine.py sample.csv > output.csv
```