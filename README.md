# TRADING_VIEW-BROKER-RSI-CALCULATOR





# Relative Strength Index (RSI) Calculator - Pure Python (Wilder's RSI)

A complete implementation of the **Relative Strength Index (RSI)** using **J. Welles Wilder's original smoothing algorithm (RMA/Wilder Moving Average)** written entirely in **Pure Python**.

Unlike many implementations that rely on **TA-Lib**, **pandas-ta**, or other technical analysis libraries, this project performs **every mathematical calculation manually**.

The purpose of this repository is to demonstrate the complete internal working of the RSI indicator rather than simply calling an external library.

---

# Features

- Pure Python implementation
- No TA-Lib
- No pandas-ta
- No technical indicator libraries
- Implements Wilder's original RSI smoothing
- Easy to understand
- Beginner friendly
- Suitable for Algorithmic Trading projects
- Every calculation is performed manually

---

# Indicator Used

Relative Strength Index (RSI)

Developed by

> **J. Welles Wilder Jr.**

Book:

> *New Concepts in Technical Trading Systems (1978)*

---

# Mathematical Formula

The RSI is calculated as

```
RS = Average Gain / Average Loss

RSI = 100 - (100 / (1 + RS))
```

The important part is **how Average Gain and Average Loss are calculated.**

This implementation follows Wilder's original recursive smoothing.

---

# How This Implementation Works

The algorithm can be divided into multiple stages.

---

## Step 1 — Read Historical Candle Data

The program first loads historical OHLC candle data from JSON.

Each candle contains

```
OPEN
HIGH
LOW
CLOSE
DATE
TIME
```

Although the candle contains OHLC values, **only the Closing Price is required for RSI calculation.**

Example

```
100
101
103
102
104
106
...
```

---

## Step 2 — Extract Closing Prices

The program creates a list containing every closing price.

Example

```
[100,101,103,102,104,106...]
```

This becomes the input for the RSI calculation.

---

## Step 3 — Calculate Consecutive Price Changes

Each closing price is compared with its previous closing price.

Example

```
100 → 101 = +1

101 → 103 = +2

103 → 102 = -1

102 → 104 = +2
```

This produces

```
+1
+2
-1
+2
...
```

These values are called **Price Differences**.

---

## Step 4 — Separate Gains and Losses

Every difference is separated into two different lists.

Positive differences become **Gains**

Negative differences become **Losses**

Example

Price Difference

```
+2
-1
+3
-4
```

Gain List

```
2
0
3
0
```

Loss List

```
0
1
0
4
```

Notice that a single candle can only contribute to either Gain or Loss.

---

## Step 5 — Calculate the First Average Gain & Average Loss

The first RSI uses the first **14 price differences**.

Average Gain

```
Average Gain = Sum(Gains) / 14
```

Average Loss

```
Average Loss = Sum(Losses) / 14
```

These become the starting point of Wilder's smoothing.

---

## Step 6 — Calculate the First RSI

After obtaining Average Gain and Average Loss,

```
RS = Average Gain / Average Loss
```

Then

```
RSI = 100 - (100 / (1 + RS))
```

This becomes the first valid RSI value.

---

## Step 7 — Wilder Recursive Smoothing

This is the most important part of the implementation.

Instead of recalculating everything from scratch every candle,

Wilder updates the averages recursively.

### If Current Difference is Positive

```
Average Gain

=
((Previous Average Gain × 13) + Current Gain)
/14

Average Loss

=
((Previous Average Loss × 13) + 0)
/14
```

---

### If Current Difference is Negative

```
Average Gain

=
((Previous Average Gain × 13) + 0)
/14

Average Loss

=
((Previous Average Loss × 13) + Current Loss)
/14
```

After updating

```
RS

=

Average Gain / Average Loss
```

Finally

```
RSI

=

100 - (100 / (1 + RS))
```

The process repeats for every candle until the latest candle.

---

# Why Wilder's Smoothing Matters

A common misconception is that RSI is simply a rolling average.

It is **not**.

The Average Gain and Average Loss are recursive.

Every newly calculated value depends on

- Previous Average Gain
- Previous Average Loss

which themselves depend on

- Earlier averages

which again depend on

- Even older averages.

Because of this recursive dependency,

**all historical candles influence the current RSI value.**

---

# Historical Warm-Up

One important observation while implementing RSI manually is that the indicator requires sufficient historical data before stabilizing.

If only a small number of candles are provided,

the recursive averages are still adjusting.

As more historical candles become available,

the recursive averages stabilize and the RSI converges.

This behavior is commonly referred to as the **Warm-Up Period**.

---

# Why Your RSI May Differ From Trading Platforms

Sometimes traders notice that manually calculated RSI values do not exactly match TradingView or other charting platforms.

This usually **does not mean the RSI formula is incorrect.**

Small differences commonly arise due to

- Different historical warm-up lengths
- Different exchange data
- Different broker data feeds
- Session handling
- Missing historical candles
- Corrected exchange candles
- Vendor-specific OHLC data

When identical historical OHLC data is supplied and sufficient warm-up history is available, implementations following Wilder's algorithm converge very closely.

---

# Data Feed Notes

This implementation calculates RSI directly from the supplied candle data.

Therefore,

the quality and accuracy of the RSI depend entirely on the quality of the input OHLC data.

Different brokers may provide slightly different candle data because of

- Exchange feeds
- Tick aggregation
- Session timing
- Data corrections

Consequently, the RSI generated by this implementation is expected to closely follow the RSI generated from the same broker's historical candle data.

---

# Time Complexity

```
O(n)
```

The dataset is traversed only once after initialization.

---

# Space Complexity

```
O(n)
```

The implementation stores

- Closing Prices
- Gain List
- Loss List
- RSI Values

---

# Project Structure

```
Historical OHLC Data
        │
        ▼
Extract Closing Prices
        │
        ▼
Price Differences
        │
        ▼
Separate Gains & Losses
        │
        ▼
First 14 Average Gain/Loss
        │
        ▼
First RSI
        │
        ▼
Recursive Wilder Smoothing
        │
        ▼
Final RSI Values
```

---

# References

J. Welles Wilder Jr.

**New Concepts in Technical Trading Systems**

Published in 1978

---

# Author

Developed as part of my personal Algorithmic Trading research project.

The objective of this project is to understand and implement technical indicators from scratch instead of relying on external libraries.
