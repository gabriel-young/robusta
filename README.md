## Headline

This is a coding challenge to implement a payment engine script reading transactions from a CSV, updating client accounts, 
handle disputes and chargebacks, and finally produce standard output on state of clients accounts.

## CLI usage

```shell
usage: payment_engine.py [-h] input_file

Payments engine that reads a series of transactions from a CSV file, handles disputes
and chargebacks, and then output on state of clients accounts.

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

You may also store the output to file like so:

```shell
python payment_engine.py sample.csv > output.csv
```

## Testing

 * Below are sample csv files used as input against payment_engine.py, along with their associated output

 * deposit.csv
```shell
type, client, tx, amount
deposit, 1, 1, 45.939394
deposit, 1, 2, 45.939394
```

* output
```shell
client,available,held,total,locked
1,91.8788,0.0,91.8788,False
````

* deposit_dispute.csv
```shell
type, client, tx, amount
deposit, 1, 1, 12
deposit, 1, 2, 26
dispute, 1, 1
````
* output

```shell
client,available,held,total,locked
1,26.0,12.0,38.0,False
```

* deposit_dispute_chargeback.csv
```shell
type, client, tx, amount
deposit, 1, 1, 12.1234
deposit, 1, 2, 26.1234
dispute, 1, 2
chargeback, 1, 2
````
* output

```shell
client,available,held,total,locked
1,12.1234,0.0,12.1234,True
````

* deposit_dispute_resolved.csv
```shell
type, client, tx, amount
deposit, 1, 1, 12.1234
deposit, 1, 2, 26.1234
dispute, 1, 2
resolve, 1, 2
```

* output
```shell
client,available,held,total,locked
1,38.2468,0.0,38.2468,False
```

* duplicate_deposit.csv
```shell
type, client, tx, amount
deposit, 1, 1, 45.939394
deposit, 1, 1, 45.939394
```

* output

```shell
client,available,held,total,locked
1,45.9394,0.0,45.9394,False
```

* duplicate_withdrawal.csv
```shell
type, client, tx, amount
deposit, 1, 1, 26.83432
withdrawal, 1, 2, 12.84564
withdrawal, 1, 2, 12.84564
```
* output

```shell
client,available,held,total,locked
1,13.9887,0.0,13.9887,False
```

* end_to_end_test.csv
```shell
type, client, tx, amount
deposit, 1, 1, 8.1234
deposit, 2, 2, 8.1234
deposit, 1, 3, 20.1234
withdrawal, 1, 4, 2.1234
dispute, 1, 4,
deposit, 1, 5, 40.1234
resolve, 1, 4

deposit, 2, 6, 20.1234
withdrawal, 2, 7, 2.1234
dispute, 2, 7,
deposit, 2, 8, 30.1234
resolve, 2, 7
```
* output

```shell
client,available,held,total,locked
1,66.2468,0.0,66.2468,False
2,56.2468,0.0,56.2468,False
```

* withdrawal.csv
```shell
type, client, tx, amount
deposit, 1, 1, 26.83432
withdrawal, 1, 2, 12.84564
```

* output
```shell
client,available,held,total,locked
1,13.9887,0.0,13.9887,False
```

* withdrawal_dispute.csv
```shell
type, client, tx, amount
deposit, 1, 1, 12.28342
deposit, 1, 2, 84.28343
withdrawal, 1, 3, 10
dispute, 1, 3
```

* output

```shell
client,available,held,total,locked
1,96.5668,10.0,86.5668,False
```

* withdrawal_dispute_chargeback.csv
```shell
type, client, tx, amount
deposit, 1, 1, 12.89283
deposit, 1, 2, 12.89283
withdrawal, 1, 3, 10
dispute, 1, 3
chargeback, 1, 3
```

* output
```
client,available,held,total,locked
1,25.7856,0.0,25.7856,True
```

* withdrawal_dispute_resolved.csv
```shell
type, client, tx, amount
deposit, 1, 1, 12.4321
deposit, 1, 2, 12.4321
withdrawal, 1, 3, 12.4321
dispute, 1, 3
resolve, 1, 3
```
* output

```shell
client,available,held,total,locked
1,12.4321,0.0,12.4321,False
```
