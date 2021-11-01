# Summary
This is a coding challenge for an interview

# Prompt
Given a list of withdrawals and desposits, detect the likely transfers amongst them.

A few notes:
- The same withdrawal or deposit cannot be used for multiple different transfers. If there's a case where a given withdrawal or deposit can be matched with multiple possible transfers, use the first occurrence in the list.
- A transfer can only be made between different wallets.

For example, given:
```
[
	('tx_id_1', 'wallet_id_1', '2020-01-01 15:30:20 UTC', 'out', 5.3),  # 5.3 BTC was withdrawn out of 'wallet_id_1'
	('tx_id_2', 'wallet_id_1', '2020-01-03 12:05:25 UTC', 'out', 3.2),  # 3.2 BTC was withdrawn out of 'wallet_id_1'
	('tx_id_3', 'wallet_id_2', '2020-01-01 15:30:20 UTC', 'in', 5.3),   # 5.3 BTC was deposited into 'wallet_id_2'
	('tx_id_4', 'wallet_id_3', '2020-01-01 15:30:20 UTC', 'in', 5.3),   # 5.3 BTC was deposited into 'wallet_id_3'
]
```
Expected output:
```
[
	('tx_id_1', 'tx_id_3'),
]
```
# Questions
#### 1. What's the time and space complexity of your algorithm?
Time complexity is O(n<sup>2</sup>) where n is the number of transactions in the rare occurence where all the transactions have the same timestamp AND amount.
More likely is the average case with time complexity of O(n) + O(m<sup>2</sup>) where m is the number of transactions with the exact same timestamp AND amount.

Space complexity is O(n).

#### 2. Imagine that for a given transfer, the outgoing timestamp may be similar but not exactly equal to the incoming timestamp. For example, a withdrawal from BitcoinExchanger is made at T1, but it takes a few minutes for the transaction to get enough confirmations on the blockchain, at T2. We'd like to evolve our algorithm for 'timestamp similarity' instead of 'timestamp equivalence'. How would you solve this?
I will query a sufficient sample of transactions to get the range of time (let's say X minutes) it takes to confirm a transaction. Then instead of matching the exact timestamp and amount, I will find 2 transaction within with the same amount occuring within X minutes of each other.
