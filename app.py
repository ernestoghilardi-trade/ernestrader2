"""
============================================================
BACKTEST PRO v4 — Versión Avanzada Completa
============================================================
- 150+ activos (USA, Europa, LATAM, Asia, Cripto, Forex)
- 6 estrategias diferentes
- Optimizador automático de parámetros
- Walk-Forward Analysis
- Monte Carlo Simulation
- Heatmap activo × estrategia
- Comparador 2 estrategias lado a lado
- Ranking filtrable
- Análisis por sector
============================================================
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
import itertools
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Backtest Pro v4', page_icon='🚀', layout='wide')

st.title('🚀 Backtest Pro v4')
st.markdown('**Análisis cuantitativo profesional — 150+ activos · 6 estrategias · Optimización · Walk-Forward · Monte Carlo**')
st.divider()

# ============================================================
# UNIVERSO DE ACTIVOS (150+)
# ============================================================
UNIVERSO = {
    '🇺🇸 USA Tech Mega': {
        'AAPL': 'AAPL', 'MSFT': 'MSFT', 'GOOGL': 'GOOGL', 'AMZN': 'AMZN',
        'META': 'META', 'NVDA': 'NVDA', 'TSLA': 'TSLA', 'NFLX': 'NFLX',
        'ADBE': 'ADBE', 'CRM': 'CRM', 'ORCL': 'ORCL', 'CSCO': 'CSCO',
    },
    '🇺🇸 USA Tech Volátiles': {
        'AMD': 'AMD', 'PLTR': 'PLTR', 'COIN': 'COIN', 'SHOP': 'SHOP',
        'NET': 'NET', 'SNOW': 'SNOW', 'CRWD': 'CRWD', 'RIVN': 'RIVN',
        'UBER': 'UBER', 'ABNB': 'ABNB', 'ROKU': 'ROKU', 'ZM': 'ZM',
    },
    '🇺🇸 USA Banca': {
        'JPM': 'JPM', 'BAC': 'BAC', 'WFC': 'WFC', 'GS': 'GS',
        'MS': 'MS', 'C': 'C', 'V': 'V', 'MA': 'MA', 'AXP': 'AXP',
    },
    '🇺🇸 USA Energía': {
        'XOM': 'XOM', 'CVX': 'CVX', 'COP': 'COP', 'SLB': 'SLB', 'OXY': 'OXY',
    },
    '🇺🇸 USA Salud': {
        'JNJ': 'JNJ', 'PFE': 'PFE', 'UNH': 'UNH', 'LLY': 'LLY',
        'ABBV': 'ABBV', 'MRK': 'MRK', 'IBRX': 'IBRX', 'MRNA': 'MRNA',
    },
    '🇺🇸 USA Consumo': {
        'KO': 'KO', 'PEP': 'PEP', 'WMT': 'WMT', 'MCD': 'MCD',
        'NKE': 'NKE', 'DIS': 'DIS', 'SBUX': 'SBUX', 'PG': 'PG',
    },
    '⚡ Nuclear/Renovables': {
        'SMR': 'SMR', 'OKLO': 'OKLO', 'NEE': 'NEE', 'ENPH': 'ENPH',
        'FSLR': 'FSLR', 'SEDG': 'SEDG',
    },
    '🇪🇺 Europa': {
        'ASML': 'ASML.AS', 'SAP': 'SAP.DE', 'LVMH': 'MC.PA',
        'TEF': 'TEF.MC', 'SAN': 'SAN.MC', 'BBVA': 'BBVA.MC',
        'IBE': 'IBE.MC', 'ITX': 'ITX.MC', 'REP': 'REP.MC',
        'AIR': 'AIR.PA', 'OR': 'OR.PA', 'SIE': 'SIE.DE',
        'VOW3': 'VOW3.DE', 'BMW': 'BMW.DE', 'BAS': 'BAS.DE',
    },
    '🌎 LATAM': {
        'PBR': 'PBR', 'VALE': 'VALE', 'ITUB': 'ITUB',
        'BBD': 'BBD', 'NU': 'NU', 'MELI': 'MELI', 'GLOB': 'GLOB',
        'AMX': 'AMX', 'GGAL': 'GGAL', 'YPF': 'YPF', 'TS': 'TS',
        'PAM': 'PAM', 'BMA': 'BMA', 'EDN': 'EDN', 'TGS': 'TGS',
    },
    '🌏 Asia': {
        'BABA': 'BABA', 'JD': 'JD', 'PDD': 'PDD',
        'BIDU': 'BIDU', 'TCEHY': 'TCEHY', 'NIO': 'NIO',
        'XPEV': 'XPEV', 'LI': 'LI', 'TSM': 'TSM', 'SONY': 'SONY',
        'TM': 'TM', 'HMC': 'HMC', 'NTES': 'NTES', 'BILI': 'BILI', 'LK': 'LK',
    },
    '📊 ETFs Índices USA': {
        'SPY': 'SPY', 'QQQ': 'QQQ', 'IWM': 'IWM', 'DIA': 'DIA', 'VTI': 'VTI',
    },
    '📊 ETFs Internacional': {
        'EFA': 'EFA', 'EEM': 'EEM', 'EWZ': 'EWZ', 'EWJ': 'EWJ',
        'FXI': 'FXI', 'INDA': 'INDA', 'EWG': 'EWG', 'EWU': 'EWU', 'EWP': 'EWP',
    },
    '📊 ETFs Sectoriales': {
        'XLK': 'XLK', 'XLF': 'XLF', 'XLE': 'XLE', 'XLV': 'XLV',
        'XLY': 'XLY', 'XLI': 'XLI', 'XLB': 'XLB', 'XLP': 'XLP',
        'XLU': 'XLU', 'XLRE': 'XLRE',
    },
    '📊 Commodities': {
        'GLD': 'GLD', 'SLV': 'SLV', 'USO': 'USO', 'UNG': 'UNG', 'DBA': 'DBA',
    },
    '₿ Cripto Top': {
        'BTC': 'BTC-USD', 'ETH': 'ETH-USD', 'BNB': 'BNB-USD',
        'SOL': 'SOL-USD', 'XRP': 'XRP-USD', 'ADA': 'ADA-USD',
        'DOGE': 'DOGE-USD', 'AVAX': 'AVAX-USD', 'DOT': 'DOT-USD',
        'MATIC': 'MATIC-USD', 'LINK': 'LINK-USD', 'LTC': 'LTC-USD',
        'BCH': 'BCH-USD', 'ATOM': 'ATOM-USD', 'XLM': 'XLM-USD',
        'ALGO': 'ALGO-USD', 'NEAR': 'NEAR-USD', 'FIL': 'FIL-USD',
        'SHIB': 'SHIB-USD', 'TRX': 'TRX-USD',
    },
    '💱 Forex Major': {
        'EUR/USD': 'EURUSD=X', 'GBP/USD': 'GBPUSD=X', 'USD/JPY': 'JPY=X',
        'USD/CHF': 'CHF=X', 'AUD/USD': 'AUDUSD=X', 'USD/CAD': 'CAD=X',
        'NZD/USD': 'NZDUSD=X',
    },
    '💱 Forex Cross': {
        'EUR/GBP': 'EURGBP=X', 'EUR/JPY': 'EURJPY=X', 'GBP/JPY': 'GBPJPY=X',
        'AUD/JPY': 'AUDJPY=X', 'EUR/CHF': 'EURCHF=X', 'GBP/CHF': 'GBPCHF=X',
    },
    '💱 Forex Emerging': {
        'USD/MXN': 'MXN=X', 'USD/BRL': 'BRL=X', 'USD/ARS': 'ARS=X',
        'USD/CNY': 'CNY=X', 'USD/INR': 'INR=X', 'USD/TRY': 'TRY=X',
    },
}

TODOS_ACTIVOS = {}
for grupo, activos in UNIVERSO.items():
    TODOS_ACTIVOS.update(activos)


# ============================================================
# INDICADORES TÉCNICOS
# ============================================================
def ema(s, p): return s.ewm(span=p, adjust=False).mean()
def sma(s, p): return s.rolling(p).mean()

def rsi(s, p=14):
    d = s.diff()
    g = d.where(d > 0, 0).rolling(p).mean()
    l = -d.where(d < 0, 0).rolling(p).mean()
    return 100 - (100 / (1 + g/l.replace(0, np.nan)))

def macd_calc(s, f=12, sl=26, sg=9):
    m = ema(s, f) - ema(s, sl)
    return m, ema(m, sg)

def atr(df, p=14):
    hl = df['High'] - df['Low']
    hc = (df['High'] - df['Close'].shift()).abs()
    lc = (df['Low'] - df['Close'].shift()).abs()
    return pd.concat([hl, hc, lc], axis=1).max(axis=1).rolling(p).mean()

def bollinger(s, p=20, std=2):
    m = sma(s, p)
    sd = s.rolling(p).std()
    return m - std*sd, m, m + std*sd

def stochastic(df, p=14, sm=3):
    hh = df['High'].rolling(p).max()
    ll = df['Low'].rolling(p).min()
    k = 100 * (df['Close'] - ll) / (hh - ll)
    ks = k.rolling(sm).mean()
    return ks, ks.rolling(sm).mean()

def adx(df, p=14):
    h, l, c = df['High'], df['Low'], df['Close']
    tr = pd.concat([(h-l), (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    atr_val = tr.rolling(p).mean()
    up = h.diff()
    dn = -l.diff()
    plus_dm = ((up > dn) & (up > 0)) * up
    minus_dm = ((dn > up) & (dn > 0)) * dn
    plus_di = 100 * plus_dm.rolling(p).mean() / atr_val
    minus_di = 100 * minus_dm.rolling(p).mean() / atr_val
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    return dx.rolling(p).mean()

def donchian(df, p=20):
    return df['High'].rolling(p).max(), df['Low'].rolling(p).min()

def vwap_calc(df):
    typical = (df['High'] + df['Low'] + df['Close']) / 3
    return (typical * df['Volume']).cumsum() / df['Volume'].cumsum()


# ============================================================
# ESTRATEGIAS (6 disponibles)
# ============================================================
def strat_trend(df, params):
    df['EMAf'] = ema(df['Close'], params['ema_fast'])
    df['EMAs'] = ema(df['Close'], params['ema_slow'])
    df['RSI'] = rsi(df['Close'], params['rsi_p'])
    df['MACD'], df['Sig'] = macd_calc(df['Close'])
    df['cu'] = (df['MACD'] > df['Sig']) & (df['MACD'].shift() <= df['Sig'].shift())
    df['cd'] = (df['MACD'] < df['Sig']) & (df['MACD'].shift() >= df['Sig'].shift())
    df['long'] = (df['EMAf'] > df['EMAs']) & (df['RSI'].between(50, 70)) & df['cu']
    df['short'] = (df['EMAf'] < df['EMAs']) & (df['RSI'].between(30, 50)) & df['cd']
    df['exit_l'] = df['RSI'] >= 75
    df['exit_s'] = df['RSI'] <= 25
    return df

def strat_meanrev(df, params):
    df['BBL'], df['BBM'], df['BBU'] = bollinger(df['Close'], params['bb_p'], params['bb_std'])
    df['RSI'] = rsi(df['Close'], params['rsi_p'])
    df['long'] = (df['Close'] <= df['BBL']) & (df['RSI'] < 30)
    df['short'] = (df['Close'] >= df['BBU']) & (df['RSI'] > 70)
    df['exit_l'] = df['Close'] >= df['BBM']
    df['exit_s'] = df['Close'] <= df['BBM']
    return df

def strat_momentum(df, params):
    df['ADX'] = adx(df, params['adx_p'])
    df['K'], df['D'] = stochastic(df, params['stoch_p'])
    df['kx_up'] = (df['K'] > df['D']) & (df['K'].shift() <= df['D'].shift()) & (df['K'] < 50)
    df['kx_dn'] = (df['K'] < df['D']) & (df['K'].shift() >= df['D'].shift()) & (df['K'] > 50)
    df['long'] = (df['ADX'] > 25) & df['kx_up']
    df['short'] = (df['ADX'] > 25) & df['kx_dn']
    df['exit_l'] = df['K'] > 80
    df['exit_s'] = df['K'] < 20
    return df

def strat_donchian(df, params):
    df['DCU'], df['DCL'] = donchian(df, params.get('donchian_p', 20))
    df['DCU_prev'] = df['DCU'].shift()
    df['DCL_prev'] = df['DCL'].shift()
    df['long'] = df['Close'] > df['DCU_prev']
    df['short'] = df['Close'] < df['DCL_prev']
    df['exit_l'] = df['Close'] < df['DCL']
    df['exit_s'] = df['Close'] > df['DCU']
    return df

def strat_triple_ema(df, params):
    df['E1'] = ema(df['Close'], 5)
    df['E2'] = ema(df['Close'], params['ema_fast'])
    df['E3'] = ema(df['Close'], params['ema_slow'])
    df['long'] = (df['E1'] > df['E2']) & (df['E2'] > df['E3']) & \
                 ((df['E1'].shift() <= df['E2'].shift()) | (df['E2'].shift() <= df['E3'].shift()))
    df['short'] = (df['E1'] < df['E2']) & (df['E2'] < df['E3']) & \
                  ((df['E1'].shift() >= df['E2'].shift()) | (df['E2'].shift() >= df['E3'].shift()))
    df['exit_l'] = df['E1'] < df['E2']
    df['exit_s'] = df['E1'] > df['E2']
    return df

def strat_vwap(df, params):
    if 'Volume' not in df.columns or df['Volume'].sum() == 0:
        df['long'] = False
        df['short'] = False
        df['exit_l'] = False
        df['exit_s'] = False
        return df
    df['VWAP'] = vwap_calc(df)
    df['RSI'] = rsi(df['Close'], params['rsi_p'])
    df['long'] = (df['Close'] > df['VWAP']) & (df['RSI'] < 50) & (df['RSI'].shift() <= 30)
    df['short'] = (df['Close'] < df['VWAP']) & (df['RSI'] > 50) & (df['RSI'].shift() >= 70)
    df['exit_l'] = df['Close'] < df['VWAP']
    df['exit_s'] = df['Close'] > df['VWAP']
    return df

ESTRATEGIAS = {
    'EMA + RSI + MACD (Trend)': strat_trend,
    'Bollinger + RSI (Mean Rev)': strat_meanrev,
    'ADX + Stochastic (Momentum)': strat_momentum,
    'Donchian Breakout (Turtle)': strat_donchian,
    'Triple EMA Crossover': strat_triple_ema,
    'VWAP + RSI (Intraday)': strat_vwap,
}


# ============================================================
# MOTOR DE BACKTEST
# ============================================================
def backtest(df, activo, tf, params, estrategia_fn):
    df = df.copy()
    df['ATR'] = atr(df, params['atr_p'])
    df = estrategia_fn(df, params)

    capital = params['capital']
    comision = params['comision']
    slippage = params['slippage']
    riesgo = params['riesgo']
    atr_sl_m = params['atr_sl_m']
    atr_tp_m = params['atr_tp_m']

    eq = capital
    curve = [eq]
    fechas = [df.index[0]]
    pos = None
    trades = []

    for i in range(1, len(df)):
        r = df.iloc[i]
        if pos:
            sal = None
            if pos['t'] == 'long':
                if r['Low'] <= pos['sl']: sal = pos['sl']
                elif r['High'] >= pos['tp']: sal = pos['tp']
                elif r.get('exit_l', False): sal = r['Close']
            else:
                if r['High'] >= pos['sl']: sal = pos['sl']
                elif r['Low'] <= pos['tp']: sal = pos['tp']
                elif r.get('exit_s', False): sal = r['Close']
            if sal:
                if pos['t'] == 'long':
                    sr = sal * (1 - slippage)
                    pnl = (sr - pos['e']) * pos['s']
                else:
                    sr = sal * (1 + slippage)
                    pnl = (pos['e'] - sr) * pos['s']
                pnl -= (pos['e'] * pos['s'] + sr * pos['s']) * comision
                eq += pnl
                trades.append({'tipo': pos['t'], 'entrada': pos['e'], 'salida': sr,
                              'pnl': pnl, 'pnl_pct': pnl/(pos['e']*pos['s'])*100,
                              'fecha': df.index[i]})
                pos = None

        if not pos and not pd.isna(r['ATR']) and r['ATR'] > 0:
            if r.get('long', False):
                e = r['Close'] * (1 + slippage)
                pos = {'t': 'long', 'e': e, 'sl': e - r['ATR']*atr_sl_m,
                       'tp': e + r['ATR']*atr_tp_m, 's': (eq*riesgo)/e}
            elif r.get('short', False):
                e = r['Close'] * (1 - slippage)
                pos = {'t': 'short', 'e': e, 'sl': e + r['ATR']*atr_sl_m,
                       'tp': e - r['ATR']*atr_tp_m, 's': (eq*riesgo)/e}

        curve.append(eq)
        fechas.append(df.index[i])

    if not trades:
        return None, curve, fechas, []

    dft = pd.DataFrame(trades)
    n = len(dft)
    w = dft[dft['pnl'] > 0]
    l = dft[dft['pnl'] <= 0]
    wr = len(w)/n*100
    ret = (eq-capital)/capital*100
    pf = w['pnl'].sum()/abs(l['pnl'].sum()) if len(l) > 0 and l['pnl'].sum() != 0 else 99.0
    arr = np.array(curve)
    rm = np.maximum.accumulate(arr)
    dd = ((arr - rm) / rm * 100).min()

    rets = pd.Series(curve).pct_change().dropna()
    f = {'1d': np.sqrt(252), '1h': np.sqrt(252*24)}.get(tf, np.sqrt(252))
    sh = (rets.mean()/rets.std()*f) if rets.std() > 0 else 0
    neg = rets[rets < 0]
    sortino = (rets.mean()/neg.std()*f) if len(neg) > 0 and neg.std() > 0 else 0
    años = len(curve) / (252 if tf == '1d' else 252*24)
    cagr = ((eq/capital)**(1/años) - 1) * 100 if años > 0 and eq > 0 else 0
    calmar = cagr / abs(dd) if dd < 0 else 0
    avg_win = w['pnl'].mean() if len(w) > 0 else 0
    avg_loss = l['pnl'].mean() if len(l) > 0 else 0
    wl = abs(avg_win/avg_loss) if avg_loss != 0 else 0
    recovery = ret/abs(dd) if dd < 0 else 0

    return {
        'Activo': activo, 'TF': tf.upper(), 'Ops': n,
        'Win rate': f'{wr:.1f}%', 'Retorno': f'{ret:+.1f}%',
        'CAGR': f'{cagr:.1f}%', 'PF': f'{pf:.2f}',
        'Max DD': f'{dd:.1f}%', 'Sharpe': f'{sh:.2f}',
        'Sortino': f'{sortino:.2f}', 'Calmar': f'{calmar:.2f}',
        'Recovery': f'{recovery:.2f}', 'W/L': f'{wl:.2f}',
        '_ret': ret, '_pf': pf, '_sh': sh, '_dd': dd, '_calmar': calmar,
        '_eq_final': eq,
    }, curve, fechas, trades


@st.cache_data(ttl=3600, show_spinner=False)
def descargar(t, i, p):
    try:
        if i == '1h': p = '730d'
        df = yf.download(t, period=p, interval=i, progress=False, auto_adjust=True)
        if df.empty: return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df.dropna()
    except: return None


# ============================================================
# SIDEBAR DE CONFIGURACIÓN
# ============================================================
with st.sidebar:
    st.header('⚙️ Configuración Global')

    st.subheader('📈 Activos')
    grupos_sel = st.multiselect(
        'Selecciona grupos:',
        list(UNIVERSO.keys()),
        default=['🇺🇸 USA Tech Mega', '📊 ETFs Índices USA']
    )

    activos_finales = {}
    for g in grupos_sel:
        activos_finales.update(UNIVERSO[g])

    if activos_finales:
        activos_sel = st.multiselect(
            'Refina selección:',
            list(activos_finales.keys()),
            default=list(activos_finales.keys())
        )
    else:
        activos_sel = []

    ticker_custom = st.text_input('Ticker personalizado:', placeholder='ej: BABA')

    st.divider()
    st.subheader('⏰ Periodo')
    tf_sel = st.selectbox('Temporalidad:', ['1D (Diario)', '1H (Horario)'])
    periodo_sel = st.selectbox('Histórico:', ['1y', '2y', '5y', '10y', 'max'], index=2)

    st.divider()
    with st.expander('🎛️ Parámetros base'):
        col1, col2 = st.columns(2)
        with col1:
            p_ema_fast = st.number_input('EMA fast', value=20, min_value=5, max_value=100)
            p_rsi = st.number_input('RSI period', value=14, min_value=5, max_value=50)
            p_bb = st.number_input('BB period', value=20, min_value=5, max_value=50)
            p_adx = st.number_input('ADX period', value=14, min_value=5, max_value=50)
            p_donchian = st.number_input('Donchian', value=20, min_value=5, max_value=100)
        with col2:
            p_ema_slow = st.number_input('EMA slow', value=50, min_value=10, max_value=200)
            p_atr = st.number_input('ATR period', value=14, min_value=5, max_value=50)
            p_bb_std = st.number_input('BB std', value=2.0, min_value=1.0, max_value=4.0, step=0.1)
            p_stoch = st.number_input('Stoch period', value=14, min_value=5, max_value=30)
        p_sl = st.slider('SL × ATR', 0.5, 5.0, 1.5, 0.1)
        p_tp = st.slider('TP × ATR', 0.5, 10.0, 3.0, 0.1)

    st.divider()
    with st.expander('💰 Costes y capital'):
        p_capital = st.number_input('Capital ($)', value=10000, min_value=100, step=1000)
        p_com = st.slider('Comisión %', 0.0, 1.0, 0.1, 0.01) / 100
        p_slip = st.slider('Slippage %', 0.0, 0.5, 0.05, 0.01) / 100
        p_riesgo = st.slider('Riesgo por trade %', 1, 50, 10) / 100

PARAMS = {
    'ema_fast': p_ema_fast, 'ema_slow': p_ema_slow, 'rsi_p': p_rsi,
    'bb_p': p_bb, 'bb_std': p_bb_std, 'adx_p': p_adx, 'stoch_p': p_stoch,
    'donchian_p': p_donchian, 'atr_p': p_atr, 'atr_sl_m': p_sl, 'atr_tp_m': p_tp,
    'capital': p_capital, 'comision': p_com, 'slippage': p_slip, 'riesgo': p_riesgo,
}

tf_map = {'1D (Diario)': '1d', '1H (Horario)': '1h'}
intervalo = tf_map[tf_sel]


# ============================================================
# TABS PRINCIPALES
# ============================================================
tab_bt, tab_comp, tab_heat, tab_opt, tab_wf, tab_mc = st.tabs([
    '🚀 Backtest Múltiple',
    '⚖️ Comparador',
    '🌡️ Heatmap',
    '🎰 Optimizador',
    '🚶 Walk-Forward',
    '🎲 Monte Carlo',
])

# ============================================================
# TAB 1: BACKTEST MÚLTIPLE
# ============================================================
with tab_bt:
    st.subheader('Backtest sobre múltiples activos')
    col1, col2 = st.columns([2, 1])
    with col1:
        est_sel = st.selectbox('Estrategia:', list(ESTRATEGIAS.keys()), key='bt_est')
    with col2:
        st.metric('Activos a probar', len(activos_sel) + (1 if ticker_custom else 0))

    if st.button('🚀 EJECUTAR BACKTEST', type='primary', use_container_width=True, key='bt_run'):
        lista = list(activos_sel)
        if ticker_custom: lista.append(ticker_custom.upper())

        if not lista:
            st.error('⚠️ Selecciona al menos un activo')
        else:
            resultados, curvas, todos_trades = [], {}, {}
            progress = st.progress(0)
            status = st.empty()

            for idx, nombre in enumerate(lista):
                ticker = TODOS_ACTIVOS.get(nombre, nombre)
                status.text(f'📊 {nombre} ({idx+1}/{len(lista)})')
                progress.progress((idx+1)/len(lista))
                df = descargar(ticker, intervalo, periodo_sel)
                if df is None or len(df) < 100: continue
                res, curve, fechas, trades = backtest(df, nombre, intervalo, PARAMS, ESTRATEGIAS[est_sel])
                if res:
                    resultados.append(res)
                    curvas[nombre] = (fechas, curve)
                    todos_trades[nombre] = trades

            status.empty()
            progress.empty()

            if not resultados:
                st.error('❌ Sin resultados')
            else:
                resultados.sort(key=lambda x: (x['_calmar'], x['_sh'], x['_pf']), reverse=True)
                for i, r in enumerate(resultados):
                    if i == 0 and r['_pf'] > 1 and r['_ret'] > 0: r['Veredicto'] = '🟢 ELEGIDO'
                    elif i == 1 and r['_pf'] > 1 and r['_ret'] > 0: r['Veredicto'] = '🟡 2º'
                    elif r['_ret'] > 0 and r['_pf'] > 1: r['Veredicto'] = '🟠 OK'
                    else: r['Veredicto'] = '🔴 Descartado'

                st.subheader('🔍 Ranking filtrable')
                fc1, fc2, fc3 = st.columns(3)
                with fc1: f_pf = st.slider('PF mínimo', 0.0, 5.0, 0.0, 0.1, key='f_pf')
                with fc2: f_ret = st.slider('Retorno mínimo %', -100, 200, -100, key='f_ret')
                with fc3: f_sh = st.slider('Sharpe mínimo', -3.0, 3.0, -3.0, 0.1, key='f_sh')

                cols = ['Activo', 'TF', 'Ops', 'Win rate', 'Retorno', 'CAGR', 'PF',
                        'Max DD', 'Sharpe', 'Sortino', 'Calmar', 'Recovery', 'W/L', 'Veredicto']
                df_res = pd.DataFrame(resultados)
                df_filt = df_res[(df_res['_pf'] >= f_pf) & (df_res['_ret'] >= f_ret) & (df_res['_sh'] >= f_sh)]
                st.dataframe(df_filt[cols], use_container_width=True, hide_index=True, height=400)

                csv = df_filt[cols].to_csv(index=False).encode('utf-8')
                st.download_button('💾 Descargar CSV', csv, 'results.csv', 'text/csv', key='bt_csv')

                st.subheader('📊 Estadísticas')
                rentables = sum(1 for r in resultados if r['_ret'] > 0)
                c1, c2, c3, c4 = st.columns(4)
                c1.metric('Total', len(resultados))
                c2.metric('Rentables', f'{rentables}/{len(resultados)}', f'{rentables/len(resultados)*100:.0f}%')
                c3.metric('Retorno medio', f'{np.mean([r["_ret"] for r in resultados]):+.1f}%')
                c4.metric('PF medio', f'{np.mean([r["_pf"] for r in resultados]):.2f}')

                st.subheader('🏭 Análisis por sector')
                sector_map = {}
                for grupo, activos in UNIVERSO.items():
                    for a in activos.keys():
                        sector_map[a] = grupo
                df_res['Sector'] = df_res['Activo'].map(sector_map).fillna('Otros')
                df_sect = df_res.groupby('Sector').agg(
                    Activos=('Activo', 'count'),
                    Ret_medio=('_ret', 'mean'),
                    PF_medio=('_pf', 'mean'),
                    Sharpe_medio=('_sh', 'mean'),
                ).round(2).reset_index()
                st.dataframe(df_sect, use_container_width=True, hide_index=True)

                mejor = resultados[0]
                st.subheader(f'🏆 Mejor: {mejor["Activo"]}')
                c1, c2, c3, c4 = st.columns(4)
                c1.metric('Retorno', mejor['Retorno'])
                c2.metric('CAGR', mejor['CAGR'])
                c3.metric('PF', mejor['PF'])
                c4.metric('Max DD', mejor['Max DD'])

                if mejor['Activo'] in curvas:
                    fechas, eq = curvas[mejor['Activo']]
                    arr = np.array(eq)
                    dd_s = (arr - np.maximum.accumulate(arr))/np.maximum.accumulate(arr)*100
                    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                        row_heights=[0.7, 0.3],
                                        subplot_titles=('Equity', 'Drawdown'))
                    fig.add_trace(go.Scatter(x=fechas, y=eq, line=dict(color='#2ecc71', width=2)), row=1, col=1)
                    fig.add_hline(y=p_capital, line_dash='dash', line_color='gray', row=1, col=1)
                    fig.add_trace(go.Scatter(x=fechas, y=dd_s, fill='tozeroy', line=dict(color='#e74c3c')), row=2, col=1)
                    fig.update_layout(height=600, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 2: COMPARADOR
# ============================================================
with tab_comp:
    st.subheader('⚖️ Comparar 2 estrategias lado a lado')
    c1, c2 = st.columns(2)
    with c1: est_a = st.selectbox('Estrategia A:', list(ESTRATEGIAS.keys()), key='comp_a')
    with c2: est_b = st.selectbox('Estrategia B:', list(ESTRATEGIAS.keys()), index=1, key='comp_b')

    activo_comp = st.selectbox('Activo:', list(activos_sel) if activos_sel else ['AAPL'], key='comp_act')

    if st.button('⚖️ Comparar', type='primary', use_container_width=True, key='comp_run'):
        ticker = TODOS_ACTIVOS.get(activo_comp, activo_comp)
        df = descargar(ticker, intervalo, periodo_sel)
        if df is None:
            st.error('❌ No se pudieron descargar datos')
        else:
            with st.spinner('Calculando...'):
                res_a, cur_a, fec_a, _ = backtest(df, activo_comp, intervalo, PARAMS, ESTRATEGIAS[est_a])
                res_b, cur_b, fec_b, _ = backtest(df, activo_comp, intervalo, PARAMS, ESTRATEGIAS[est_b])

            if res_a and res_b:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f'### 🅰️ {est_a.split("(")[0]}')
                    st.metric('Retorno', res_a['Retorno'])
                    st.metric('PF', res_a['PF'])
                    st.metric('Max DD', res_a['Max DD'])
                    st.metric('Sharpe', res_a['Sharpe'])
                    st.metric('Operaciones', res_a['Ops'])
                with col_b:
                    st.markdown(f'### 🅱️ {est_b.split("(")[0]}')
                    st.metric('Retorno', res_b['Retorno'])
                    st.metric('PF', res_b['PF'])
                    st.metric('Max DD', res_b['Max DD'])
                    st.metric('Sharpe', res_b['Sharpe'])
                    st.metric('Operaciones', res_b['Ops'])

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=fec_a, y=cur_a, name=f'A: {est_a.split("(")[0]}',
                                         line=dict(color='#3498db', width=2)))
                fig.add_trace(go.Scatter(x=fec_b, y=cur_b, name=f'B: {est_b.split("(")[0]}',
                                         line=dict(color='#e67e22', width=2)))
                fig.add_hline(y=p_capital, line_dash='dash', line_color='gray')
                fig.update_layout(title=f'Comparación de equity — {activo_comp}',
                                  yaxis_title='Equity ($)', height=500)
                st.plotly_chart(fig, use_container_width=True)

                if res_a['_calmar'] > res_b['_calmar']:
                    st.success(f'🏆 Ganador: Estrategia A')
                else:
                    st.success(f'🏆 Ganador: Estrategia B')
            else:
                st.warning('⚠️ Una o ambas estrategias no generaron operaciones')

# ============================================================
# TAB 3: HEATMAP
# ============================================================
with tab_heat:
    st.subheader('🌡️ Heatmap — Retornos por activo y estrategia')
    st.caption('Prueba TODAS las estrategias sobre TODOS los activos seleccionados')

    if st.button('🌡️ Generar Heatmap', type='primary', use_container_width=True, key='heat_run'):
        lista = list(activos_sel)
        if ticker_custom: lista.append(ticker_custom.upper())

        if not lista:
            st.error('⚠️ Selecciona activos')
        else:
            matriz = {}
            progress = st.progress(0)
            status = st.empty()
            total = len(lista) * len(ESTRATEGIAS)
            count = 0

            for nombre in lista:
                ticker = TODOS_ACTIVOS.get(nombre, nombre)
                df = descargar(ticker, intervalo, periodo_sel)
                if df is None or len(df) < 100: continue
                matriz[nombre] = {}
                for est_name, est_fn in ESTRATEGIAS.items():
                    count += 1
                    status.text(f'{nombre} × {est_name}')
                    progress.progress(count/total)
                    res, _, _, _ = backtest(df, nombre, intervalo, PARAMS, est_fn)
                    matriz[nombre][est_name.split('(')[0].strip()] = res['_ret'] if res else 0

            status.empty()
            progress.empty()

            df_heat = pd.DataFrame(matriz).T
            fig = px.imshow(df_heat,
                            color_continuous_scale='RdYlGn',
                            aspect='auto', text_auto='.1f',
                            zmin=-50, zmax=50,
                            labels=dict(x='Estrategia', y='Activo', color='Retorno %'))
            fig.update_layout(height=max(400, 30*len(df_heat)))
            st.plotly_chart(fig, use_container_width=True)

            st.subheader('🏆 Top 10 combinaciones')
            top_list = []
            for activo, estrats in matriz.items():
                for est, ret in estrats.items():
                    top_list.append({'Activo': activo, 'Estrategia': est, 'Retorno %': round(ret, 2)})
            df_top = pd.DataFrame(top_list).sort_values('Retorno %', ascending=False).head(10)
            st.dataframe(df_top, use_container_width=True, hide_index=True)

# ============================================================
# TAB 4: OPTIMIZADOR
# ============================================================
with tab_opt:
    st.subheader('🎰 Optimizador automático de parámetros')
    st.caption('Busca la mejor combinación de parámetros para una estrategia')

    est_opt = st.selectbox('Estrategia a optimizar:', list(ESTRATEGIAS.keys()), key='opt_est')
    act_opt = st.selectbox('Activo:', list(activos_sel) if activos_sel else ['AAPL'], key='opt_act')

    st.markdown('**Rangos a probar:**')
    c1, c2 = st.columns(2)
    with c1: ef_range = st.slider('EMA fast (min, max)', 5, 50, (10, 30), 5)
    with c2: es_range = st.slider('EMA slow (min, max)', 20, 200, (40, 100), 10)

    sl_range = st.slider('SL multiplier ATR (rango)', 0.5, 5.0, (1.0, 2.5), 0.5)
    tp_range = st.slider('TP multiplier ATR (rango)', 0.5, 10.0, (2.0, 5.0), 0.5)

    if st.button('🎰 Optimizar', type='primary', use_container_width=True, key='opt_run'):
        ticker = TODOS_ACTIVOS.get(act_opt, act_opt)
        df = descargar(ticker, intervalo, periodo_sel)
        if df is None:
            st.error('❌ Datos no disponibles')
        else:
            combos = list(itertools.product(
                range(ef_range[0], ef_range[1]+1, 5),
                range(es_range[0], es_range[1]+1, 10),
                np.arange(sl_range[0], sl_range[1]+0.1, 0.5),
                np.arange(tp_range[0], tp_range[1]+0.1, 0.5),
            ))
            combos = [c for c in combos if c[0] < c[1]]
            st.info(f'🔬 Probando {len(combos)} combinaciones...')

            resultados_opt = []
            progress = st.progress(0)
            for idx, (ef, es, sl, tp) in enumerate(combos):
                progress.progress((idx+1)/len(combos))
                params_t = {**PARAMS, 'ema_fast': ef, 'ema_slow': es, 'atr_sl_m': sl, 'atr_tp_m': tp}
                res, _, _, _ = backtest(df, act_opt, intervalo, params_t, ESTRATEGIAS[est_opt])
                if res:
                    resultados_opt.append({
                        'EMA fast': ef, 'EMA slow': es, 'SL': sl, 'TP': tp,
                        'Retorno': res['_ret'], 'PF': res['_pf'],
                        'Sharpe': res['_sh'], 'Max DD': res['_dd'], 'Ops': res['Ops'],
                    })

            progress.empty()
            if resultados_opt:
                df_opt = pd.DataFrame(resultados_opt).sort_values('Sharpe', ascending=False)
                st.subheader('🏆 Top 20 combinaciones')
                st.dataframe(df_opt.head(20), use_container_width=True, hide_index=True)
                mejor = df_opt.iloc[0]
                st.success(f'**Mejor:** EMA {int(mejor["EMA fast"])}/{int(mejor["EMA slow"])} | '
                          f'SL {mejor["SL"]}× | TP {mejor["TP"]}× → '
                          f'Sharpe {mejor["Sharpe"]:.2f}, Retorno {mejor["Retorno"]:+.1f}%')
            else:
                st.warning('Sin resultados válidos')

# ============================================================
# TAB 5: WALK-FORWARD
# ============================================================
with tab_wf:
    st.subheader('🚶 Walk-Forward Analysis')
    st.caption('Divide la historia en períodos y prueba secuencialmente — robusto contra overfitting')

    est_wf = st.selectbox('Estrategia:', list(ESTRATEGIAS.keys()), key='wf_est')
    act_wf = st.selectbox('Activo:', list(activos_sel) if activos_sel else ['AAPL'], key='wf_act')
    n_ventanas = st.slider('Número de ventanas', 3, 12, 6, key='wf_n')

    if st.button('🚶 Ejecutar Walk-Forward', type='primary', use_container_width=True, key='wf_run'):
        ticker = TODOS_ACTIVOS.get(act_wf, act_wf)
        df = descargar(ticker, intervalo, periodo_sel)
        if df is None or len(df) < 200:
            st.error('❌ Datos insuficientes')
        else:
            ventana_size = len(df) // n_ventanas
            res_wf = []
            progress = st.progress(0)

            for v in range(n_ventanas):
                start = v * ventana_size
                end = (v + 1) * ventana_size
                df_sub = df.iloc[start:end].copy()
                if len(df_sub) < 50: continue
                res, _, _, _ = backtest(df_sub, act_wf, intervalo, PARAMS, ESTRATEGIAS[est_wf])
                if res:
                    res_wf.append({
                        'Ventana': f'V{v+1}',
                        'Desde': df_sub.index[0].strftime('%Y-%m-%d'),
                        'Hasta': df_sub.index[-1].strftime('%Y-%m-%d'),
                        'Retorno': res['_ret'],
                        'PF': res['_pf'],
                        'Sharpe': res['_sh'],
                        'Ops': res['Ops'],
                    })
                progress.progress((v+1)/n_ventanas)
            progress.empty()

            if res_wf:
                df_wf = pd.DataFrame(res_wf)
                st.dataframe(df_wf, use_container_width=True, hide_index=True)

                fig = go.Figure()
                colors = ['#2ecc71' if r > 0 else '#e74c3c' for r in df_wf['Retorno']]
                fig.add_trace(go.Bar(x=df_wf['Ventana'], y=df_wf['Retorno'],
                                     marker_color=colors, text=df_wf['Retorno'].round(1)))
                fig.update_layout(title='Retorno por ventana',
                                  yaxis_title='Retorno %', height=400)
                st.plotly_chart(fig, use_container_width=True)

                positivas = sum(1 for r in df_wf['Retorno'] if r > 0)
                ratio = positivas / len(df_wf)
                if ratio >= 0.66:
                    st.success(f'✅ ROBUSTA: {positivas}/{len(df_wf)} ventanas rentables ({ratio*100:.0f}%)')
                elif ratio >= 0.5:
                    st.warning(f'⚠️ INESTABLE: {positivas}/{len(df_wf)} ventanas rentables ({ratio*100:.0f}%)')
                else:
                    st.error(f'❌ FRÁGIL: Solo {positivas}/{len(df_wf)} ventanas rentables ({ratio*100:.0f}%)')

# ============================================================
# TAB 6: MONTE CARLO
# ============================================================
with tab_mc:
    st.subheader('🎲 Monte Carlo Simulation')
    st.caption('Reordena aleatoriamente los trades N veces para ver el rango de resultados posibles')

    est_mc = st.selectbox('Estrategia:', list(ESTRATEGIAS.keys()), key='mc_est')
    act_mc = st.selectbox('Activo:', list(activos_sel) if activos_sel else ['AAPL'], key='mc_act')
    n_sim = st.slider('Simulaciones', 100, 5000, 1000, 100, key='mc_n')

    if st.button('🎲 Ejecutar Monte Carlo', type='primary', use_container_width=True, key='mc_run'):
        ticker = TODOS_ACTIVOS.get(act_mc, act_mc)
        df = descargar(ticker, intervalo, periodo_sel)
        if df is None:
            st.error('❌ Datos no disponibles')
        else:
            res, _, _, trades = backtest(df, act_mc, intervalo, PARAMS, ESTRATEGIAS[est_mc])
            if not trades:
                st.error('❌ Sin trades para simular')
            else:
                pnls = np.array([t['pnl'] for t in trades])
                final_eqs = []
                max_dds = []
                progress = st.progress(0)

                for i in range(n_sim):
                    progress.progress((i+1)/n_sim)
                    shuffled = np.random.permutation(pnls)
                    curve = p_capital + np.cumsum(shuffled)
                    final_eqs.append(curve[-1])
                    rm = np.maximum.accumulate(curve)
                    dd = ((curve - rm) / rm * 100).min()
                    max_dds.append(dd)
                progress.empty()

                final_eqs = np.array(final_eqs)
                max_dds = np.array(max_dds)
                rets = (final_eqs - p_capital) / p_capital * 100

                c1, c2, c3, c4 = st.columns(4)
                c1.metric('Retorno medio', f'{rets.mean():+.1f}%')
                c2.metric('Mediana', f'{np.median(rets):+.1f}%')
                c3.metric('Peor (5%)', f'{np.percentile(rets, 5):+.1f}%')
                c4.metric('Mejor (95%)', f'{np.percentile(rets, 95):+.1f}%')

                c1, c2, c3, c4 = st.columns(4)
                c1.metric('% Rentables', f'{(rets > 0).mean()*100:.1f}%')
                c2.metric('DD medio', f'{max_dds.mean():.1f}%')
                c3.metric('DD máximo', f'{max_dds.min():.1f}%')
                c4.metric('Simulaciones', n_sim)

                fig = go.Figure()
                fig.add_trace(go.Histogram(x=rets, nbinsx=50, marker_color='#3498db'))
                fig.add_vline(x=0, line_dash='dash', line_color='gray')
                fig.add_vline(x=rets.mean(), line_color='#2ecc71',
                              annotation_text=f'Media {rets.mean():.1f}%')
                fig.update_layout(title='Distribución de retornos finales',
                                  xaxis_title='Retorno (%)', yaxis_title='Frecuencia', height=400)
                st.plotly_chart(fig, use_container_width=True)

                pct_rentable = (rets > 0).mean() * 100
                if pct_rentable >= 90:
                    st.success(f'✅ MUY ROBUSTA: {pct_rentable:.0f}% rentables')
                elif pct_rentable >= 70:
                    st.info(f'👍 ROBUSTA: {pct_rentable:.0f}% rentables')
                elif pct_rentable >= 50:
                    st.warning(f'⚠️ MODERADA: {pct_rentable:.0f}% rentables')
                else:
                    st.error(f'❌ FRÁGIL: Solo {pct_rentable:.0f}% rentables')

st.divider()
st.caption('⚠️ Backtest Pro v4 · Herramienta de análisis cuantitativo · No constituye asesoramiento financiero.')
