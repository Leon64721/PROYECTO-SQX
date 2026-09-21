#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patcher: BASE_CUSTOM_PROJECT_MASTER_CLEAN_SQX_V1_SOURCE_ONLY.cfx -> 4 edge-specific Custom Projects
for NDXm_TICK_UTCPlus02 / Tickmill - Nasdaq, per SQX_PROJECT_SKILLS_OOS_20_30_EXISTING_SESSION_SHORTNAME_SAFE package.
"""
import re, os, shutil, zipfile, json
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

BASE_DIR = "E:/PROYECTOS/CLAUDE CODE/STRATEGY QUANT"
OUT_ROOT = "E:/PROYECTOS/CLAUDE CODE/STRATEGY QUANT/patched_master_projects"
WORK = os.path.join(OUT_ROOT, "_work")

CFX_BASE_FILE = os.path.join(BASE_DIR, "07_BASE_CUSTOM_PROJECT_MASTER_CLEAN_SQX_V1_SOURCE_ONLY_FIXED.cfx")
UNZIPPED_BASE_DIR = os.path.join(WORK, "unzipped_base_cfx") # Directorio temporal para descomprimir el CFX base

TASK_FILES = ["Build-Task1.xml","Retest-Task1.xml","Retest-Task2.xml","Retest-Task3.xml",
              "Retest-Task4.xml","Retest-Task5.xml","Retest-Task6.xml","Retest-Task7.xml"]

# Diagnostic-only isolation switch (2026-08-31 incident): V2/V3 both showed "Exception in backtest:
# n must be positive, got: 0" for ~100% of MC_SPREAD_SLIPPAGE simulations, regardless of the
# RandomizeSlippage Min/Max values used. Set SQX_DIAG_MC_MODE=off_both / off_spread / off_slippage
# to isolate which randomize method (if either) is the trigger, before assuming it\'s something else
# entirely (engine/data/precision issue unrelated to these two params).
DIAG_MC_MODE = os.environ.get("SQX_DIAG_MC_MODE", "").strip().lower()

# ---------------------------------------------------------------- global identity/cost params
ASSET = "NDXm_TICK_UTCPlus02"
INSTRUMENT = "NDXm(2)"   # confirmed real Data Manager instrument id (from sibling NDXm_Qlib_OOS20.cfx), NOT the symbol name
BROKER_LABEL = "TICKMILL"
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

