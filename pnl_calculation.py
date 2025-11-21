from dataclasses import dataclass
from collections import deque, defaultdict
from typing import List, Literal, Dict

Side = Literal['BUY', 'SELL']

@dataclass
class Trade:
    symbol: str
    side: Side
    quantity: float
    price: float

def calculate_pnl_avg_cost(trades: List[Trade]) -> Dict[str, float]:

    positions: Dict[str, float] = {}
    realized_pnl: Dict[str, float] = {}
    avg_costs: Dict[str, float] = {}

    for t in trades:
        symbol = t.symbol
        side = t.side
        qty = t.quantity
        price = t.price

        pos = positions.get(symbol, 0.0)
        avg_cost = avg_costs.get(symbol, 0.0)
        pnl = realized_pnl.get(symbol, 0.0)

        if side == 'BUY':
            new_pos = pos + qty
            if new_pos != 0:
                avg_cost = (avg_cost * pos + price * qty) / new_pos

            positions[symbol] = new_pos
            avg_costs[symbol] = avg_cost

        elif side == 'SELL':
            new_pos = pos - qty
            if new_pos < 0:
                raise ValueError(f"Cannot sell more than current position for {symbol}")
            
            pnl += (price - avg_cost) * qty
            positions[symbol] = new_pos
            realized_pnl[symbol] = pnl

    return realized_pnl


def calculate_pnl_lifo(trades: List[Trade]) -> Dict[str, float]:

    lots: Dict[str, deque] = defaultdict(deque)
    pnl: Dict[str, float] = defaultdict(float)

    for trade in trades:
        symbol = trade.symbol
        side = trade.side
        qty = trade.quantity
        price = trade.price

        if side == 'BUY':
            lots[symbol].append((qty, price))

        elif side == 'SELL':
            remaining = qty
            while remaining > 0:
                if not lots[symbol]:
                    raise ValueError(f"Not enough inventory to sell for {symbol}")
                lot_qty, lot_price = lots[symbol][-1]
                matched_qty = min(remaining, lot_qty)
                pnl[symbol] += matched_qty * (price - lot_price)

                remaining -= matched_qty
                lot_qty -= matched_qty

                if lot_qty > 0:
                    lots[symbol][-1] = (lot_qty, lot_price)
                else:
                    lots[symbol].pop()

    return pnl


def calculate_pnl_fifo(trades: List[Trade]) -> Dict[str, float]:

    lots: Dict[str, deque] = defaultdict(deque)
    pnl: Dict[str, float] = defaultdict(float)

    for trade in trades:
        symbol = trade.symbol
        side = trade.side
        qty = trade.quantity
        price = trade.price

        if side == 'BUY':
            lots[symbol].append((qty, price))

        elif side == 'SELL':
            remaining = qty
            while remaining > 0:
                if not lots[symbol]:
                    raise ValueError(f"Not enough inventory to sell for {symbol}")
                lot_qty, lot_price = lots[symbol][0]
                matched_qty = min(remaining, lot_qty)
                pnl[symbol] += matched_qty * (price - lot_price)

                remaining -= matched_qty
                lot_qty -= matched_qty

                if lot_qty > 0:
                    lots[symbol][0] = (lot_qty, lot_price)
                else:
                    lots[symbol].popleft()

    return pnl


if __name__ == "__main__":
    
    trades = [
        Trade(symbol="AAPL", side="BUY", quantity=10, price=150),
        Trade(symbol="AAPL", side="BUY", quantity=5, price=155),
        Trade(symbol="AAPL", side="SELL", quantity=8, price=160),
        Trade(symbol="GOOGL", side="BUY", quantity=8, price=2000), 
        Trade(symbol="GOOGL", side="SELL", quantity=3, price=2100),
    ]

    pnl_avg = calculate_pnl_avg_cost(trades)
    pnl_lifo = calculate_pnl_lifo(trades)
    pnl_fifo = calculate_pnl_fifo(trades)
    print('P&L FIFO:', pnl_fifo)
    print('P&L LIFO:', pnl_lifo)
    print('P&L Avg Cost:', pnl_avg)