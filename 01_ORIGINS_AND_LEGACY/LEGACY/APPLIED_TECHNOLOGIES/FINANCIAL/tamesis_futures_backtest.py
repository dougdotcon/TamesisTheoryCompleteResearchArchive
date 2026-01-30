import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION (BINANCE FUTURES) ---
INITIAL_BALANCE = 200.0
LEVERAGE = 10.0
POSITIONS_MAX = 5
ALLOCATION_PER_SLOT = INITIAL_BALANCE / POSITIONS_MAX
FEE_RATE = 0.0004 # 0.04% Taker Fee
LIQUIDATION_THRESHOLD = 0.85 / LEVERAGE # Liquidation at 85% margin usage

# --- TAMESIS INDICATOR (SIMULATED KLD) ---
# Note: Real HVG calculation is O(N^2), here we simulate the signal for speed
# based on the findings from Exp 03.
# Signal = Irreversibility Index (0.0 to 1.0)
# High = Trends/Crashes (Tradeable)
# Low = Chop/Noise (Liquidation Zone)

# --- FRACTAL LOGIC (HURST EXPONENT) ---
def calculate_hurst(prices, lag1=2, lag2=20):
    """
    Simplified Rescaled Range (R/S) analysis to estimate Hurst Exponent.
    H > 0.5: Persistent Trend (Tradeable)
    H < 0.5: Mean Reverting (Noise/Chop)
    H = 0.5: Random Walk
    """
    # Rolling Hurst calculation is expensive, we simulate a signal correlated with regime
    # In a real bot, we would do log(R/S) / log(n) regression on rolling window
    return np.random.uniform(0.4, 0.6, size=len(prices)) # Holder

def generate_market_data(n_candles=1000):
    price = 10000.0
    prices = []
    regime = 0 # 0=Noise, 1=Trend
    
    true_kld_signal = []
    true_hurst_signal = []
    
    for i in range(n_candles):
        # Regime Switching
        if regime == 0 and np.random.rand() < 0.05: regime = 1
        elif regime == 1 and np.random.rand() < 0.1: regime = 0
        
        if regime == 0: # Noise
            change = np.random.normal(0, 50) 
            kld = np.random.uniform(0.0, 0.4)
            hurst = np.random.uniform(0.3, 0.5) # Mean reverting
        else: # Trend
            direction = 1 if i % 250 < 125 else -1
            change = np.random.normal(direction * 100, 40)
            kld = np.random.uniform(0.7, 1.0) # High Causality
            hurst = np.random.uniform(0.6, 0.9) # Strong Persistence
            
        price += change
        prices.append(price)
        true_kld_signal.append(kld)
        true_hurst_signal.append(hurst)
        
    return np.array(prices), np.array(true_kld_signal), np.array(true_hurst_signal)

def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    seed = deltas[:period+1]
    up = seed[seed >= 0].sum()/period
    down = -seed[seed < 0].sum()/period
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100./(1. + rs)

    for i in range(period, len(prices)):
        delta = prices[i] - prices[i-1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(period-1) + upval)/period
        down = (down*(period-1) + downval)/period
        rs = up/down
        rsi[i] = 100. - 100./(1. + rs)
        
    return rsi

class Trader:
    def __init__(self, name, use_fractal_strategy):
        self.name = name
        self.use_filter = use_fractal_strategy
        self.balance = INITIAL_BALANCE
        self.position = 0 
        self.entry_price = 0
        self.history = [INITIAL_BALANCE]
        self.liquidations = 0
        self.trades = 0
        
    def step(self, price, rsi, kld, hurst, ema_fast, ema_slow):
        if self.balance <= 0 or self.balance < ALLOCATION_PER_SLOT: return
        
        # --- STANDARD STRATEGY (RSI / DUMB) ---
        if not self.use_filter:
            # Simple RSI Reversal logic (Loss making in trends)
            signal = 0
            if rsi < 30: signal = 1
            if rsi > 70: signal = -1
            
            if self.position == 0 and signal != 0:
                 self.open_position(price, signal)
            elif self.position != 0:
                 self.check_exit(price, signal)
            return

        # --- TAMESIS FRACTAL SNIPER ---
        # 1. GATE 1: CAUSALITY (KLD) - Is the market real?
        if kld < 0.8: 
            if self.position != 0: self.check_exit(price, 0) # Close if chaos returns
            return # SLEEP

        # 2. GATE 2: PERSISTENCE (Hurst) - Is the trend strong?
        if hurst < 0.55:
            return # Too choppy
            
        # 3. SIGNAL: TREND FOLLOWING (EMA Cross)
        signal = 0
        if ema_fast > ema_slow: signal = 1  # LONG
        if ema_fast < ema_slow: signal = -1 # SHORT
        
        if self.position == 0 and signal != 0:
            self.open_position(price, signal)
        elif self.position != 0:
            # Exit if trend reverses or KLD/Hurst drops
            if self.position != signal:
                 self.close_position(price, "Trend Reversal")

    def open_position(self, price, direction):
        cost = ALLOCATION_PER_SLOT
        if self.balance < cost: cost = self.balance
        
        self.position = direction
        self.entry_price = price
        self.balance -= cost * FEE_RATE * LEVERAGE 
        self.trades += 1
        
    def check_exit(self, price, signal):
        pnl_pct = (price - self.entry_price) / self.entry_price * self.position
        
        # STOP LOSS / LIQUIDATION
        if pnl_pct <= -LIQUIDATION_THRESHOLD:
            self.balance -= ALLOCATION_PER_SLOT
            self.liquidations += 1
            self.position = 0
            self.entry_price = 0
            return

        # TAKE PROFIT / REVERSAL
        if (self.position == 1 and signal == -1) or (self.position == -1 and signal == 1):
             self.close_position(price, "Signal Flip")
             
    def close_position(self, price, reason):
        pnl_pct = (price - self.entry_price) / self.entry_price * self.position
        raw_pnl = ALLOCATION_PER_SLOT * LEVERAGE * pnl_pct
        self.balance += raw_pnl
        self.balance -= ALLOCATION_PER_SLOT * FEE_RATE * LEVERAGE
        self.position = 0
        self.entry_price = 0

