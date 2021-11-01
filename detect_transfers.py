from collections import defaultdict


def detect_transfers(transactions):
    """Detects transfers amongst the given transactions."""

    # Create a dictionary with timestamp as the key
    tx_dict = defaultdict(list)
    for transaction in transactions:
        tx_dict[transaction[2]].append(
            {
                "tx_id": transaction[0],
                "wallet_id": transaction[1],
                "tx_type": transaction[3],
                "amount": transaction[4],
            }
        )

    # Loop through the tx_dict, and find the timestamps with length > 1
    result = []
    for tx_list in tx_dict.values():
        if len(tx_list) > 1:

            # Create a smaller dict with amount as the key
            amt_dict = defaultdict(list)
            for tx in tx_list:
                amt_dict[tx["amount"]].append(
                    {
                        "tx_id": tx["tx_id"],
                        "wallet_id": tx["wallet_id"],
                        "tx_type": tx["tx_type"],
                    }
                )

            # All values in amt_dict now have matching timestamp and amount (aka. matched_tx)
            # Now, compare all pairs in matched_tx to make sure that one is 'in' and one is 'out', and that they are from different wallets
            for matched_tx in amt_dict.values():
                if len(matched_tx) > 1:
                    for i in range(len(matched_tx)):
                        for j in range(i + 1, len(matched_tx)):
                            if (
                                matched_tx[i]["tx_type"] != matched_tx[j]["tx_type"]
                            ) and (
                                matched_tx[i]["wallet_id"] != matched_tx[j]["wallet_id"]
                            ):
                                pair = (
                                    matched_tx[i]["tx_id"],
                                    matched_tx[j]["tx_id"],
                                )
                                result.append(pair)
                                break

    return result


"""
Add tests for `detect_transfers` below.
"""
# 1 matching transfer
test_case_1 = [
    ("tx_id_1", "wallet_id_1", "2020-01-01 15:30:20 UTC", "out", 5.3),
    ("tx_id_2", "wallet_id_1", "2020-01-03 12:05:25 UTC", "out", 3.2),
    ("tx_id_3", "wallet_id_2", "2020-01-01 15:30:20 UTC", "in", 5.3),
    ("tx_id_4", "wallet_id_3", "2020-01-01 15:30:20 UTC", "in", 5.3),
]

# multiple matching transfers
test_case_2 = [
    ("tx_id_1", "wallet_id_1", "2020-01-01 15:30:20 UTC", "out", 5.3),  # pair1
    ("tx_id_2", "wallet_id_1", "2020-01-03 12:05:25 UTC", "out", 3.2),
    ("tx_id_3", "wallet_id_2", "2020-01-01 15:30:20 UTC", "in", 5.3),  # pair1
    ("tx_id_4", "wallet_id_3", "2020-01-01 15:30:20 UTC", "in", 4.6),  # pair2
    ("tx_id_5", "wallet_id_7", "2020-01-01 15:30:20 UTC", "in", 5.3),
    ("tx_id_6", "wallet_id_5", "2020-01-02 20:30:35 UTC", "out", 2.1),  # pair3
    ("tx_id_7", "wallet_id_8", "2020-01-01 15:30:20 UTC", "in", 5.3),
    ("tx_id_8", "wallet_id_4", "2020-01-01 15:30:20 UTC", "out", 4.6),  # pair2
    ("tx_id_9", "wallet_id_6", "2020-01-02 20:30:35 UTC", "in", 2.1),  # pair3
]

# no matching transfers
test_case_3 = [
    ("tx_id_1", "wallet_id_1", "2020-01-01 15:30:20 UTC", "out", 5.3),
    ("tx_id_2", "wallet_id_1", "2020-01-03 12:05:25 UTC", "out", 3.2),
    ("tx_id_3", "wallet_id_2", "2020-01-01 15:30:20 UTC", "in", 6.7),
    ("tx_id_4", "wallet_id_3", "2020-01-01 15:30:20 UTC", "in", 4.6),
    ("tx_id_5", "wallet_id_7", "2020-01-02 20:30:20 UTC", "in", 5.3),
]
# empty list
test_case_4 = []

assert detect_transfers(test_case_1) == [("tx_id_1", "tx_id_3")]
assert detect_transfers(test_case_2) == [
    ("tx_id_1", "tx_id_3"),
    ("tx_id_4", "tx_id_8"),
    ("tx_id_6", "tx_id_9"),
]
assert detect_transfers(test_case_3) == []
assert detect_transfers(test_case_4) == []
