#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patcher: BASE_CUSTOM_PROJECT_MASTER_CLEAN_SQX_V1_SOURCE_ONLY.cfx -> 4 edge-specific Custom Projects
for NDXm_TICK_UTCPlus02 / Tickmill - Nasdaq, per SQX_PROJECT_SKILLS_OOS_20_30_EXISTING_SESSION_SHORTNAME_SAFE package.
"""
import re, os, shutil, zipfile, json
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

BASE_DIR = "C:/Users/LEON6/AppData/Local/Temp/ndx_peek/base"
OUT_ROOT = "E:/PROYECTOS/CLAUDE CODE/STRATEGY QUANT/outputs/NDXm_OANDA_20260831"
WORK = os.path.join(OUT_ROOT, "_work")

TASK_FILES = ["Build-Task1.xml","Retest-Task1.xml","Retest-Task2.xml","Retest-Task3.xml",
              "Retest-Task4.xml","Retest-Task5.xml","Retest-Task6.xml","Retest-Task7.xml"]

# ---------------------------------------------------------------- global identity/cost params
ASSET = "NDXm_TICK_UTCPlus02"
INSTRUMENT = "NDXm(2)"   # confirmed real Data Manager instrument id (from sibling NDXm_Qlib_OOS20.cfx), NOT the symbol name
BROKER_LABEL = "OANDA"
STRATEGY_FILE = r"D:\work\StrategyQuant4\work_directory\StrategyQuant\user\projects\Retester\databanks\Results\Strategy 0.1.7.sq4"

def epoch_ms(y,m,d):
    return int(datetime(y,m,d,tzinfo=timezone.utc).timestamp()*1000)

BUILDER_START_D = (2018,6,27)
OOS_START_D     = (2023,6,1)
NORMAL_END_D    = (2025,1,1)

# Epoch-ms values: ONLY used for month-math and for the Resources/Symbols catalog dateFrom/dateTo
# (confirmed epoch-ms format from the real working sibling project).
BUILDER_START = str(epoch_ms(*BUILDER_START_D))
OOS_START     = str(epoch_ms(*OOS_START_D))
NORMAL_END    = str(epoch_ms(*NORMAL_END_D))
TICK_START    = BUILDER_START
TICK_END      = NORMAL_END

# Text "yyyy.MM.dd" values: this is what Setup/Range dateFrom/dateTo actually expect (confirmed
# from the sibling project's working Setup elements: dateFrom="2018.06.27" dateTo="2026.06.25").
# Using epoch-ms there caused: "Cannot resolve resources - Invalid format: '...' is malformed at '0000'".
def date_str(y,m,d):
    return f"{y:04d}.{m:02d}.{d:02d}"

BUILDER_START_STR = date_str(*BUILDER_START_D)
OOS_START_STR     = date_str(*OOS_START_D)
NORMAL_END_STR    = date_str(*NORMAL_END_D)
TICK_START_STR    = BUILDER_START_STR
TICK_END_STR      = NORMAL_END_STR

# Confirmed real bounds for the Resources/Symbols catalog entry (full available range in Data
# Manager for this exact symbol, from the sibling project), independent of our chosen IS/OOS window.
SYMBOL_CATALOG_DATEFROM_MS = "1530057600000"   # 2018-06-27
SYMBOL_CATALOG_DATETO_MS   = "1782345600000"   # ~2026-06-25 (full available data)

# Costs below come from a LIVE MT5 query (mt5.symbol_info) against symbol "US100" on the OANDA
# Global Live-1 account, snapshot 2026-08-31 (see outputs/COSTOS_MERCADO_OANDA_20260831/).
# tickSize stays 0.01 (property of the NDXm_TICK_UTCPlus02 Darwinex-sourced price DATA already in
# Data Manager, confirmed via Edit Symbol dialog) -- it is independent of which broker's costs we
# overlay. pointValue=1.0 is confirmed consistent between the existing Data Manager record AND
# OANDA's live US100 (tick_value/tick_size = 0.1/0.1 = 1.0), which cross-validates the assumption.
TICK_SIZE = "0.01"
TICK_STEP = "0.01"
POINT_VALUE = "1.0"                # confirmed: OANDA US100 tick_value/tick_size = 1.0
DEFAULT_SPREAD = "2.2"             # OANDA US100 live spread snapshot: 22 points * 0.1 = 2.2
DEFAULT_SLIPPAGE = "0.01"          # not a broker-reported field; kept as a conservative 1-tick assumption
COMMISSION = "0"                   # OANDA CFD indices: spread-only, no separate commission
SWAP_LONG = "-15.02"               # OANDA US100 swap_long, estimated $/lot/day (INTEREST_CURRENT formula)
SWAP_SHORT = "2.79"                # OANDA US100 swap_short, estimated $/lot/day
MIN_DISTANCE = "0.0"
DECIMALS = "2"
CAPITAL = "1000"
RISKED_MONEY = "15"   # 1.5% of capital, documented assumption (not explicitly ordered)

MC_SPREAD_MIN, MC_SPREAD_MAX = "2.2", "6.6"   # 1x-3x live spread
# RandomizeSlippage/RandomizeSpread (SQ.MonteCarlo.Retest, Snippets.jar) compute
# n = (int)((Max-Min)/0.1) and call IRandomGenerator.nextInt(n) -- 0.1 is a hardcoded
# engine step, unrelated to the symbol's tickSize. Any Max-Min < 0.1 truncates to n=0
# and crashes with "Exception in backtest: n must be positive, got: 0" on every single
# simulation (confirmed by decompiling RandomizeSlippage.class / RandomizeSpread.class
# with javap). The previous 0.01-0.05 range (width 0.04) was always broken; widening it
# past 0.1 is mandatory, not optional. See PropFirm_Management/21_incidente... for detail.
MC_SLIP_MIN, MC_SLIP_MAX = "0.0", "0.5"   # width 0.5 -> n=5 discrete steps, safely above the 0.1 engine floor

COMMON_COMPARATORS = ["IsGreater","IsLower","IsGreaterOrEqual","IsLowerOrEqual",
                      "CrossesAbove","CrossesBelow","IsRising","IsFalling",
                      "Prices.Close","Prices.High","Prices.Low","Prices.Open"]

EDGES = {
 "E1": dict(
    name="Trend Following EMA/ADX", shortname="NDXM_OANDA_E1_H1TF_V4",
    timeframe="H1", direction="long",
    rules=dict(minConditions=2,maxConditions=3,minExitConditions=0,maxExitConditions=1,
               minExitTypes=1,maxExitTypes=2,minPeriod=10,maxPeriod=100,minShift=1,maxShift=1),
    slpt=dict(slMin=1.2, slMax=2.8, slPer=(14,28), ptMin=2.0, ptMax=4.5, ptPer=(14,28),
              rrrFrom=150, rrrTo=400),
    order_type="EnterAtMarket", stoplimit=[],
    exit_types=dict(exitafterbars=False, movesl2be=False, profittarget=True, stoploss=True,
                     trailing=True),
    indicators=["Indicators.EMA","Indicators.SMA","Indicators.ADX","Indicators.ATR"],
    signals=["MARising","MAFalling","MABarClosesAbove","MABarClosesBelow","ADXRising","ADXHigher"],
    trades_per_month=1.5,
    genetic=dict(pf=1.02, dd_max=60),
    ranking=dict(pf=1.05, retdd=1.60, dd_max=40, stag_max=40, winpct=None),
    notes="Tesis: en regimen alcista con vol media, EMA rapida sobre EMA lenta + ADX creciente confirma persistencia direccional. Entrada Market, salida ATR SL + Trailing (deja correr ganadoras).",
 ),
 "E2": dict(
    name="Pullback Continuation EMA/RSI", shortname="NDXM_OANDA_E2_M15PB_V4",
    timeframe="M15", direction="long",
    rules=dict(minConditions=2,maxConditions=4,minExitConditions=0,maxExitConditions=1,
               minExitTypes=1,maxExitTypes=2,minPeriod=5,maxPeriod=60,minShift=1,maxShift=1),
    slpt=dict(slMin=1.0, slMax=2.2, slPer=(14,21), ptMin=1.2, ptMax=2.8, ptPer=(14,21),
              rrrFrom=80, rrrTo=250),
    order_type="EnterAtMarket", stoplimit=[],
    exit_types=dict(exitafterbars=True, movesl2be=False, profittarget=True, stoploss=True,
                     trailing=False),
    indicators=["Indicators.EMA","Indicators.SMA","Indicators.RSI","Indicators.ATR"],
    signals=["MARising","MAFalling","RSICrossUp","RSICrossDown","RSILower","RSIRising"],
    trades_per_month=6.0,
    genetic=dict(pf=1.02, dd_max=55),
    ranking=dict(pf=1.10, retdd=1.80, dd_max=35, stag_max=35, winpct=38),
    notes="Tesis: dentro de tendencia alcista dominante, retroceso hacia EMA (RSI sale de zona baja) ofrece reentrada a favor de tendencia. Entrada Market, salida SL+PT ATR + limite de barras.",
 ),
 "E3": dict(
    name="Volatility Expansion Breakout", shortname="NDXM_OANDA_E3_H1BO_V4",
    timeframe="H1", direction="long",
    rules=dict(minConditions=1,maxConditions=3,minExitConditions=0,maxExitConditions=1,
               minExitTypes=1,maxExitTypes=2,minPeriod=10,maxPeriod=80,minShift=1,maxShift=1),
    slpt=dict(slMin=1.4, slMax=3.0, slPer=(14,28), ptMin=2.5, ptMax=5.0, ptPer=(14,28),
              rrrFrom=150, rrrTo=450),
    order_type="EnterAtStop", stoplimit=["Stop/Limit Price Levels.Highest","Stop/Limit Price Ranges.ATR"],
    exit_types=dict(exitafterbars=False, movesl2be=False, profittarget=True, stoploss=True,
                     trailing=True),
    indicators=["Indicators.ATR","Indicators.Highest","Indicators.Lowest"],
    signals=["ATRRising","ATRHigher","ATRFalling"],
    trades_per_month=1.2,
    genetic=dict(pf=1.00, dd_max=65),
    ranking=dict(pf=1.03, retdd=1.50, dd_max=42, stag_max=42, winpct=None),
    notes="Tesis: ruptura del maximo de N barras con expansion de ATR confirma continuacion de impulso alcista. Entrada Stop sobre Highest(N), SL/PT y trailing basados en ATR.",
 ),
 "E4": dict(
    name="Selective Mean Reversion (buy-the-dip)", shortname="NDXM_OANDA_E4_M15MR_V4",
    timeframe="M15", direction="long",
    rules=dict(minConditions=2,maxConditions=4,minExitConditions=0,maxExitConditions=1,
               minExitTypes=1,maxExitTypes=2,minPeriod=5,maxPeriod=50,minShift=1,maxShift=1),
    slpt=dict(slMin=1.0, slMax=2.0, slPer=(10,20), ptMin=1.0, ptMax=2.2, ptPer=(10,20),
              rrrFrom=60, rrrTo=200),
    order_type="EnterAtMarket", stoplimit=[],
    exit_types=dict(exitafterbars=True, movesl2be=False, profittarget=True, stoploss=True,
                     trailing=False),
    indicators=["Indicators.EMA","Indicators.RSI","Indicators.BollingerBands","Indicators.ATR"],
    signals=["RSILower","RSICrossUp","RSIRising","MARising"],
    trades_per_month=8.0,
    genetic=dict(pf=1.02, dd_max=55),
    ranking=dict(pf=1.12, retdd=1.70, dd_max=32, stag_max=32, winpct=45),
    notes="Tesis: dentro de tendencia alcista (EMA de contexto), RSI sobrevendido / toque de banda inferior de Bollinger ofrece entrada de reversion a favor del sesgo dominante (buy-the-dip). Entrada Market, salida cercana SL/PT + limite de barras.",
 ),
}

def months_between(d1_ms, d2_ms):
    d1 = datetime.fromtimestamp(int(d1_ms)/1000, tz=timezone.utc)
    d2 = datetime.fromtimestamp(int(d2_ms)/1000, tz=timezone.utc)
    return (d2-d1).days/30.4368

MESES_IS = months_between(BUILDER_START, OOS_START)
MESES_OOS = months_between(OOS_START, NORMAL_END)
MESES_FULL = months_between(BUILDER_START, NORMAL_END)

print(f"Meses_IS={MESES_IS:.1f}  Meses_OOS={MESES_OOS:.1f}  Meses_FULL(tick)={MESES_FULL:.1f}")

# ---------------------------------------------------------------- phase 1: text substitutions
def phase1_text(txt):
    # two placeholders on same line (SPP/WFA primary Setup) -- Setup/Range dates use "yyyy.MM.dd" text format
    txt = re.sub(r'dateFrom="__DATE_REPLACE__" dateTo="__DATE_REPLACE__"',
                 f'dateFrom="{BUILDER_START_STR}" dateTo="{NORMAL_END_STR}"', txt)
    txt = txt.replace("__DATE_REPLACE__", BUILDER_START_STR)  # remaining lone occurrences (dateFrom position)

    txt = txt.replace("FX_XCCY_Currency1__BROKER_PROFILE__", "No Session")
    txt = txt.replace("__SESSION__", "No Session")
    txt = txt.replace("__BROKER_PROFILE__", BROKER_LABEL)
    txt = txt.replace("__BROKER_NAME__", BROKER_LABEL)

    txt = txt.replace("[[__ASSET__]]", ASSET)
    txt = txt.replace("__ASSET__", ASSET)
    txt = txt.replace("__NORMAL_SYMBOL__", ASSET)
    txt = txt.replace("__TICK_SYMBOL__", ASSET)
    txt = txt.replace("__INSTRUMENT__", INSTRUMENT)
    txt = txt.replace("__STRATEGY_FILE__", STRATEGY_FILE)

    txt = txt.replace("__BUILDER_START__", BUILDER_START_STR)
    txt = txt.replace("__OOS_START__", OOS_START_STR)
    txt = txt.replace("__NORMAL_END__", NORMAL_END_STR)
    txt = txt.replace("__TICK_START__", TICK_START_STR)
    txt = txt.replace("__TICK_END__", TICK_END_STR)
    return txt

def fix_symbol_tag(txt):
    """Rewrite the Resources/Symbols catalog <Symbol name="ASSET" ...> opening tag(s) to match the
    confirmed real Data Manager record for this exact symbol (from the working sibling project
    user/projects/Builder/NDXm_Qlib_OOS20.cfx). Uses epoch-ms (confirmed correct in this context,
    unlike Setup/Range which need text dates)."""
    def repl(m):
        tag = m.group(0)
        tag = re.sub(r'source="[^"]*"', 'source="4"', tag)
        tag = re.sub(r'precision="[^"]*"', 'precision="TICK"', tag)
        tag = re.sub(r'timezone="[^"]*"', 'timezone="EET"', tag)
        tag = re.sub(r'uSymbol="[^"]*"', 'uSymbol="NDXm"', tag)
        tag = re.sub(r'uSymbolName="[^"]*"', 'uSymbolName="NDXm"', tag)
        tag = re.sub(r'dateFrom="[^"]*"', f'dateFrom="{SYMBOL_CATALOG_DATEFROM_MS}"', tag)
        tag = re.sub(r'dateTo="[^"]*"', f'dateTo="{SYMBOL_CATALOG_DATETO_MS}"', tag)
        tag = re.sub(r'\s*groupDescription="[^"]*"', '', tag)  # stray attr from the D1-asset scaffold variant
        if "cloneFrom" not in tag:
            tag = tag[:-1] + ' cloneFrom="NDXm" sourceTimezone="Etc/UCT">'
        return tag
    return re.sub(rf'<Symbol name="{re.escape(ASSET)}"[^>]*>', repl, txt)

# ---------------------------------------------------------------- InstrumentInfo cost rewrite (regex, attribute-level)
# Values below reconciled against the CONFIRMED real Data Manager record for this exact symbol
# (sibling project user/projects/Builder/NDXm_Qlib_OOS20.cfx): tickValueInMoney stays 0.0 (separate,
# unused field -- pointValue is the real "point value in $"), dataType=6, commissions Method type=None,
# swap type=money, description/exchange/country/sector match the confirmed record.
INSTR_ATTR_REPLACERS = [
    (r'tickSize="[^"]*"', f'tickSize="{TICK_SIZE}"'),
    (r'tickStep="[^"]*"', f'tickStep="{TICK_STEP}"'),
    (r'minDistance="[^"]*"', f'minDistance="{MIN_DISTANCE}"'),
    (r'tickValueInMoney="[^"]*"', 'tickValueInMoney="0.0"'),
    (r'defaultSpread="[^"]*"', f'defaultSpread="{DEFAULT_SPREAD}"'),
    (r'defaultSlippage="[^"]*"', f'defaultSlippage="{DEFAULT_SLIPPAGE}"'),
    (r'decimals="[^"]*"', f'decimals="{DECIMALS}"'),
    (r'pointValue="[^"]*"', f'pointValue="{POINT_VALUE}"'),
    (r'dataType="[^"]*"', 'dataType="6"'),
    (r'exchange="[^"]*"', 'exchange=""'),
    (r'country="[^"]*"', 'country=""'),
    (r'sector="[^"]*"', 'sector=""'),
]

def patch_instrumentinfo_blocks(txt):
    # operate only inside <InstrumentInfo .../> self-closed tags
    def repl(m):
        tag = m.group(0)
        for pat, new in INSTR_ATTR_REPLACERS:
            tag = re.sub(pat, new, tag)
        tag = re.sub(r'commissions="[^"]*"',
                      'commissions="&lt;Method type=&quot;None&quot; use=&quot;true&quot;&gt;&lt;Params/&gt;&lt;/Method&gt;"',
                      tag)
        tag = re.sub(r'swap="[^"]*"',
                      f'swap="&amp;lt;Swap use=&amp;quot;true&amp;quot; type=&amp;quot;money&amp;quot; long=&amp;quot;{SWAP_LONG}&amp;quot; short=&amp;quot;{SWAP_SHORT}&amp;quot; tripleSwapOn=&amp;quot;FRIDAY&amp;quot; rolloutHour=&amp;quot;23:00&amp;quot;/&amp;gt;"'.replace('&amp;','&'),
                      tag)
        tag = re.sub(r'description="[^"]*"', 'description="Darwinex instrument"', tag)
        return tag
    return re.sub(r'<InstrumentInfo\b[^>]*/>', repl, txt)

def patch_setup_swap(txt):
    # <Swap use="true" type="points" long="X" short="Y" .../> direct elements inside <Setup><Data>...
    def repl(m):
        tag = m.group(0)
        tag = re.sub(r'type="[^"]*"', 'type="money"', tag)
        tag = re.sub(r'long="[^"]*"', f'long="{SWAP_LONG}"', tag)
        tag = re.sub(r'short="[^"]*"', f'short="{SWAP_SHORT}"', tag)
        return tag
    return re.sub(r'<Swap use="true"[^>]*/>', repl, txt)

def patch_setup_charts(txt, timeframe):
    # Chart symbol timeframe spread — force EVERY <Chart symbol=ASSET .../> tag (both the
    # primary block and the secondary "detailed settings" duplicate) to the edge's own
    # timeframe. The base template ships Retest-Task4 (SPP) and Retest-Task7 (WFA MATRIX)
    # hardcoded to D1/H4 regardless of edge timeframe -- confirmed by inspecting
    # 07_BASE_CUSTOM_PROJECT_MASTER_CLEAN_SQX_V1_SOURCE_ONLY.cfx directly, present before any
    # patching. Skill 3 SS71-78 ("Auditoria Multi-Timeframe Quality Gate") requires timeframe
    # per task to match the edge and explicitly blocks delivery otherwise -- a previous version
    # of this function only replaced timeframe="H1", silently leaving SPP/WFA on the wrong
    # timeframe. Always overwrite, regardless of the tag's current timeframe value.
    def repl(m):
        tag = m.group(0)
        tag = re.sub(r'timeframe="[^"]*"', f'timeframe="{timeframe}"', tag)
        tag = re.sub(r'spread="[^"]*"', f'spread="{DEFAULT_SPREAD}"', tag)
        return tag
    return re.sub(rf'<Chart symbol="{re.escape(ASSET)}"[^>]*/>', repl, txt)

def patch_setup_slippage(txt):
    # Setup slippage="X" attribute -> DEFAULT_SLIPPAGE (only where currently 0 or 0.1, i.e. all Setup tags)
    def repl(m):
        tag = m.group(0)
        tag = re.sub(r'slippage="[^"]*"', f'slippage="{DEFAULT_SLIPPAGE}"', tag)
        return tag
    return re.sub(r'<Setup dateFrom="[^"]*" dateTo="[^"]*"[^>]*>', repl, txt)

def patch_commission_blocks(txt):
    return re.sub(r'(<Param key="Commission" className="SizeBased">)[^<]*(</Param>)',
                  rf'\g<1>{COMMISSION}\g<2>', txt)

# ---------------------------------------------------------------- DataBank chain residue fix
# See patch_cfx.py (Tickmill generator) for the full explanation. Root cause of the real-world
# incident (2026-08-31, NDXM_TMILL_E2_M15PB): OOS->MC_TRADES->MC_SPREAD_SLIPPAGE never populated
# because the base's retestSelected="false" Databanks block (the one SQX actually routes on) still
# carried donor-project residual names ("MONTECARLO RNADOMIZE TRADES Y SKIP TRADES", "MONTECARLO
# SLIPPAGE Y SPREAD", "GESTION MONETARIA" without "- DESACTIVADA") instead of the real chain names.
DATABANK_CHAIN_FIXES = {
    "Retest-Task2.xml": [
        ('value="MONTECARLO RNADOMIZE TRADES Y SKIP TRADES"', 'value="MC_TRADES"'),
        ('value="GESTION MONETARIA"', 'value="OOS"'),
    ],
    "Retest-Task3.xml": [
        ('value="MONTECARLO SLIPPAGE Y SPREAD"', 'value="MC_SPREAD_SLIPPAGE"'),
        ('value="MONTECARLO RNADOMIZE TRADES Y SKIP TRADES"', 'value="MC_TRADES"'),
    ],
    "Retest-Task5.xml": [
        ('value="MONTECARLO SLIPPAGE Y SPREAD"', 'value="MC_SPREAD_SLIPPAGE"'),
    ],
    "Retest-Task6.xml": [
        ('value="GESTION MONETARIA"', 'value="GESTION MONETARIA - DESACTIVADA"'),
    ],
}
GENERIC_DATABANKS_BLOCK = (
    '<Databanks>\n'
    '    <Databank label="Output databank" name="Output" value="Results" />\n'
    '    <Databank label="Input databank" name="Input" value="Results" />\n'
    '  </Databanks>'
)
GENERIC_DATABANKS_TARGET = {
    "Retest-Task1.xml": ("OOS", "Results"),
    "Retest-Task2.xml": ("MC_TRADES", "OOS"),
    "Retest-Task3.xml": ("MC_SPREAD_SLIPPAGE", "MC_TRADES"),
}

def fix_databank_chain(txt, fname):
    for old, new in DATABANK_CHAIN_FIXES.get(fname, []):
        txt = txt.replace(old, new)
    if fname in GENERIC_DATABANKS_TARGET and GENERIC_DATABANKS_BLOCK in txt:
        out_val, in_val = GENERIC_DATABANKS_TARGET[fname]
        replacement = (
            '<Databanks>\n'
            f'    <Databank label="Output databank" name="Output" value="{out_val}" />\n'
            f'    <Databank label="Input databank" name="Input" value="{in_val}" />\n'
            '  </Databanks>'
        )
        txt = txt.replace(GENERIC_DATABANKS_BLOCK, replacement)
    return txt

# ---------------------------------------------------------------- ElementTree structural edits
def strip_ns(tag):
    return tag

def edit_build_task(root, edge):
    # BuildTradingOptions Session param already "No Session" via text pass; MarketOpenSession too.
    # RulesComplexity
    rc = edge["rules"]
    for chart in root.iter("Chart"):
        if chart.tag == "Chart" and chart.get("name") == "Main chart":
            for k,v in rc.items():
                if k in ("minConditions","maxConditions","minExitConditions","maxExitConditions",
                         "minExitTypes","maxExitTypes","minPeriod","maxPeriod","minShift","maxShift"):
                    chart.set(k, str(v))
    # MarketSides
    ms = root.find(".//MarketSides")
    if ms is not None:
        ms.set("type", edge["direction"])
    # SLPTOptions
    slpt = root.find(".//SLPTOptions")
    if slpt is not None:
        s = edge["slpt"]
        slpt.find("MinSLATRMultiple").text = str(s["slMin"])
        slpt.find("MaxSLATRMultiple").text = str(s["slMax"])
        slpt.find("MinSLATRPeriod").text = str(s["slPer"][0])
        slpt.find("MaxSLATRPeriod").text = str(s["slPer"][1])
        slpt.find("MinPTATRMultiple").text = str(s["ptMin"])
        slpt.find("MaxPTATRMultiple").text = str(s["ptMax"])
        slpt.find("MinPTATRPeriod").text = str(s["ptPer"][0])
        slpt.find("MaxPTATRPeriod").text = str(s["ptPer"][1])
        slpt.find("LimitSLPTRRRFrom").text = str(s["rrrFrom"])
        slpt.find("LimitSLPTRRRTo").text = str(s["rrrTo"])
    # StrategyType templateFile/strategyFile already set via text pass (STRATEGY_FILE global replace)

    # Genetic prefilters (BuildMode/Conditions) -- 3 known conditions: ProfitFactor, NumberOfTrades, DrawdownPct
    gmin_final = MESES_IS * edge["trades_per_month"]
    gmin_genetic = gmin_final * 0.6
    for cond in root.findall(".//BuildMode/Conditions/Condition"):
        colv = cond.find(".//Column-Value")
        if colv is None: continue
        cls = colv.get("class")
        num = cond.find("./Right-Side/Numeric-Value")
        if cls == "ProfitFactor" and num is not None:
            num.set("value", f'{edge["genetic"]["pf"]:.2f}')
        elif cls == "NumberOfTrades" and num is not None:
            num.set("value", str(int(round(gmin_genetic))))
        elif cls == "DrawdownPct" and num is not None:
            num.set("value", str(edge["genetic"]["dd_max"]))

    # Ranking Final (Rankings/Conditions at top-level, NOT inside BuildMode)
    rankings = root.find(".//Rankings")
    if rankings is not None:
        for cond in rankings.findall("./Conditions/Condition"):
            colv = cond.find(".//Column-Value")
            if colv is None: continue
            cls = colv.get("class")
            num = cond.find("./Right-Side/Numeric-Value")
            if num is None: continue
            r = edge["ranking"]
            if cls == "NumberOfTrades":
                num.set("value", str(int(round(gmin_final))))
            elif cls == "ProfitFactor":
                num.set("value", f'{r["pf"]:.2f}')
            elif cls == "ReturnDDRatio":
                num.set("value", f'{r["retdd"]:.2f}')
            elif cls == "DrawdownPct":
                num.set("value", str(r["dd_max"]))
            elif cls == "StagnationPct":
                num.set("value", str(r["stag_max"]))
            elif cls == "AvgTrade":
                num.set("value", "0")
            elif cls == "WinningPct":
                if r["winpct"] is None:
                    cond.set("use", "false")
                else:
                    num.set("value", str(r["winpct"]))

    edit_building_blocks(root, edge)
    edit_order_exit_types(root, edge)
    edit_risk_mm(root)
    return root

def edit_building_blocks(root, edge):
    whitelist_ind_sig = set(COMMON_COMPARATORS) | set(edge["indicators"]) | set(edge["signals"])
    whitelist_stoplimit = set(edge["stoplimit"])
    for blocks_parent_tag in ("BuildingBlocks",):
        parent = root.find(f".//{blocks_parent_tag}")
        if parent is None:
            continue
        for block in parent.iter("Block"):
            cat = block.get("category")
            key = block.get("key")
            if cat in ("indicators","signals"):
                block.set("use", "true" if key in whitelist_ind_sig else "false")
            elif cat == "stopLimitBlocks":
                block.set("use", "true" if key in whitelist_stoplimit else "false")

def edit_order_exit_types(root, edge):
    for order_types in root.iter("OrderTypes"):
        if order_types.find("./Block") is None:
            continue  # this is the PartsToImprove/OrderTypes stub, not the real Block catalog
        for block in order_types.findall("./Block"):
            block.set("use", "true" if block.get("key") == edge["order_type"] else "false")
    exit_types = root.find(".//ExitTypes")
    if exit_types is not None:
        ex = edge["exit_types"]
        mapping = {
            "ExitAfterBars.ExitAfterBars": ex["exitafterbars"],
            "MoveSL2BE.MoveSL2BE": ex["movesl2be"],
            "MoveSL2BE.SL2BEAddPips": ex["movesl2be"],
            "ProfitTarget.ProfitTarget": ex["profittarget"],
            "StopLoss.StopLoss": ex["stoploss"],
            "TrailingStop.TrailingStop": ex["trailing"],
            "TrailingStop.TrailingActivation": ex["trailing"],
            "_ExitRule_": False,
        }
        for block in exit_types.findall("./Block"):
            key = block.get("key")
            if key in mapping:
                block.set("use", "true" if mapping[key] else "false")

def edit_risk_mm(root):
    ic = root.find(".//RiskMoneyManagement/MoneyManagement/InitialCapital")
    if ic is not None:
        ic.text = CAPITAL
    for method in root.findall(".//RiskMoneyManagement/MoneyManagement/Method"):
        if method.get("type") == "FixedAmount":
            for p in method.findall("./Params/Param"):
                if p.get("key") == "RiskedMoney":
                    p.text = RISKED_MONEY

def edit_oos_task(root, edge):
    # Range = OOS1 (already OOS_START..NORMAL_END via text pass). Ranking Final proportional to Meses_OOS.
    gmin_oos = MESES_OOS * edge["trades_per_month"]
    r = edge["ranking"]
    rankings = root.find(".//Rankings")
    if rankings is not None:
        for cond in rankings.findall("./Conditions/Condition"):
            colv = cond.find(".//Column-Value")
            if colv is None: continue
            cls = colv.get("class")
            num = cond.find("./Right-Side/Numeric-Value")
            if num is None: continue
            if cls == "NumberOfTrades":
                num.set("value", str(max(5, int(round(gmin_oos)))))
            elif cls == "ProfitFactor":
                num.set("value", "1.03")
            elif cls == "ReturnDDRatio":
                num.set("value", "0.90")
            elif cls == "DrawdownPct":
                num.set("value", str(min(50, r["dd_max"]+8)))
            elif cls == "AvgTrade":
                num.set("value", "0")
    for dfs in root.iter("DeleteFailedStrategies"):
        dfs.text = "true"

def set_delete_failed_true(root):
    for dfs in root.iter("DeleteFailedStrategies"):
        dfs.text = "true"

_FORMATS = {
    "NetProfit": "Decimal2PL", "ProfitFactor": "Decimal2", "NumberOfTrades": "Integer",
    "DrawdownPct": "Decimal2Pct", "ReturnDDRatio": "Decimal2", "AvgTrade": "Decimal2PL",
    "StagnationPct": "Decimal2Pct", "WinningPct": "Decimal2Pct",
}

def make_condition(cls, comparator, value):
    cond = ET.Element("Condition", {"use": "true"})
    left = ET.SubElement(cond, "Left-Side", {"valueType": "column"})
    ET.SubElement(left, "Column-Value", {
        "column": cls, "columnType": "0", "format": _FORMATS[cls], "resultType": "main",
        "direction": "0", "sampleType": "127", "plType": "10", "confidenceLevel": "50",
        "market": "1", "subresult": "30", "pctRatio": "0", "class": cls,
    })
    ET.SubElement(cond, "Comparator", {"value": comparator})
    right = ET.SubElement(cond, "Right-Side", {"valueType": "numeric"})
    ET.SubElement(right, "Numeric-Value", {"value": str(value)})
    return cond

def edit_tick_task(root, edge):
    gmin_tick = max(10, int(round(MESES_FULL * edge["trades_per_month"])))
    r = edge["ranking"]
    rankings = root.find(".//Rankings")
    if rankings is not None:
        conds = rankings.find("./Conditions")
        if conds is not None:
            for child in list(conds):
                conds.remove(child)
            conds.append(make_condition("NetProfit", ">", 0))
            conds.append(make_condition("ProfitFactor", ">", 1.02))
            conds.append(make_condition("NumberOfTrades", ">", gmin_tick))
            conds.append(make_condition("DrawdownPct", "<", min(55, r["dd_max"] + 10)))
            conds.append(make_condition("ReturnDDRatio", ">", 0.70))
            conds.append(make_condition("AvgTrade", ">", 0))
    set_delete_failed_true(root)

def edit_mc_spread_slippage_task(root):
    for method in root.iter("Method"):
        mtype = method.get("type")
        if mtype == "RandomizeSpread":
            for p in method.findall("./Params/Param"):
                if p.get("key") == "Min": p.text = MC_SPREAD_MIN
                if p.get("key") == "Max": p.text = MC_SPREAD_MAX
        elif mtype == "RandomizeSlippage":
            for p in method.findall("./Params/Param"):
                if p.get("key") == "Min": p.text = MC_SLIP_MIN
                if p.get("key") == "Max": p.text = MC_SLIP_MAX

def remove_embedded_sessions(root):
    for sessions_el in root.iter("Sessions"):
        for child in list(sessions_el):
            sessions_el.remove(child)

def dedup_symbols(root):
    """After unifying NORMAL/TICK/ASSET to a single symbol name, the Resources/Symbols catalog can
    end up with 2 <Symbol name="X"> entries for the same name (duplicate resource key). Keep only one."""
    for syms in root.iter("Symbols"):
        seen = set()
        for child in list(syms):
            if child.tag != "Symbol":
                continue
            name = child.get("name")
            if name in seen:
                syms.remove(child)
            else:
                seen.add(name)

def set_project_name(cfg_root, shortname):
    proj = cfg_root.find(".")
    if proj.tag == "Project":
        proj.set("name", shortname)

# ---------------------------------------------------------------- driver
ET.register_namespace("", "")

def process_edge(edge_key):
    edge = EDGES[edge_key]
    edge_dir = os.path.join(WORK, edge_key)
    if os.path.exists(edge_dir):
        shutil.rmtree(edge_dir)
    os.makedirs(edge_dir)

    for fname in TASK_FILES:
        with open(os.path.join(BASE_DIR, fname), "r", encoding="utf-8") as f:
            txt = f.read()
        txt = phase1_text(txt)
        txt = fix_symbol_tag(txt)
        txt = patch_instrumentinfo_blocks(txt)
        txt = patch_setup_swap(txt)
        txt = patch_setup_charts(txt, edge["timeframe"])
        txt = patch_setup_slippage(txt)
        txt = patch_commission_blocks(txt)
        txt = fix_databank_chain(txt, fname)

        root = ET.fromstring(txt)
        dedup_symbols(root)

        if fname == "Build-Task1.xml":
            edit_build_task(root, edge)
            remove_embedded_sessions(root)
        elif fname == "Retest-Task1.xml":
            edit_oos_task(root, edge)
            remove_embedded_sessions(root)
        elif fname == "Retest-Task3.xml":
            set_delete_failed_true(root)
            edit_mc_spread_slippage_task(root)
            remove_embedded_sessions(root)
        elif fname in ("Retest-Task2.xml","Retest-Task4.xml","Retest-Task7.xml"):
            set_delete_failed_true(root)
            remove_embedded_sessions(root)
        elif fname == "Retest-Task5.xml":
            edit_tick_task(root, edge)
            remove_embedded_sessions(root)
        elif fname == "Retest-Task6.xml":
            remove_embedded_sessions(root)

        try:
            ET.indent(root, space="  ")
        except Exception:
            pass
        out_path = os.path.join(edge_dir, fname)
        ET.ElementTree(root).write(out_path, encoding="utf-8", xml_declaration=False)

    # config.xml : copy + set project name
    with open(os.path.join(BASE_DIR, "config.xml"), "r", encoding="utf-8") as f:
        cfg_txt = f.read()
    cfg_root = ET.fromstring(cfg_txt)
    set_project_name(cfg_root, edge["shortname"])
    try:
        ET.indent(cfg_root, space="  ")
    except Exception:
        pass
    ET.ElementTree(cfg_root).write(os.path.join(edge_dir, "config.xml"), encoding="utf-8", xml_declaration=False)

    # zip into .cfx
    cfx_path = os.path.join(OUT_ROOT, f'{edge["shortname"]}.cfx')
    if os.path.exists(cfx_path):
        os.remove(cfx_path)
    with zipfile.ZipFile(cfx_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(edge_dir, "config.xml"), "config.xml")
        for fname in TASK_FILES:
            z.write(os.path.join(edge_dir, fname), fname)
    return cfx_path, dict(gmin_final=MESES_IS*edge["trades_per_month"],
                           gmin_oos=MESES_OOS*edge["trades_per_month"],
                           gmin_tick=MESES_FULL*edge["trades_per_month"])

if __name__ == "__main__":
    results = {}
    for k in EDGES:
        path, calc = process_edge(k)
        print("Built:", path)
        results[k] = calc
    with open(os.path.join(WORK, "calc_summary.json"), "w") as f:
        json.dump(dict(MESES_IS=MESES_IS, MESES_OOS=MESES_OOS, MESES_FULL=MESES_FULL,
                        BUILDER_START=BUILDER_START, OOS_START=OOS_START, NORMAL_END=NORMAL_END,
                        per_edge=results), f, indent=2)
    print("Done.")
