import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# 1. AESTHETIC & CUTE UI CONFIGURATION (CSS)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Chibi Trader 📈", page_icon="🍡", layout="wide")

# Custom CSS for that "Cute, Colorful, Aesthetic" look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Quicksand', sans-serif;
        background-color: #FDF6F6; /* Soft Pink Background */
        color: #5D5D5D;
    }
    
    /* Cute Buttons */
    .stButton>button {
        background-color: #FFD1DC; /* Pastel Pink */
        color: #5D5D5D;
        border-radius: 20px;
        border: 2px solid #FFB7B2;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FFB7B2;
        color: white;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #FFF0F5; /* Lavender Blush */
    }

    /* Titles */
    h1, h2, h3 {
        color: #8470FF; /* Soft Purple */
        text-align: center;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #00CED1; /* Dark Turquoise */
    }
    
    /* The Signal Box */
    .signal-box {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. LOGIC: ANALYSIS ENGINE
# -----------------------------------------------------------------------------
def get_data(ticker_symbol, period='1y'):
    try:
        stock = yf.Ticker(ticker_symbol)
        df = stock.history(period=period)
        return df
    except:
        return None

def calculate_indicators(df):
    # Simple Moving Averages
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    
    # RSI (Relative Strength Index)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df

def generate_signal(df):
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]
    
    current_price = last_row['Close']
    rsi = last_row['RSI']
    
    # Basic Logic for Demo
    signal = "HOLD 🍒"
    color = "#E6E6FA" # Lavender default
    
    # Trend Analysis (SMA Crossover)
    if last_row['SMA_20'] > last_row['SMA_50'] and prev_row['SMA_20'] <= prev_row['SMA_50']:
        signal = "STRONG BUY 🐻❗️ (Golden Cross)"
        color = "#98FB98" # Pastel Green
    elif last_row['SMA_20'] < last_row['SMA_50'] and prev_row['SMA_20'] >= prev_row['SMA_50']:
        signal = "SELL 🐻 (Death Cross)"
        color = "#FFB6C1" # Light Pink
    elif rsi > 70:
        signal = "OVERBOUGHT 😴 (Sell Time?)"
        color = "#FFD700" # Gold
    elif rsi < 30:
        signal = "OVERSOLD 🤑 (Buy Time?)"
        color = "#87CEFA" # Light Sky Blue
        
    # Target & Stop Loss (Simple 5% / 3% Rule)
    target = current_price * 1.05
    stop_loss = current_price * 0.97
    
    return signal, color, current_price, target, stop_loss, rsi, df

# -----------------------------------------------------------------------------
# 3. THE USER INTERFACE
# -----------------------------------------------------------------------------

st.title("🍡 Chibi Chart Reader")
st.markdown("### Your Cute guide to the Stock Market!")

# Sidebar - The "Teacher"
with st.sidebar:
    st.markdown("## 🏫 Chibi Academy")
    st.info("Enter a stock symbol (e.g., AAPL, TSLA, RELIANCE.NS) in the main box to start learning!")
    
    st.markdown("### 📚 Today's Lesson:")
    lesson = st.selectbox("Choose a topic:", 
        ["Moving Averages", "RSI (Momentum)", "Candlesticks", "Volume"])
    
    if lesson == "Moving Averages":
        st.markdown("""
        **SMA** is like the average grade of a student. 
        If the short-term average (20 days) crosses above the long-term average (50 days), 
        it might be a **Buy** signal! 📈
        """)
    elif lesson == "RSI":
        st.markdown("""
        **RSI** measures how fast the price is changing.
        Above 70? The stock is tired (Overbought) 😴.
        Below 30? It has energy remaining (Oversold) ⚡.
        """)
    elif lesson == "Candlesticks":
        st.markdown("""
        **Green Candle** = Price went UP 🟢
        **Red Candle** = Price went DOWN 🔴
        The 'body' shows the Open and Close prices.
        """)
    elif lesson == "Volume":
        st.markdown("""
        **Volume** is how many people are playing the game!
        High volume + Price Go Up = Strong party! 🎉
        """)

# Main Inputs
col1, col2 = st.columns([1, 2])
with col1:
    ticker = st.text_input("Enter Stock Ticker:", value="AAPL")
    analyze_btn = st.button("Analyze Chart! ✨")

if analyze_btn and ticker:
    with st.spinner('Crunching the numbers...'):
        data = get_data(ticker)
        
        if data.empty:
            st.error("Oops! Couldn't find that stock. Try a valid ticker like 'MSFT' or 'GOOG'.")
        else:
            data = calculate_indicators(data)
            signal, signal_color, curr_price, target, stop_loss, rsi, data = generate_signal(data)
            
            # Show Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Current Price", f"${curr_price:.2f}")
            m2.metric("Target (5%)", f"${target:.2f}", delta=f"+{(target-curr_price):.2f}")
            m3.metric("Stop Loss", f"${stop_loss:.2f}", delta=f"{(stop_loss-curr_price):.2f}")
            m4.metric("RSI Score", f"{rsi:.1f}")
            
            # Signal Display
            st.markdown(f"""
            <div class="signal-box" style="background-color: {signal_color};">
                RECOMMENDATION: {signal}
            </div>
            """, unsafe_allow_html=True)

            # CANDLESTICK CHART
            fig = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                increasing_line_color='#FF69B4', # Hot Pink for cute up
                decreasing_line_color='#20B2AA'  # Light Sea Green for down
            )])
            
            # Add Moving Averages to Chart
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], name='SMA 20', line=dict(color='#FFB6C1', width=1.5)))
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name='SMA 50', line=dict(color='#8470FF', width=2)))
            
            fig.update_layout(
                title=f"{ticker} - Cutie Pattern Analysis",
                yaxis_title='Price ($)',
                template='plotly_white',
                xaxis_rangeslider_visible=False,
                height=500,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Educational Context based on result
            st.markdown("### 🧐 Chibi Analysis:")
            if "BUY" in signal:
                st.markdown("The short average is acting **cute** and staying above the long average! The trend looks friendly.")
            elif "SELL" in signal:
                st.markdown("The trend is looking a bit **shy** and turning down. Be careful!")
            else:
                st.markdown("The market is chilling. It is waiting for a new direction.")
