import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. ULTRA-CUTE CUSTOM CHIBI CARTOON CHARACTERS UI CONFIGURATION (CSS)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Chibi Trader Pro 🎀", page_icon="🦋", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght=500;700&display=swap');
    
    /* Soft pastel purple/lavender background */
    .stApp {
        font-family: 'Quicksand', sans-serif;
        background-color: #f3effa !important;
        color: #4a3e56;
        overflow-x: hidden;
    }
    
    /* --- FLOATING CHIBI BACKGROUND ANIMATION --- */
    .floating-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        inset: 0;
        z-index: 0;
        pointer-events: none; /* Allows clicking through elements to reach buttons */
        overflow: hidden;
    }

    .chibi-item {
        position: absolute;
        bottom: -100px;
        font-size: 55px; /* Larger size for impact */
        opacity: 0.35;
        animation: floatUp 16s linear infinite;
        filter: drop-shadow(0px 6px 8px rgba(123, 92, 150, 0.15));
    }

    /* Distributing different ultra-cute smiling elements with faces */
    .chibi-1 { left: 4%; animation-duration: 13s; animation-delay: 0s; }
    .chibi-2 { left: 14%; animation-duration: 17s; animation-delay: 2s; font-size: 60px; }
    .chibi-3 { left: 28%; animation-duration: 15s; animation-delay: 5s; }
    .chibi-4 { left: 42%; animation-duration: 14s; animation-delay: 1s; font-size: 65px; }
    .chibi-5 { left: 58%; animation-duration: 19s; animation-delay: 4s; }
    .chibi-6 { left: 72%; animation-duration: 12s; animation-delay: 0s; font-size: 58px; }
    .chibi-7 { left: 85%; animation-duration: 16s; animation-delay: 3s; }
    .chibi-8 { left: 93%; animation-duration: 18s; animation-delay: 6s; }

    @keyframes floatUp {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 0.45;
        }
        90% {
            opacity: 0.45;
        }
        100% {
            transform: translateY(-118vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    /* --- INTERFACE CONTAINERS (Z-INDEX FORCED TO BE ABOVE BACKDROP) --- */
    .block-container {
        position: relative;
        z-index: 10 !important;
    }

    .soft-title {
        font-size: 46px;
        font-weight: 700;
        color: #7b5c96;
        text-align: center;
        margin-bottom: 2px;
        text-shadow: 2px 2px 4px #e2daf0;
    }
    
    .soft-subtitle {
        text-align: center;
        color: #9c82b3;
        font-size: 17px;
        margin-bottom: 25px;
        font-weight: 500;
    }
    
    button[data-baseweb="tab"] {
        font-size: 17px !important;
        font-weight: bold !important;
        color: #9c82b3 !important;
        background-color: transparent !important;
        border-radius: 12px 12px 0px 0px;
        padding: 12px 24px !important;
        transition: all 0.3s ease;
    }
    
    button[aria-selected="true"] {
        background-color: #e6def2 !important;
        color: #63447c !important;
        border-bottom: 3px solid #ac92c7 !important;
    }
    
    .metric-card {
        padding: 24px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(123, 92, 150, 0.1);
        margin-bottom: 18px;
        border: 2px solid transparent;
        background-color: #ffffff;
    }
    
    .card-entry { background-color: #f0f4f8; border-color: #dbe5ee; } 
    .card-target { background-color: #edf7f2; border-color: #daebd1; }  
    .card-sl { background-color: #fbf0f2; border-color: #f3dadf; }   
    .card-rsi { background-color: #f4f0fa; border-color: #e6def3; }   
    
    .metric-label { font-size: 15px; font-weight: 700; color: #786b85; margin-bottom: 6px; }
    .metric-val { font-size: 28px; font-weight: 700; }

    .soft-signal {
        padding: 18px;
        border-radius: 18px;
        text-align: center;
        font-size: 17px;
        font-weight: bold;
        margin: 24px 0;
        background-color: #eadef7;
        border: 2px dashed #c0a9db;
        color: #583c70;
    }
    
    .horizon-box {
        background: #ffffff;
        padding: 24px;
        border-radius: 24px;
        border: 2px solid #eae2f5;
        box-shadow: 0 10px 30px rgba(123, 92, 150, 0.05);
        margin-bottom: 24px;
    }
    
    label, p, span, .stMarkdown { color: #4a3e56; }
    code { background-color: #eadef7 !important; color: #583c70 !important; font-weight: bold; padding: 2px 6px; border-radius: 6px; }
    
    .chat-container, .panel-container {
        background: #ffffff;
        border-radius: 24px;
        padding: 24px;
        border: 2px solid #eae2f5;
        margin-top: 18px;
    }
    
    .stButton>button {
        background: #9c82b3 !important;
        color: #ffffff !important;
        border-radius: 16px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 12px 28px !important;
        font-size: 16px !important;
        box-shadow: 0 5px 12px rgba(156, 130, 179, 0.25) !important;
    }
    </style>

    <div class="floating-background">
        <div class="chibi-item chibi-1">😊🐼</div>
        <div class="chibi-item chibi-2">Smiling Cloud 😊☁️</div>
        <div class="chibi-item chibi-3">Cute Fairy 😊🧚‍♀️</div>
        <div class="chibi-item chibi-4">Smiling Bear 😊🐻</div>
        <div class="chibi-item chibi-5">Cute Butterfly 😊🦋</div>
        <div class="chibi-item chibi-6">Cute Blossom 😊🌸</div>
        <div class="chibi-item chibi-7">Smiling Unicorn 😊🦄</div>
        <div class="chibi-item chibi-8">Smiling Cloud 😊☁️</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. CORE ENGINES & WATCHLIST INFRASTRUCTURE
# -----------------------------------------------------------------------------
MICRO_WATCHLIST = [
    "SUZLON.NS", "SJVN.NS", "NHPC.NS", "IRFC.NS", "GMRINFRA.NS", 
    "NBCC.NS", "IDFCFIRSTB.NS", "IFCI.NS", "ALOKINDS.NS", "INFIBEAM.NS"
]

def get_market_data(ticker_symbol, interval, period):
    try:
        stock = yf.Ticker(ticker_symbol)
        df = stock.history(period=period, interval=interval)
        return df if (df is not None and isinstance(df, pd.DataFrame) and not df.empty) else pd.DataFrame()
    except:
        return pd.DataFrame()

def calculate_advanced_indicators(df):
    if df.empty: return df
    df['SMA_Fast'] = df['Close'].rolling(window=20).mean()
    df['SMA_Slow'] = df['Close'].rolling(window=50).mean()
    
    high_low = df['High'] - df['Low']
    high_cp = (df['High'] - df['Close'].shift()).abs()
    low_cp = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1)
    df['ATR'] = tr.rolling(window=14).mean()
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain / loss)))
    return df

def run_exact_micro_analysis():
    matched_results = []
    for stock in MICRO_WATCHLIST:
        try:
            ticker_obj = yf.Ticker(stock)
            df_15m = ticker_obj.history(period="7d", interval="15m")
            df_daily = ticker_obj.history(period="22d", interval="1d")
            
            if df_15m is not None and not df_15m.empty and len(df_15m) >= 20 and df_daily is not None and not df_daily.empty:
                close_series = df_15m['Close']
                ema_20 = close_series.ewm(span=20, adjust=False).mean()
                
                delta = close_series.diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi_15m = 100 - (100 / (1 + (gain / loss)))
                
                last_close = close_series.iloc[-1]
                last_rsi = rsi_15m.iloc[-1]
                last_ema20 = ema_20.iloc[-1]
                
                live_cumulative_volume = df_daily['Volume'].iloc[-1]
                historical_volume_sma20 = df_daily['Volume'].rolling(window=20).mean().iloc[-2]
                
                price_condition = (last_close >= 10 and last_close <= 30)
                ema_condition = (last_close > last_ema20)
                rsi_condition = (last_rsi > 68)
                volume_condition = (live_cumulative_volume > historical_volume_sma20 * 3) and (live_cumulative_volume > 500000)
                
                if price_condition and ema_condition and rsi_condition and volume_condition:
                    matched_results.append({
                        "ticker": stock, 
                        "price": last_close, 
                        "rsi": last_rsi, 
                        "vol": live_cumulative_volume
                    })
        except:
            continue
    return matched_results

# -----------------------------------------------------------------------------
# 3. INTERFACE WORKSPACE LAYOUT
# -----------------------------------------------------------------------------
st.markdown('<div class="soft-title">Chibi Trader Pro 🎀☁️</div>', unsafe_allow_html=True)
st.markdown("<div class='soft-subtitle'>Max-Cute Blushing Characters & Magical Secret Garden Lounge</div>", unsafe_allow_html=True)

tab_chart, tab_micro, tab_ai, tab_academy = st.tabs([
    "Cloud with Face ☁️ Chart Reader", 
    "🔍 Micro Analysis", 
    "💬 Chibi AI Chat", 
    "📚 Academy Corner"
])

# -----------------------------------------------------------------------------
# TAB 1: ADVANCED CHART READER
# -----------------------------------------------------------------------------
with tab_chart:
    st.write("")
    col_input, _ = st.columns([1, 2])
    with col_input:
        ticker = st.text_input("Enter Ticker Code:", value="SUZLON.NS", key="adv_chart_ticker").strip().upper()
    
    if ticker:
        if "horizon_mode" not in st.session_state:
            st.session_state.horizon_mode = "Short Term"
            
        st.markdown('<div class="horizon-box">', unsafe_allow_html=True)
        st.markdown("<p style='font-size:16px; font-weight:bold; margin-bottom:12px; color:#7b5c96;'>Select Strategy Horizon:</p>", unsafe_allow_html=True)
        
        hb1, hb2, hb3 = st.columns(3)
        if hb1.button("Cute Butterfly 🦋 Intraday (15m)", use_container_width=True):
            st.session_state.horizon_mode = "Intraday"
        if hb2.button("Cute Blossom 🌸 Short Term (Daily)", use_container_width=True):
            st.session_state.horizon_mode = "Short Term"
        if hb3.button("Smiling Unicorn 🦄 Long Term (Weekly)", use_container_width=True):
            st.session_state.horizon_mode = "Long Term"
            
        st.write("---")
        
        if st.button("🔄 Reload Live Market Data", use_container_width=True):
            st.cache_data.clear()  
            st.rerun()            
            
        st.markdown(f"Current Data Profile: <b style='color:#7b5c96;'>{st.session_state.horizon_mode} Focus Mode</b>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.horizon_mode == "Intraday":
            interval, period = "15m", "5d"
        elif st.session_state.horizon_mode == "Short Term":
            interval, period = "1d", "3mo"
        else:
            interval, period = "1wk", "2y"
            
        with st.spinner('Loading cute data streams...'):
            data = get_market_data(ticker, interval=interval, period=period)
            if data.empty:
                st.error("⚠️ Data lookup failed. Please confirm the extension suffix code.")
            else:
                currency = "₹" if (ticker.endswith(".NS") or ticker.endswith(".BO")) else "$"
                data = calculate_advanced_indicators(data)
                
                entry_price = data['Close'].iloc[-1]
                latest_atr = data['ATR'].iloc[-1] if not pd.isna(data['ATR'].iloc[-1]) else (entry_price * 0.02)
                
                if st.session_state.horizon_mode == "Intraday":
                    target_price = entry_price + (latest_atr * 1.5)
                    stop_loss_price = entry_price - (latest_atr * 1.0)
                elif st.session_state.horizon_mode == "Short Term":
                    target_price = entry_price + (latest_atr * 2.5)
                    stop_loss_price = entry_price - (latest_atr * 1.5)
                else: 
                    target_price = entry_price * 1.30 
                    stop_loss_price = entry_price * 0.85
                
                rsi = data['RSI'].iloc[-1]
                
                last_row = data.iloc[-1]
                prev_row = data.iloc[-2]
                signal = "💖 NEUTRAL CONDITION TRACKING"
                if last_row['SMA_Fast'] > last_row['SMA_Slow'] and prev_row['SMA_Fast'] <= prev_row['SMA_Slow']:
                    signal = "Cute Butterfly 🦋 UPWARD TREND CROSSOVER INDICATED"
                elif rsi < 32:
                    signal = "Cute Blossom 🌸 ASSET IN OVERSOLD RANGE VALUE ACCUMULATION"
                elif rsi > 68:
                    signal = "Smiling Fairy 🧚‍♀️ ASSET IN HIGH MOMENTUM OVERBOUGHT OVEREXTENSION"

                c1, c2, c3, c4 = st.columns(4)
                c1.markdown(f'<div class="metric-card card-entry"><div class="metric-label" style="color:#4b7fa3;">Ribbon Face 🎀 Entry Point</div><div class="metric-val" style="color:#4b7fa3;">{currency}{entry_price:.2f}</div></div>', unsafe_allow_html=True)
                c2.markdown(f'<div class="metric-card card-target"><div class="metric-label" style="color:#43875a;">Smiling Fairy 🧚‍♀️ Target Objective</div><div class="metric-val" style="color:#43875a;">{currency}{target_price:.2f}</div></div>', unsafe_allow_html=True)
                c3.markdown(f'<div class="metric-card card-sl"><div class="metric-label" style="color:#a84e5b;">Blushing Heart 💗 Protective SL</div><div class="metric-val" style="color:#a84e5b;">{currency}{stop_loss_price:.2f}</div></div>', unsafe_allow_html=True)
                c4.markdown(f'<div class="metric-card card-rsi"><div class="metric-label" style="color:#7b5c96;">Cute Blossom 🌸 {st.session_state.horizon_mode} RSI</div><div class="metric-val" style="color:#7b5c96;">{rsi:.1f}</div></div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="soft-signal">{signal}</div>', unsafe_allow_html=True)
                
                fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Price', increasing_line_color='#6ba686', decreasing_line_color='#d48792')])
                fig.add_hline(y=entry_price, line_dash="dash", line_color="#4b7fa3", line_width=1.5, annotation_text="Ribbon Face 🎀 Entry Point", annotation_position="top left", annotation_font_color="#4b7fa3")
                fig.add_hline(y=target_price, line_dash="dash", line_color="#43875a", line_width=1.5, annotation_text="Smiling Fairy 🧚‍♀️
