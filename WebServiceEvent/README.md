# Usage 

```python webtier.py host port datagen_host datagen_port```

# Endpoints

check connection
```host:port/connection```

authentication
```host:port/authentication?username=username&password=password```

average sell/buy
```host:port/metrics/average/sell-buy```
returns {"sell": sell-num, "buy": buy-num}