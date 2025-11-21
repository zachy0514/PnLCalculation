# P&L Calculation Methods

Compare three methods for calculating trading Profit & Loss: **Average Cost**, **FIFO**, and **LIFO**.

## Methods

- **Average Cost**: Uses weighted average of all purchases
- **FIFO** (First-In-First-Out): Sells oldest lots first
- **LIFO** (Last-In-First-Out): Sells newest lots first

## Usage

```powershell
python pnl_calculation.py
```

```python
from pnl_calculation import Trade, calculate_pnl_avg_cost, calculate_pnl_fifo, calculate_pnl_lifo

trades = [
    Trade(symbol="AAPL", side="BUY", quantity=10, price=150),
    Trade(symbol="AAPL", side="BUY", quantity=5, price=155),
    Trade(symbol="AAPL", side="SELL", quantity=8, price=160),
]

pnl_fifo = calculate_pnl_fifo(trades)    # {'AAPL': 115.0}
pnl_lifo = calculate_pnl_lifo(trades)    # {'AAPL': 55.0}
pnl_avg = calculate_pnl_avg_cost(trades) # {'AAPL': 66.67}
```

## Why Results Differ

| Method | Sells These Lots | P&L |
|--------|------------------|-----|
| FIFO | 10 @ $150, then 3 @ $155 | $115 |
| LIFO | 5 @ $155, then 3 @ $150 | $55 |
| Avg Cost | 8 @ $151.67 (average) | $66.67 |

Results only differ when selling from multiple lots at different prices.

## Requirements

Python 3.9+ • No external dependencies
