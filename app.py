import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. MINDFUL & SOFT LOW-CONTRAST UI CONFIGURATION (CSS)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Chibi Trader Pro 📈", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&display=swap');
    
    /* Soft, warm dark gray background to prevent light glare */
    .stApp {
        font-family: 'Quicksand', sans-serif;
        background-color: #1e222b !important;
        color: #cfd6df;
    }
    
    /* Gentle, non-glowing title heading */
    .soft-title {
        font-size: 36px;
        font-weight: 700;
        color: #a3b8cc;
        text-align: center;
        margin-bottom: 5px;
    }
    
    .soft-subtitle {
        text-align: center;
        color: #8a99ad;
        font-size: 15px;
        margin-bottom: 20px;
    }
    
    /* Muted tabs without sudden bright highlights */
    button[data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: bold !important;
        color: #788796 !important;
        background-color: transparent !important;
        border-radius: 6px 6px 0px 0px;
        padding: 10px 20px !important;
    }
    
    button[aria-selected="true"] {
        background-color: #252a36 !important;
        color: #a3b8cc !important;
        border-bottom: 2px solid #5c7080 !important;
    }
    
    /* Low-contrast, gentle metric cards */
    .metric-card {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin-bottom: 15px;
    }
    .card-entry { background-color: #212936; border: 1px solid #364359; } 
    .card-target { background-color: #1f2b25; border: 1px solid #30473b; }  
    .card-sl { background-color: #2b2022; border: 1px solid #4a3437; }   
    .card-rsi { background-color: #222731; border: 1px solid #383f4f; }   
    
    .metric-label { font-size: 14px; font-weight: 700; color: #8a99ad; margin-bottom: 5px; letter-spacing: 0.5px; }
    .metric-val { font-size: 24px; font-weight: 700; }

    /* Subtle, flat status banners */
    .soft-signal {
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        margin: 20px 0;
        background-color: #252a36;
        border: 1px solid #313745;
        color: #cbd5e1;
    }
    
    /* Flat control panel container */
    .horizon-box {
        background: #252a36;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #313745;
        margin-bottom: 20px;
    }
    
    /* Ensuring all baseline text stays in relaxed neutral tones */
    label, p, span, .stMarkdown { color: #cfd6df; }
    code { background-color: #252a36 !important; color: #a3b8cc !important; }
    
    .chat-container, .panel-container {
        background: #252a36;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #313745;
        margin-top: 15px;
    }
    
    /* Soft button styling with no aggressive hover pops */
    .stButton>button {
        background: #2c3240 !important;
        color: #cfd6df !important;
        border-radius: 6px !important;
        border: 1px solid #3d4659 !important;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background: #343b4d !important;
        border-color: #5c7080 !important;
        color: #ffffff !important;
    }
    </style>
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
            df_15m = ticker_obj.history(period="5d", interval="15m")
            if df_15m is not None and not df_15m.empty and len(df_15m) >= 20:
                close_series = df_15m['Close']
                volume_series = df_15m['Volume']
                ema_20 = close_series.ewm(span=20, adjust=False).mean()
                sma_vol_20 = volume_series.rolling(window=20).mean()
                
                delta = close_series.diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi_15m = 100 - (100 / (1 + (gain / loss)))
                
                last_close = close_series.iloc[-1]
                last_rsi = rsi_15m.iloc[-1]
                last_vol = volume_series.iloc[-1]
                last_ema20 = ema_20.iloc[-1]
                last_smavol20 = sma_vol_20.iloc[-1]
                
                if (last_close >= 10 and last_close <= 30) and (last_close > last_ema20) and (last_rsi > 68) and (last_vol > last_smavol20 * 3) and (last_vol > 500000):
                    matched_results.append({"ticker": stock, "price": last_close, "rsi": last_rsi, "vol": last_vol})
        except:
            continue
    return matched_results

# -----------------------------------------------------------------------------
# 3. INTERFACE WORKSPACE LAYOUT
# -----------------------------------------------------------------------------
st.markdown('<div class="soft-title">Chibi Trader Pro</div>', unsafe_allow_html=True)
st.markdown("<div class='soft-subtitle'>Comfort View Technical Workstation</div>", unsafe_allow_html=True)

tab_chart, tab_micro, tab_ai, tab_academy = st.tabs([
    "📊 Advanced Chart Reader", 
    "🔍 Micro Analysis", 
    "💬 Chibi AI Chat", 
    "📚 Academy Corner"
])

# -----------------------------------------------------------------------------
# TAB 1: ADVANCED CHART READER (COMFORT VISUALS)
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
        st.markdown("<p style='font-size:15px; font-weight:bold; margin-bottom:10px; color:#8a99ad;'>Select Strategy Horizon:</p>", unsafe_allow_html=True)
        
        hb1, hb2, hb3 = st.columns(3)
        if hb1.button("Intraday (15m Candles)", use_container_width=True):
            st.session_state.horizon_mode = "Intraday"
        if hb2.button("Short Term (Daily Candles)", use_container_width=True):
            st.session_state.horizon_mode = "Short Term"
        if hb3.button("Long Term (Weekly Candles)", use_container_width=True):
            st.session_state.horizon_mode = "Long Term"
            
        st.write("---")
        
        # 🔄 Reload Button
        if st.button("🔄 Reload Live Market Data", use_container_width=True):
            st.cache_data.clear()  
            st.rerun()            
            
        st.markdown(f"Current Data Profile: <b style='color:#a3b8cc;'>{st.session_state.horizon_mode} Focus</b>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.horizon_mode == "Intraday":
            interval, period = "15m", "5d"
        elif st.session_state.horizon_mode == "Short Term":
            interval, period = "1d", "3mo"
        else:
            interval, period = "1wk", "2y"
            
        with st.spinner('Loading data streams...'):
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
                signal = "NEUTRAL CONDITION TRACKING"
                if last_row['SMA_Fast'] > last_row['SMA_Slow'] and prev_row['SMA_Fast'] <= prev_row['SMA_Slow']:
                    signal = "UPWARD TREND CROSSOVER INDICATED"
                elif rsi < 32:
                    signal = "ASSET IN OVERSOLD RANGE VALUE ACCUMULATION"
                elif rsi > 68:
                    signal = "ASSET IN HIGH MOMENTUM OVERBOUGHT OVEREXTENSION"

                # Mindful Muted Color Grid Items
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown(f'<div class="metric-card card-entry"><div class="metric-label" style="color:#7ca6cc;">🔵 Entry Point</div><div class="metric-val" style="color:#7ca6cc;">{currency}{entry_price:.2f}</div></div>', unsafe_allow_html=True)
                c2.markdown(f'<div class="metric-card card-target"><div class="metric-label" style="color:#79a88e;">🟢 Target Objective</div><div class="metric-val" style="color:#79a88e;">{currency}{target_price:.2f}</div></div>', unsafe_allow_html=True)
                c3.markdown(f'<div class="metric-card card-sl"><div class="metric-label" style="color:#bd868a;">🔴 Protective SL</div><div class="metric-val" style="color:#bd868a;">{currency}{stop_loss_price:.2f}</div></div>', unsafe_allow_html=True)
                c4.markdown(f'<div class="metric-card card-rsi"><div class="metric-label" style="color:#a3b8cc;">{st.session_state.horizon_mode} RSI</div><div class="metric-val" style="color:#a3b8cc;">{rsi:.1f}</div></div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="soft-signal">📋 TECHNICAL SUMMARY VERDICT: {signal}</div>', unsafe_allow_html=True)
                
                # Matte, low-contrast canvas layout for the candlestick chart
                fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Price', increasing_line_color='#608078', decreasing_line_color='#946b70')])
                
                # Non-piercing, muted dash horizon metrics line overlays
                fig.add_hline(y=entry_price, line_dash="dash", line_color="#536e87", line_width=1.5, annotation_text="🔵 Entry Checkpoint", annotation_position="top left", annotation_font_color="#7ca6cc")
                fig.add_hline(y=target_price, line_dash="dash", line_color="#547361", line_width=1.5, annotation_text="🟢 Calculated Target", annotation_position="top left", annotation_font_color="#79a88e")
                fig.add_hline(y=stop_loss_price, line_dash="dash", line_color="#825c60", line_width=1.5, annotation_text="🔴 Protection Support", annotation_position="top left", annotation_font_color="#bd868a")
                
                fig.update_layout(template='plotly_dark', paper_bgcolor='#1e222b', plot_bgcolor='#1e222b', xaxis_rangeslider_visible=False, height=450, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: MICRO ANALYSIS SCANNER
# -----------------------------------------------------------------------------
with tab_micro:
    st.markdown("<h4 style='color:#a3b8cc;'>🔍 High-Volume Micro Matrix</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div class="panel-container">
        <strong style="color:#a3b8cc;">📋 MONITORING CONDITIONS SCHEMA:</strong><br>
        • Cap Bounds: <code>₹10 to ₹30</code> | • Parameter Check: <code>15m Candle > 20 EMA</code><br>
        • Strength Filter: <code>15m RSI > 68</code> | • Volume Scale: <code>Volume > 3x Vol SMA(20) & Pool Total > 500k</code>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    
    if st.button("🚀 Execute Micro Matrix Sweep", key="btn_run_micro"):
        with st.spinner("Analyzing watchlist..."):
            hits = run_exact_micro_analysis()
            if hits:
                st.success(f"Found {len(hits)} alerts fulfilling rule metrics.")
                for h in hits:
                    st.markdown(f"""
                    <div class="metric-card card-target" style="text-align: left; padding: 15px;">
                        <span style="font-size:18px; font-weight:bold; color:#a3b8cc;">📈 {h['ticker']}</span><br>
                        • <b>Live Check:</b> ₹{h['price']:.2f} | • <b>15m RSI:</b> {h['rsi']:.1f} | • <b>Volume:</b> {h['vol']:,} shares
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No tickers matching constraint variables currently.")

# -----------------------------------------------------------------------------
# TAB 3: MATTE AI ASSISTANT HUD
# -----------------------------------------------------------------------------
with tab_ai:
    st.markdown("<h4 style='color:#a3b8cc;'>💬 Technical System Advisor</h4>", unsafe_allow_html=True)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": "Interface set to neutral view. Ask me any parameter questions safely."}]
        
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
            
    if chat_input := st.chat_input("Type a message..."):
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        with st.chat_message("user"): st.markdown(chat_input)
        
        q = chat_input.lower()
        if "stop loss" in q or "sl" in q:
            reply = "The **Stop Loss (🔴)** marks structural levels below localized candle bodies to safeguard capital systematically."
        elif "target" in q:
            reply = "The **Target Line (🟢)** identifies extension levels calculated by volatility ratios to optimize profit positions."
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
    st.markdown("<h4 style='color:#a3b8cc;'>📚 Strategic Management Index</h4>", unsafe_allow_html=True)
    with st.expander("📊 Exposure Allocations"):
        st.markdown("Sound configurations align setups where the profit distance to **Target (🟢)** safely compensates potential exposure down toward the **Stop Loss (🔴)** line.")
