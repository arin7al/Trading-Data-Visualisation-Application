# Usage 

```python webtier.py host port datagen_host datagen_port```

# Endpoints

check connection
```host:port/connection```
returns {'connection': true or false}

authentication
```host:port/authentication?username=username&password=password```
returns {'success': true or false}

average sell/buy
```host:port/metrics/average/sell-buy?instrument=instrument_name```
returns {"sell": sell-num, "buy": buy-num}
