//+------------------------------------------------------------------+
//| RapidSpreadStats_MarketWatch_V3_1_ONE_CSV_FINAL.mq5                   |
//| Market Watch spread statistics using CopyTicksRange().          |
//| Processes every visible Market Watch symbol sequentially.       |
//| Produces exactly one master CSV with one row per symbol.         |
//+------------------------------------------------------------------+
#property strict
#property version   "3.10"
#property script_show_inputs

enum ENUM_RSS_SCOPE
{
   RSS_MARKET_WATCH = 0,   // Every symbol currently visible in Market Watch
   RSS_SINGLE_SYMBOL = 1   // InpSymbol, or current chart when empty
};

input ENUM_RSS_SCOPE InpScope          = RSS_MARKET_WATCH;       // Default: all Market Watch symbols
input string   InpSymbol               = "";                    // Used only in single-symbol mode
input datetime InpStartDate            = D'2024.01.01 00:00';    // Start date
input datetime InpEndDate              = D'2026.05.26 23:59';    // End date
input int      InpBatchDays            = 7;                      // Ticks copied in chunks of N days
input int      InpProcessEveryNTicks   = 1;                      // 1=all ticks, 10/100=faster sample
input int      InpPercentileSampleStep = 100;                    // Store first, every N, and final valid tick
input int      InpMinValidTicks        = 10000;                  // Minimum valid ticks for recommendations
input int      InpMinPercentileSamples = 1000;                   // Minimum samples for recommendations
input double   InpMinHistoryCoveragePct= 90.0;                   // Minimum first-to-last coverage of requested span
input double   InpMaxStartGapDays      = 14.0;                   // Maximum gap from requested start to first valid tick
input double   InpMaxEndGapDays        = 7.0;                    // Maximum gap from last valid tick to requested end
input int      InpMaxSymbols           = 0;                      // 0=all visible symbols; positive value limits run
input string   InpOutputPrefix         = "RapidSpreadStats";     // Output prefix

double g_sum_pips = 0.0;
double g_min_pips = DBL_MAX;
double g_max_pips = 0.0;
ulong  g_raw_ticks = 0;
ulong  g_processed_ticks = 0;
ulong  g_used_ticks = 0;
ulong  g_bad_ticks = 0;
ulong  g_invalid_price_ticks = 0;
ulong  g_crossed_market_ticks = 0;
ulong  g_nonfinite_ticks = 0;
ulong  g_zero_spread_ticks = 0;
ulong  g_positive_spread_ticks = 0;
ulong  g_misaligned_spread_ticks = 0;

ulong  g_batch_count = 0;
ulong  g_failed_batch_count = 0;
ulong  g_empty_batch_count = 0;
bool   g_stopped_early = false;

long   g_first_tick_time_msc = 0;
long   g_last_tick_time_msc = 0;
double g_last_valid_spread_pips = 0.0;
bool   g_last_valid_spread_sampled = false;

double g_samples[];
int    g_sample_count = 0;

string g_symbol = "";

int    g_master_handle = INVALID_HANDLE;
string g_master_file = "";
int    g_symbols_requested = 0;
int    g_symbols_processed = 0;
int    g_symbols_pass = 0;
int    g_symbols_blocked = 0;
int    g_symbols_skipped = 0;

double g_point_size = 0.0;
double g_trade_tick_size = 0.0;
double g_sqx_pip_size = 0.0;
int    g_digits = 0;
int    g_calc_mode = 0;

bool IsForexCalcMode(const int calc_mode)
{
   return calc_mode == SYMBOL_CALC_MODE_FOREX || calc_mode == SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE;
}

double SQXPipSize(const string symbol)
{
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   double trade_tick = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);
   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   int calc_mode = (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_CALC_MODE);

   if(point <= 0) return 0;
   if(trade_tick <= 0) trade_tick = point;

   if(IsForexCalcMode(calc_mode))
      return point * ((digits == 3 || digits == 5) ? 10.0 : 1.0);

   // For CFDs, indexes, metals, commodities and futures, one SQX pip is one
   // negotiated trade tick, not one display point inferred from digits.
   return trade_tick;
}

