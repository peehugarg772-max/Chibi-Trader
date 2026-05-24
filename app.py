import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. ULTRA-CUTE BLUSHING CHARACTERS & CLOUDS WITH FACES UI CONFIGURATION (CSS)
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
        font-size: 42px;
        opacity: 0.28;
        animation: floatUp 15s linear infinite;
        filter: drop-shadow(0px 4px 6px rgba(123, 92, 150, 0.1));
    }

    /* Distributing different cute smiling elements across coordinates with varying speeds */
    .chibi-1 { left: 4%; animation-duration: 13s; animation-delay: 0s; }
    .chibi-2 { left: 14%; animation-duration: 17s; animation-delay: 2s; font-size: 46px; }
    .chibi-3 { left: 28%; animation-duration: 15s; animation-delay: 5s; }
    .chibi-4 { left: 42%; animation-duration: 14s; animation-delay: 1s; font-size: 52px; }
    .chibi-5 { left: 58%; animation-duration: 19s; animation-delay: 4s; }
    .chibi-6 { left: 72%; animation-duration: 12s; animation-delay: 0s; font-size: 44px; }
    .chibi-7 { left: 85%; animation-duration: 16s; animation-delay: 3s; }
    .chibi-8 { left: 93%; animation-duration: 18s; animation-delay: 6s; }

    @keyframes floatUp {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 0.38;
        }
        90% {
            opacity: 0.38;
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
        font-size: 44px;
        font-weight: 700;
        color: #7b5c96;
        text-align: center;
        margin-bottom: 2px;
        text-shadow: 2px 2px 4px #e2daf0;
    }
    
    .soft-subtitle {
        text-align: center;
        color: #9c82b3;
        font-size: 16px;
        margin-bottom: 25px;
        font-weight: 500;
    }
    
    button[data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: bold !important;
        color: #9c82b3 !important;
        background-color: transparent !important;
        border-radius: 12px 12px 0px 0px;
        padding: 10px 20px !important;
        transition: all 0.3s ease;
    }
    
    button[aria-selected="true"] {
        background-color: #e6def2 !important;
        color: #63447c !important;
        border-bottom: 3px solid #ac92c7 !important;
    }
    
    .metric-card {
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(123, 92, 150, 0.08);
        margin-bottom: 15px;
        border: 2px solid transparent;
        background-color: #ffffff;
    }
    
    .card-entry { background-color: #f0f4f8; border-color: #dbe5ee; } 
    .card-target { background-color: #edf7f2; border-color: #daebd1; }  
    .card-sl { background-color: #fbf0f2; border-color: #f3dadf; }   
    .card-rsi { background-color: #f4f0fa; border-color: #e6def3; }   
    
    .metric-label { font-size: 14px; font-weight: 700; color: #786b85; margin-bottom: 5px; }
    .metric-val { font-size: 26px; font-weight: 700; }

    .soft-signal {
        padding: 16px;
        border-radius: 16px;
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        margin: 22px 0;
        background-color: #eadef7;
        border: 2px dashed #c0a9db;
        color: #583c70;
    }
    
    .horizon-box {
        background: #ffffff;
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #eae2f5;
        box-shadow: 0 8px 24px rgba(123, 92, 150, 0.04);
        margin-bottom: 20px;
    }
    
    label, p, span, .stMarkdown { color: #4a3e56; }
    code { background-color: #eadef7 !important; color: #583c70 !important; font-weight: bold; padding: 2px 6px; border-radius: 6px; }
    
    .chat-container, .panel-container {
        background: #ffffff;
        border-radius: 20px;
        padding: 20px;
        border: 2px solid #eae2f5;
        margin-top: 15px;
    }
    
    .stButton>button {
        background: #9c82b3 !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        border: none !important;
        font-weight: bold !important;
        box-shadow: 0 4px 10px rgba(156, 130, 179, 0.2) !important;
    }
    </style>

    <div class="floating-background">
        <div class="chibi-item chibi-1">🐼</div>
        <div class="chibi-item chibi-2">☁️</div>
        <div class="chibi-item chibi-3">🧚‍♀️</div>
        <div class="chibi-item chibi-4">🐻</div>
        <div class="chibi-item chibi-5">🦋</div>
        <div class="chibi-item chibi-6">🌸</div>
        <div class="chibi-item chibi-7">🦄</div>
        <div class="chibi-item chibi-8">☁️</div>
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
st.markdown("<div class='soft-subtitle'>Magical Fairy Garden & Cute Blushing Character Lounge</div>", unsafe_allow_html=True)

tab_chart, tab_micro, tab_ai, tab_academy = st.tabs([
    "☁️ Advanced Chart Reader", 
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
        st.markdown("<p style='font-size:15px; font-weight:bold; margin-bottom:10px; color:#7b5c96;'>Select Strategy Horizon:</p>", unsafe_allow_html=True)
        
        hb1, hb2, hb3 = st.columns(3)
        if hb1.button("🦋 Intraday (15m)", use_container_width=True):
            st.session_state.horizon_mode = "Intraday"
        if hb2.button("🌸 Short Term (Daily)", use_container_width=True):
            st.session_state.horizon_mode = "Short Term"
        if hb3.button("🦄 Long Term (Weekly)", use_container_width=True):
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
                    signal = "🦋 UPWARD TREND CROSSOVER INDICATED"
                elif rsi < 32:
                    signal = "🌸 ASSET IN OVERSOLD RANGE VALUE ACCUMULATION"
                elif rsi > 68:
                    signal = "🧚‍♀️ ASSET IN HIGH MOMENTUM OVERBOUGHT OVEREXTENSION"

                c1, c2, c3, c4 = st.columns(4)
                c1.markdown(f'<div class="metric-card card-entry"><div class="metric-label" style="color:#4b7fa3;">🎀 Entry Point</div><div class="metric-val" style="color:#4b7fa3;">{currency}{entry_price:.2f}</div></div>', unsafe_allow_html=True)
                c2.markdown(f'<div class="metric-card card-target"><div class="metric-label" style="color:#43875a;">🧚‍♀️ Target Objective</div><div class="metric-val" style="color:#43875a;">{currency}{target_price:.2f}</div></div>', unsafe_allow_html=True)
                c3.markdown(f'<div class="metric-card card-sl"><div class="metric-label" style="color:#a84e5b;">💗 Protective SL</div><div class="metric-val" style="color:#a84e5b;">{currency}{stop_loss_price:.2f}</div></div>', unsafe_allow_html=True)
                c4.markdown(f'<div class="metric-card card-rsi"><div class="metric-label" style="color:#7b5c96;">🌸 {st.session_state.horizon_mode} RSI</div><div class="metric-val" style="color:#7b5c96;">{rsi:.1f}</div></div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="soft-signal">{signal}</div>', unsafe_allow_html=True)
                
                fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Price', increasing_line_color='#6ba686', decreasing_line_color='#d48792')])
                fig.add_hline(y=entry_price, line_dash="dash", line_color="#4b7fa3", line_width=1.5, annotation_text="🎀 Entry Point", annotation_position="top left", annotation_font_color="#4b7fa3")
                fig.add_hline(y=target_price, line_dash="dash", line_color="#43875a", line_width=1.5, annotation_text="🧚‍♀️ Target Level", annotation_position="top left", annotation_font_color="#43875a")
                fig.add_hline(y=stop_loss_price, line_dash="dash", line_color="#a84e5b", line_width=1.5, annotation_text="💗 Protection SL", annotation_position="top left", annotation_font_color="#a84e5b")
                
                fig.update_layout(template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#ffffff', xaxis_rangeslider_visible=False, height=450, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: MICRO ANALYSIS SCANNER
# -----------------------------------------------------------------------------
with tab_micro:
    st.markdown("<h4 style='color:#7b5c96;'>🌸 Fairy Garden Micro Matrix Scanner</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div class="panel-container">
        <strong style="color:#7b5c96;">🌸 ALIGNED CRITERIA SCHEMA:</strong><br>
        • Price Range: <code>₹10 to ₹30</code> | • Trend Parameter: <code>15m Close > 20 EMA</code><br>
        • Signal Strength: <code>15m RSI > 68</code> | • Daily Cumulative Volume: <code>Today's Vol > 3x (20-Day SMA Vol) & Total > 500k</code>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    
    if st.button("🚀 Execute Micro Matrix Sweep", key="btn_run_micro"):
        with st.spinner("Syncing data engines with fairytale conditions..."):
            hits = run_exact_micro_analysis()
            if hits:
                st.success(f"Success! Found {len(hits)} alerts matching the algorithm criteria.")
                for h in hits:
                    st.markdown(f"""
                    <div class="metric-card card-target" style="text-align: left; padding: 15px;">
                        <span style="font-size:18px; font-weight:bold; color:#7b5c96;">🦋 {h['ticker']}</span><br>
                        • <b>Price Level:</b> ₹{h['price']:.2f} | • <b>15m RSI:</b> {h['rsi']:.1f} | • <b>Day Volume:</b> {h['vol']:,} shares
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No stocks currently matching your precise criteria scan. (If checked pre-market, no items carried over the filters from yesterday's close).")

# -----------------------------------------------------------------------------
# TAB 3: PASTEL AI ASSISTANT HUD
# -----------------------------------------------------------------------------
with tab_ai:
    st.markdown("<h4 style='color:#7b5c96;'>💬 Technical System Advisor</h4>", unsafe_allow_html=True)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": "Interface set to cozy pastel view. Ask me any parameter questions safely."}]
        
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
            
    if chat_input := st.chat_input("Type a message..."):
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        with st.chat_message("user"): st.markdown(chat_input)
        
        q = chat_input.lower()
        if "stop loss" in q or "sl" in q:
            reply = "The **Stop Loss (💗)** marks structural levels below localized candle bodies to safeguard capital systematically."
        elif "target" in q:
            reply = "The **Target Line (🧚‍♀️)** identifies extension levels calculated by volatility ratios to optimize profit positions."
        else:
            reply = "You can view dynamic horizon targets anytime by looking directly inside the main Advanced Chart Reader Tab."
            
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"): st.markdown(reply)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 4: RISK MANAGEMENT
# -----------------------------------------------------------------------------
with tab_academy:
    st.markdown("<h4 style='color:#7b5c96;'>📚 Strategic Management Index</h4>", unsafe_allow_html=True)
    with st.expander("📊 Exposure Allocations"):
        st.markdown("Sound configurations align setups where the profit distance to **Target (🧚‍♀️)** safely compensates potential exposure down toward the **Stop Loss (💗)** line.")
