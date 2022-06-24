Implementation:

1. Deposit ETH into AAVE
2. Borrow some asset with ETH Collateral
   1. Sell that borrowed asset. Short Selling.
3. Repay everything back

Testing:

1. Integration test: Kovan
2. Unit test: mainnet-fork

NOTE: if you are not working with oracles and you don't need to mock responses then you can use mainnet-fork for unit testing