double PipInPoints(const string symbol)
{
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   double pip_size = SQXPipSize(symbol);
   if(point <= 0 || pip_size <= 0) return 0;
   return pip_size / point;
}

string CleanFilePart(string s)
{
   StringReplace(s, ":", "-");
   StringReplace(s, ".", "_");
   StringReplace(s, "/", "_");
   StringReplace(s, "\\", "_");
   StringReplace(s, " ", "_");
   return s;
}

void AddSample(const double value)
{
   if(g_sample_count >= ArraySize(g_samples))
      ArrayResize(g_samples, ArraySize(g_samples) + 10000);

   g_samples[g_sample_count] = value;
   g_sample_count++;
}

double Percentile(double &arr[], const int n, const double pct)
{
   if(n <= 0) return 0.0;

   double rank = (pct / 100.0) * (double)(n - 1);
   int lo = (int)MathFloor(rank);
   int hi = (int)MathCeil(rank);

   if(lo < 0) lo = 0;
   if(hi < 0) hi = 0;
   if(lo >= n) lo = n - 1;
   if(hi >= n) hi = n - 1;

   if(lo == hi) return arr[lo];

   double weight = rank - (double)lo;
   return arr[lo] * (1.0 - weight) + arr[hi] * weight;
}

void ResetSymbolState()
{
   g_sum_pips = 0.0;
   g_min_pips = DBL_MAX;
   g_max_pips = 0.0;

   g_raw_ticks = 0;
   g_processed_ticks = 0;
   g_used_ticks = 0;
   g_bad_ticks = 0;
   g_invalid_price_ticks = 0;
   g_crossed_market_ticks = 0;
   g_nonfinite_ticks = 0;
   g_zero_spread_ticks = 0;
   g_positive_spread_ticks = 0;
   g_misaligned_spread_ticks = 0;

   g_batch_count = 0;
   g_failed_batch_count = 0;
   g_empty_batch_count = 0;
   g_stopped_early = false;

   g_first_tick_time_msc = 0;
   g_last_tick_time_msc = 0;
   g_last_valid_spread_pips = 0.0;
   g_last_valid_spread_sampled = false;

   g_sample_count = 0;
   ArrayResize(g_samples, 0);

   g_symbol = "";
   g_point_size = 0.0;
   g_trade_tick_size = 0.0;
   g_sqx_pip_size = 0.0;
   g_digits = 0;
   g_calc_mode = 0;
}
//+------------------------------------------------------------------+
bool OpenMasterFile()
{
   string start_part = CleanFilePart(TimeToString(InpStartDate, TIME_DATE | TIME_SECONDS));
   string end_part = CleanFilePart(TimeToString(InpEndDate, TIME_DATE | TIME_SECONDS));
   string scope_part = (InpScope == RSS_MARKET_WATCH ? "MarketWatch" : "SingleSymbol");

   g_master_file =
      InpOutputPrefix + "_" + scope_part + "_" + start_part + "_to_" + end_part + "_ONE_FILE.csv";

   g_master_handle = FileOpen(
      g_master_file,
      FILE_WRITE | FILE_CSV | FILE_ANSI,
      ';'
   );

   if(g_master_handle == INVALID_HANDLE)
   {
      Print("Could not open master output file. Error: ", GetLastError());
      return false;
   }

   FileWrite(
      g_master_handle,
      "schema_version",
      "scope",
      "symbol",
      "validation_status",
      "recommendation_status",
      "data_complete",
      "transport_complete",
      "history_coverage_status",
      "history_coverage_ok",
      "stopped_early",
      "start_date",
      "end_date",
      "first_valid_tick_time",
      "last_valid_tick_time",
      "requested_span_days",
      "observed_span_days",
      "history_coverage_percent",
      "start_gap_days",
      "end_gap_days",
      "digits",
      "trade_calc_mode",
      "point_size",
      "trade_tick_size",
      "sqx_pip_size",
      "pip_in_points",
      "copy_batch_count",
      "copy_batch_failure_count",
      "empty_batch_count",
      "empty_batch_percent",
      "raw_tick_count_read",
      "processed_tick_count_attempted",
      "tick_count_used_for_average",
      "bad_tick_count_skipped",
      "bad_tick_percent",
      "zero_spread_tick_count",
      "zero_spread_tick_percent",
      "misaligned_spread_tick_count",
      "misaligned_spread_tick_percent",
      "percentile_sample_count",
      "avg_spread_pips",
      "min_spread_pips",
      "max_spread_pips",
      "p50_spread_pips",
      "p75_spread_pips",
      "p90_spread_pips",
      "p95_spread_pips",
      "p99_spread_pips",
      "suggested_builder_raw_spread_pips",
      "suggested_builder_soft_spread_pips",
      "suggested_cost_lock_spread_pips",
      "suggested_mc_spread_min_pips",
      "suggested_mc_spread_max_pips",
      "note"
   );

   return true;
}
//+------------------------------------------------------------------+
void WriteMasterFailure(string symbol, string status, string note)
{
   if(g_master_handle == INVALID_HANDLE)
      return;

   FileWrite(
      g_master_handle,
      "3.1_FINAL",
      (InpScope == RSS_MARKET_WATCH ? "MARKET_WATCH" : "SINGLE_SYMBOL"),
      symbol,
      status,
      "BLOCKED_" + status,
      "false",
      "false",
      "NOT_EVALUATED",
      "false",
      "false",
      TimeToString(InpStartDate, TIME_DATE | TIME_SECONDS),
      TimeToString(InpEndDate, TIME_DATE | TIME_SECONDS),
      "NA",
      "NA",
      DoubleToString((double)(InpEndDate - InpStartDate) / 86400.0, 6),
      "0.000000",
      "0.000000",
      "0.000000",
      "0.000000",
      "0",
      "0",
      "0.000000000000",
      "0.000000000000",
      "0.000000000000",
      "0.00000000",
      "0",
      "0",
      "0",
      "0.00000000",
      "0",
      "0",
      "0",
      "0",
      "0.00000000",
      "0",
      "0.00000000",
      "0",
      "0.00000000",
      "0",
      "0.000000",
      "0.000000",
      "0.000000",
      "0.000000",
      "0.000000",
      "0.000000",
      "0.000000",
      "0.000000",
      "0.000000",
      "0.000000",
      "0.000000",
      "0.000000",
      "0.000000",
      note
   );
}
//+------------------------------------------------------------------+
void ProcessSpread(const MqlTick &tick)
{
   g_processed_ticks++;

   if(!MathIsValidNumber(tick.bid) || !MathIsValidNumber(tick.ask))
   {
      g_bad_ticks++;
      g_nonfinite_ticks++;
      return;
   }

   if(tick.bid <= 0.0 || tick.ask <= 0.0)
   {
      g_bad_ticks++;
      g_invalid_price_ticks++;
      return;
   }

   if(tick.ask < tick.bid)
   {
      g_bad_ticks++;
      g_crossed_market_ticks++;
      return;
   }

   double spread_price = tick.ask - tick.bid;
   double spread_sqx_pips = spread_price / g_sqx_pip_size;

   if(!MathIsValidNumber(spread_price) ||
      !MathIsValidNumber(spread_sqx_pips) ||
      spread_price < 0.0 ||
      spread_sqx_pips < 0.0)
   {
      g_bad_ticks++;
      g_nonfinite_ticks++;
      return;
   }

   g_used_ticks++;
   g_sum_pips += spread_sqx_pips;

   if(spread_sqx_pips < g_min_pips) g_min_pips = spread_sqx_pips;
   if(spread_sqx_pips > g_max_pips) g_max_pips = spread_sqx_pips;

   double zero_tolerance = g_point_size * 0.000000001;
   if(spread_price <= zero_tolerance)
      g_zero_spread_ticks++;
   else
      g_positive_spread_ticks++;

   double spread_trade_ticks = spread_price / g_trade_tick_size;
   double nearest_trade_ticks = MathRound(spread_trade_ticks);
   if(MathAbs(spread_trade_ticks - nearest_trade_ticks) > 0.000001)
      g_misaligned_spread_ticks++;

   long tick_time_msc = tick.time_msc;
   if(tick_time_msc <= 0)
      tick_time_msc = (long)tick.time * 1000;

   if(g_first_tick_time_msc == 0 || tick_time_msc < g_first_tick_time_msc)
      g_first_tick_time_msc = tick_time_msc;
   if(tick_time_msc > g_last_tick_time_msc)
      g_last_tick_time_msc = tick_time_msc;

   g_last_valid_spread_pips = spread_sqx_pips;

   int pct_step = MathMax(1, InpPercentileSampleStep);
   bool sample_now =
      (g_used_ticks == 1 || (g_used_ticks % (ulong)pct_step) == 0);

   if(sample_now)
   {
      AddSample(spread_sqx_pips);
      g_last_valid_spread_sampled = true;
   }
   else
   {
      g_last_valid_spread_sampled = false;
   }
}