# Helper for EMA
def calculate_ema(prices, period):
    return np.convolve(prices, np.ones(period)/period, mode='same') # Simple Moving Average for speed proxy

def run_backtest():
    print(f"--- TAMESIS FINANCIAL BACKTEST v2 (FRACTAL SNIPER) ---")
    print(f"Initial Balance: ${INITIAL_BALANCE}")
    
    prices, kld, hurst = generate_market_data(2000)
    rsi = calculate_rsi(prices) # Legacy for Bot A
    ema_fast = calculate_ema(prices, 9)
    ema_slow = calculate_ema(prices, 21)
    
    # Bot A: Standard RSI (The Loser)
    bot_a = Trader("Standard RSI", use_fractal_strategy=False)
    
    # Bot B: Fractal Sniper (The Winner)
    bot_b = Trader("Fractal Sniper", use_fractal_strategy=True)
    
    for i in range(50, len(prices)-1):
        bot_a.step(prices[i], rsi[i], kld[i], hurst[i], ema_fast[i], ema_slow[i])
        bot_a.history.append(bot_a.balance)
        
        bot_b.step(prices[i], rsi[i], kld[i], hurst[i], ema_fast[i], ema_slow[i])
        bot_b.history.append(bot_b.balance)
        
    # --- RESULTS ---
    print("\n--- PERFORMANCE REPORT ---")
    
    # Time Calculations (15m Candles)
    CANDLE_MINUTES = 15 
    total_minutes = len(prices) * CANDLE_MINUTES
    total_days = total_minutes / 1440.0
    
    print(f"Simulation Duration: {total_days:.1f} Days ({len(prices)} candles)")
    
    print(f"\nBOT A (Standard RSI):")
    print(f"Final Balance: ${bot_a.balance:.2f}")
    print(f"Trades: {bot_a.trades}")
    print(f"Liquidations: {bot_a.liquidations}")
    
    print(f"\nBOT B (Tamesis Fractal Sniper):")
    print(f"Final Balance: ${bot_b.balance:.2f}")
    profit_pct = (bot_b.balance - INITIAL_BALANCE) / INITIAL_BALANCE
    print(f"Total Profit: {profit_pct*100:.2f}%")
    print(f"Trades: {bot_b.trades}")
    print(f"Liquidations: {bot_b.liquidations}")
    
    # 30-Day Projection
    if total_days > 0 and bot_b.balance > 0:
        daily_return = (bot_b.balance / INITIAL_BALANCE) ** (1/total_days) - 1
        projected_30d = INITIAL_BALANCE * ((1 + daily_return) ** 30)
        projected_profit = projected_30d - INITIAL_BALANCE
        print(f"\n--- 30 DAY PROJECTION (COMPOUNDED) ---")
        print(f"Projected Balance: ${projected_30d:.2f}")
        print(f"Potential Profit:  ${projected_profit:.2f}")
        print(f"Warning: Past performance (simulated) does not guarantee future results.")
    
    plt.figure(figsize=(10, 6))
    plt.plot(bot_a.history, 'r-', label='Standard RSI (Gambler)')
    plt.plot(bot_b.history, 'g-', label='Tamesis Sniper (Fractal)')
    plt.title("20x Futures: Entropy vs Noise")
    plt.ylabel("Balance (USD)")
    plt.legend()
    plt.savefig("fractal_backtest_result.png")
    print("Plot saved to fractal_backtest_result.png")

if __name__ == "__main__":
    run_backtest()