void WriteSummary()
{
   // Preserve both temporal endpoints in the percentile sample.
   if(g_used_ticks > 1 && !g_last_valid_spread_sampled)
      AddSample(g_last_valid_spread_pips);

   double avg = (g_used_ticks > 0 ? g_sum_pips / (double)g_used_ticks : 0.0);
   double zero_spread_pct =
      (g_used_ticks > 0 ? 100.0 * (double)g_zero_spread_ticks / (double)g_used_ticks : 0.0);
   double bad_tick_pct =
      (g_processed_ticks > 0 ? 100.0 * (double)g_bad_ticks / (double)g_processed_ticks : 0.0);
   double misaligned_spread_pct =
      (g_used_ticks > 0 ? 100.0 * (double)g_misaligned_spread_ticks / (double)g_used_ticks : 0.0);
   double sample_coverage_pct =
      (g_used_ticks > 0 ? 100.0 * (double)g_sample_count / (double)g_used_ticks : 0.0);
   double empty_batch_pct =
      (g_batch_count > 0 ? 100.0 * (double)g_empty_batch_count / (double)g_batch_count : 0.0);

   double requested_span_days =
      MathMax(0.0, (double)(InpEndDate - InpStartDate) / 86400.0);

   double observed_span_days = 0.0;
   double start_gap_days = requested_span_days;
   double end_gap_days = requested_span_days;

   if(g_first_tick_time_msc > 0 && g_last_tick_time_msc >= g_first_tick_time_msc)
   {
      observed_span_days =
         (double)(g_last_tick_time_msc - g_first_tick_time_msc) / 86400000.0;

      start_gap_days =
         MathMax(0.0,
                 ((double)g_first_tick_time_msc / 1000.0 - (double)InpStartDate)
                 / 86400.0);

      end_gap_days =
         MathMax(0.0,
                 ((double)InpEndDate - (double)g_last_tick_time_msc / 1000.0)
                 / 86400.0);
   }

   double history_coverage_pct =
      (requested_span_days > 0.0
       ? MathMin(100.0, 100.0 * observed_span_days / requested_span_days)
       : 0.0);

   bool enough_ticks =
      (g_used_ticks >= (ulong)MathMax(1, InpMinValidTicks));
   bool enough_samples =
      (g_sample_count >= MathMax(1, InpMinPercentileSamples));

   bool start_coverage_ok =
      (start_gap_days <= MathMax(0.0, InpMaxStartGapDays));
   bool end_coverage_ok =
      (end_gap_days <= MathMax(0.0, InpMaxEndGapDays));
   bool span_coverage_ok =
      (history_coverage_pct >= MathMax(0.0, MathMin(100.0, InpMinHistoryCoveragePct)));

   bool history_coverage_ok =
      (g_used_ticks > 0 &&
       start_coverage_ok &&
       end_coverage_ok &&
       span_coverage_ok);

   bool transport_complete =
      (g_failed_batch_count == 0 && !g_stopped_early);

   bool data_complete =
      (transport_complete && history_coverage_ok);

   string history_coverage_status =
      (history_coverage_ok ? "PASS" : "PARTIAL_HISTORY");

   string validation_status = "PASS";
   if(g_used_ticks == 0)
      validation_status = "NO_VALID_TICKS";
   else if(!transport_complete)
      validation_status = "INCOMPLETE_DATA";
   else if(!history_coverage_ok)
      validation_status = "PARTIAL_HISTORY";
   else if(!enough_ticks || !enough_samples)
      validation_status = "INSUFFICIENT_EVIDENCE";

   string recommendation_status =
      (validation_status == "PASS" ? "AVAILABLE" : "BLOCKED_" + validation_status);

   double p50 = 0.0, p75 = 0.0, p90 = 0.0, p95 = 0.0, p99 = 0.0;

   if(g_sample_count > 0)
   {
      ArrayResize(g_samples, g_sample_count);
      ArraySort(g_samples);
      p50 = Percentile(g_samples, g_sample_count, 50.0);
      p75 = Percentile(g_samples, g_sample_count, 75.0);
      p90 = Percentile(g_samples, g_sample_count, 90.0);
      p95 = Percentile(g_samples, g_sample_count, 95.0);
      p99 = Percentile(g_samples, g_sample_count, 99.0);
   }

   // V3.1 writes only to the master CSV. No per-symbol files are created.
   int h = INVALID_HANDLE;


   if(g_master_handle != INVALID_HANDLE)
   {
      FileWrite(
         g_master_handle,
         "3.1_FINAL",
         (InpScope == RSS_MARKET_WATCH ? "MARKET_WATCH" : "SINGLE_SYMBOL"),
         g_symbol,
         validation_status,
         recommendation_status,
         (data_complete ? "true" : "false"),
         (transport_complete ? "true" : "false"),
         history_coverage_status,
         (history_coverage_ok ? "true" : "false"),
         (g_stopped_early ? "true" : "false"),
         TimeToString(InpStartDate, TIME_DATE | TIME_SECONDS),
         TimeToString(InpEndDate, TIME_DATE | TIME_SECONDS),
         (g_first_tick_time_msc > 0
          ? TimeToString((datetime)(g_first_tick_time_msc / 1000), TIME_DATE | TIME_SECONDS)
          : "NA"),
         (g_last_tick_time_msc > 0
          ? TimeToString((datetime)(g_last_tick_time_msc / 1000), TIME_DATE | TIME_SECONDS)
          : "NA"),
         DoubleToString(requested_span_days, 6),
         DoubleToString(observed_span_days, 6),
         DoubleToString(history_coverage_pct, 6),
         DoubleToString(start_gap_days, 6),
         DoubleToString(end_gap_days, 6),
         IntegerToString(g_digits),
         IntegerToString(g_calc_mode),
         DoubleToString(g_point_size, 12),
         DoubleToString(g_trade_tick_size, 12),
         DoubleToString(g_sqx_pip_size, 12),
         DoubleToString(PipInPoints(g_symbol), 8),
         IntegerToString((long)g_batch_count),
         IntegerToString((long)g_failed_batch_count),
         IntegerToString((long)g_empty_batch_count),
         DoubleToString(empty_batch_pct, 8),
         IntegerToString((long)g_raw_ticks),
         IntegerToString((long)g_processed_ticks),
         IntegerToString((long)g_used_ticks),
         IntegerToString((long)g_bad_ticks),
         DoubleToString(bad_tick_pct, 8),
         IntegerToString((long)g_zero_spread_ticks),
         DoubleToString(zero_spread_pct, 8),
         IntegerToString((long)g_misaligned_spread_ticks),
         DoubleToString(misaligned_spread_pct, 8),
         IntegerToString(g_sample_count),
         DoubleToString(avg, 6),
         DoubleToString(g_min_pips == DBL_MAX ? 0.0 : g_min_pips, 6),
         DoubleToString(g_max_pips, 6),
         DoubleToString(p50, 6),
         DoubleToString(p75, 6),
         DoubleToString(p90, 6),
         DoubleToString(p95, 6),
         DoubleToString(p99, 6),
         DoubleToString(p50, 6),
         DoubleToString(p75, 6),
         DoubleToString(p95, 6),
         DoubleToString(p95, 6),
         DoubleToString(p99, 6),
         ""
      );
   }

   g_symbols_processed++;
   if(validation_status == "PASS")
      g_symbols_pass++;
   else
      g_symbols_blocked++;

   Print("RapidSpreadStats completed for ", g_symbol,
         " | validation_status=", validation_status,
         " | recommendation_status=", recommendation_status,
         " | history_coverage=", DoubleToString(history_coverage_pct, 2), "%",
         " | start_gap_days=", DoubleToString(start_gap_days, 2),
         " | end_gap_days=", DoubleToString(end_gap_days, 2));
   Print("Avg=", DoubleToString(avg, 4),
         " P50=", DoubleToString(p50, 4),
         " P75=", DoubleToString(p75, 4),
         " P90=", DoubleToString(p90, 4),
         " P95=", DoubleToString(p95, 4),
         " P99=", DoubleToString(p99, 4));
}

bool ProcessOneSymbol(string symbol, int ordinal, int total)
{
   ResetSymbolState();
   g_symbol = symbol;

   if(!SymbolSelect(g_symbol, true))
   {
      string note = "SymbolSelect failed, error=" + IntegerToString(GetLastError());
      Print("Could not select symbol: ", g_symbol, " ", note);
      WriteMasterFailure(g_symbol, "SYMBOL_SELECT_FAILED", note);
      g_symbols_skipped++;
      return false;
   }

   g_digits = (int)SymbolInfoInteger(g_symbol, SYMBOL_DIGITS);
   g_calc_mode = (int)SymbolInfoInteger(g_symbol, SYMBOL_TRADE_CALC_MODE);
   g_point_size = SymbolInfoDouble(g_symbol, SYMBOL_POINT);
   g_trade_tick_size = SymbolInfoDouble(g_symbol, SYMBOL_TRADE_TICK_SIZE);
   if(g_trade_tick_size <= 0.0)
      g_trade_tick_size = g_point_size;

   g_sqx_pip_size = SQXPipSize(g_symbol);

   if(g_point_size <= 0.0 || g_trade_tick_size <= 0.0 || g_sqx_pip_size <= 0.0)
   {
      string note =
         "Invalid dimensions: point=" + DoubleToString(g_point_size, 12) +
         ", trade_tick=" + DoubleToString(g_trade_tick_size, 12) +
         ", sqx_pip=" + DoubleToString(g_sqx_pip_size, 12);

      Print("[", ordinal, "/", total, "] ", g_symbol, " ", note);
      WriteMasterFailure(g_symbol, "INVALID_SYMBOL_DIMENSIONS", note);
      g_symbols_skipped++;
      return false;
   }

   int process_step = InpProcessEveryNTicks;
   if(process_step < 1)
      process_step = 1;

   int batch_days = InpBatchDays;
   if(batch_days < 1)
      batch_days = 1;

   Print("[", ordinal, "/", total, "] RapidSpreadStats started for ", g_symbol,
         " | ", TimeToString(InpStartDate, TIME_DATE | TIME_SECONDS),
         " -> ", TimeToString(InpEndDate, TIME_DATE | TIME_SECONDS),
         " | process step=", process_step);

   ulong current_from_msc = (ulong)InpStartDate * 1000;
   ulong final_to_msc = (ulong)InpEndDate * 1000 + 999;
   ulong batch_span_msc = (ulong)batch_days * 86400 * 1000;

   while(current_from_msc <= final_to_msc && !IsStopped())
   {
      g_batch_count++;

      ulong batch_to_msc = current_from_msc + batch_span_msc - 1;
      if(batch_to_msc > final_to_msc)
         batch_to_msc = final_to_msc;

      MqlTick ticks[];
      int copied = CopyTicksRange(
         g_symbol,
         ticks,
         COPY_TICKS_INFO,
         current_from_msc,
         batch_to_msc
      );

      datetime batch_start = (datetime)(current_from_msc / 1000);
      datetime batch_end = (datetime)(batch_to_msc / 1000);

      if(copied < 0)
      {
         g_failed_batch_count++;
         Print("[", g_symbol, "] CopyTicksRange failed: ",
               TimeToString(batch_start, TIME_DATE | TIME_SECONDS),
               " -> ",
               TimeToString(batch_end, TIME_DATE | TIME_SECONDS),
               " Error: ", GetLastError());
      }
      else
      {
         if(copied == 0)
            g_empty_batch_count++;

         g_raw_ticks += (ulong)copied;

         for(int i = 0; i < copied; i += process_step)
            ProcessSpread(ticks[i]);
      }

      if(batch_to_msc == final_to_msc)
         break;

      current_from_msc = batch_to_msc + 1;
   }

   if(IsStopped() && current_from_msc <= final_to_msc)
      g_stopped_early = true;

   WriteSummary();
   return true;
}
//+------------------------------------------------------------------+
void OnStart()
{
   if(InpEndDate <= InpStartDate)
   {
      Print("End date must be greater than start date.");
      return;
   }

   if(!OpenMasterFile())
      return;

   if(InpScope == RSS_SINGLE_SYMBOL)
   {
      string symbol = InpSymbol;
      if(symbol == "")
         symbol = _Symbol;

      g_symbols_requested = 1;
      ProcessOneSymbol(symbol, 1, 1);
   }
   else
   {
      int visible_total = SymbolsTotal(true);
      int run_total = visible_total;

      if(InpMaxSymbols > 0 && InpMaxSymbols < run_total)
         run_total = InpMaxSymbols;

      g_symbols_requested = run_total;

      if(run_total <= 0)
      {
         Print("No visible symbols found in Market Watch.");
      }
      else
      {
         Print("Market Watch run started. Visible symbols=", visible_total,
               " | symbols to process=", run_total);

         for(int i = 0; i < run_total; i++)
         {
            if(IsStopped())
               break;

            string symbol = SymbolName(i, true);
            if(symbol == "")
            {
               WriteMasterFailure("", "EMPTY_SYMBOL_NAME",
                                  "SymbolName returned an empty value at index " +
                                  IntegerToString(i));
               g_symbols_skipped++;
               continue;
            }

            ProcessOneSymbol(symbol, i + 1, run_total);
         }
      }
   }

   if(g_master_handle != INVALID_HANDLE)
   {
      FileClose(g_master_handle);
      g_master_handle = INVALID_HANDLE;
   }

   Print("RapidSpreadStats Market Watch run finished.",
         " requested=", g_symbols_requested,
         " processed=", g_symbols_processed,
         " pass=", g_symbols_pass,
         " blocked=", g_symbols_blocked,
         " skipped=", g_symbols_skipped,
         " master_file=MQL5/Files/", g_master_file);
}
//+------------------------------------------------------------------+
