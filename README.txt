╭──────────────────────────────────────────────────────────────────────────────╮
│ BBox Claudit v1.9 - Claude Code Use/Cost Auditor                            │
│ © 2026 Donald Peters | BentoBox Tools | All Rights Reserved                 │
╰──────────────────────────────────────────────────────────────────────────────╯

WHAT IS CLAUDIT?
----------------
Claudit is a comprehensive cost analysis tool for Claude Code that tracks your
AI spending across all projects with GLOBAL CURRENCY SUPPORT and a professional
colorized interface with rounded Unicode borders. It provides detailed
breakdowns by:
  - Timeframe (Daily, Weekly, Monthly, Yearly)
  - Project (see which projects cost the most)
  - Model (Sonnet, Opus, Haiku)
  - Cache Savings (how much you saved with prompt caching)
  - 100+ Currencies (with live exchange rates!)

INSTALLATION
------------
1. Copy claudit.py to: C:\Users\YourName\bin\
2. Copy claudit.cmd to: C:\Users\YourName\bin\
3. Ensure your bin folder is in your PATH

USAGE
-----
From any terminal window:

    claudit              # Default (CAD)
    claudit -c EUR       # Show costs in Euros
    claudit -c JPY       # Show costs in Japanese Yen
    claudit -c GBP       # Show costs in British Pounds
    claudit -c INR       # Show costs in Indian Rupees
    claudit -c BRL       # Show costs in Brazilian Real
    claudit -c AUD       # Show costs in Australian Dollars

MULTI-CURRENCY MAGIC
--------------------
Claudit v1.6 includes the "Global Vault" with 100+ ISO 4217 currencies:

AMERICAS: USD, CAD, MXN, BRL, ARS, CLP, COP, PEN, UYU, VES, BOB, PYG, CRC,
          GTQ, HNL, NIO, PAB, DOP, JMD, TTD, BSD, BBD, BZD, XCD

EUROPE:   EUR, GBP, CHF, SEK, NOK, DKK, PLN, CZK, HUF, RON, BGN, HRK, ISK,
          RSD, BAM, MKD, ALL, MDL, UAH, BYN, RUB, GEL, AMD, AZN

ASIA/PACIFIC: JPY, CNY, INR, AUD, NZD, HKD, SGD, KRW, TWD, THB, IDR, PHP,
              VND, MYR, BND, KHR, LAK, MMK, PKR, BDT, LKR, NPR, BTN, AFN,
              KZT, UZS, KGS, TJS, TMT, MNT

MIDDLE EAST: TRY, ILS, AED, SAR, KWD, QAR, OMR, BHD, JOD, LBP, SYP, IQD, YER

AFRICA:   ZAR, EGP, NGN, KES, GHS, TZS, UGX, MAD, TND, DZD, AOA, XOF, XAF,
          ZMW, BWP, MUR, SCR, ETB, RWF, MWK, ZWL

CRYPTO:   BTC, ETH (for fun!)

LIVE SYNC ENGINE
----------------
Claudit automatically fetches live exchange rates from api.frankfurter.dev.
If the API is offline or doesn't support your currency, it uses the April 2026
"Global Vault" fallback rates.

The report header shows you which source was used:
  🌐 LIVE SYNC - Real-time rate from API
  💾 VAULT     - Fallback rate from Global Vault

UNDERSTANDING YOUR REPORT
--------------------------
📅 COST BY TIMEFRAME (1 USD = X.XX [CURRENCY] - SOURCE)
  Shows exchange rate and source (LIVE SYNC 🌐 or VAULT 💾)
  All amounts displayed as: $X.XX USD (Y.YY CURRENCY)

📁 COST BY PROJECT
  Lists all your Claude Code projects sorted by cost (highest first).
  Projects under $0.05 are grouped into "Miscellaneous" to keep it readable.

🤖 COST BY MODEL
  Breaks down costs by Claude model (Sonnet, Opus, Haiku).

💾 PROMPT CACHING SAVINGS
  Shows how much you saved by using prompt caching. This feature can save
  70-90% on token costs!

📊 USAGE EFFICIENCY - THE ANXIETY KILLER
  Proves you only pay for active days. Idle days cost $0.00!

🔗 VERIFY ON WEB
  Direct link to your Anthropic billing dashboard.

FINAL SUMMARY BLOCK
--------------------
The bottom summary always shows (in order):
  ✅ Daily Spend:   $X.XX USD ($Y.YY CURRENCY)
  ✅ Weekly Spend:  $X.XX USD ($Y.YY CURRENCY)
  ✅ Monthly Spend: $X.XX USD ($Y.YY CURRENCY)
  ✅ Yearly Spend:  $X.XX USD ($Y.YY CURRENCY)

FEATURES
--------
✅ 100+ Currencies: Global Vault with April 2026 fallback rates
✅ Live Exchange Rates: Auto-fetches from frankfurter.dev API
✅ Multi-Currency Display: Shows both USD and your chosen currency
✅ Project Breakdown: See exactly where your credits went
✅ Cache Savings Tracker: Monitor your prompt caching savings
✅ Anxiety Killer: Shows idle days cost $0.00 (pay only when active)
✅ Direct Billing Link: One-click access to Anthropic dashboard
✅ 100% Portable: Uses expanduser('~') for cross-platform compatibility

COMMAND LINE OPTIONS
--------------------
  -c, --currency CURRENCY    ISO 4217 currency code (default: CAD)
  -h, --help                Show help message and exit

EXAMPLES
--------
# View costs in Canadian Dollars (default)
claudit

# View costs in Euros
claudit -c EUR

# View costs in Japanese Yen
claudit -c JPY

# View costs in Bitcoin (why not!)
claudit -c BTC

SUPPORT THE BUILD
-----------------
If Claudit saved you some Loonies (or Euros, or Yen...), buy a coffee:
  https://ko-fi.com/bboxtools

Your support helps maintain and improve BentoBox Tools!

TECHNICAL DETAILS
-----------------
Data Sources:
  - ~/.claude/stats-cache.json (aggregate historical data)
  - ~/.claude/history.jsonl (project activity logs)
  - ~/.claude/projects/**/*.jsonl (current session logs)

Exchange Rate API:
  - Live: api.frankfurter.dev (free, open source)
  - Fallback: Global Vault (April 2026 rates)

Pricing (2026 rates):
  Sonnet 4.5: $0.003 input, $0.015 output per 1K tokens
  Opus 4.6:   $0.015 input, $0.075 output per 1K tokens
  Haiku 4.5:  $0.0008 input, $0.004 output per 1K tokens

  Cache Read: 90% discount on input token prices
  Cache Write: 25% markup on input token prices

VERSION HISTORY
---------------
v1.9 (2026-04-02)
  - Perfect Visual Alignment with BobAI aesthetic
  - ANSI 256-color palette for exact color matching:
    * CYAN (51) - Title text
    * WHITE (255) - Subtitle text
    * GREY (244) - Copyright info
    * BOBAI_BLUE (39) - All borders and separator lines
    * GREEN (82) - Savings, checkmarks, and "Liked the audit" line
    * MAGENTA (201) - Local currency conversions
    * YELLOW (226) - Pro tips
  - Enhanced border styles (═ for main borders, ─ for separators)
  - Daily Spend confirmed as first item in summary
  - Production-ready professional interface

v1.8 (2026-04-02)
  - Professional rounded Unicode box header (╭╮╰╯─│)
  - Official branding: "Claude Code Use/Cost Auditor"
  - Updated API endpoint: frankfurter.dev/v2/latest
  - Refined Global Vault rates (CAD: 1.39, EUR: 0.87, GBP: 0.75, etc.)
  - ISO currency code labeling ($10.00 USD ($13.94 CAD))
  - Professional color hierarchy
  - Daily Spend prioritized in summary
  - Clean, production-ready interface

v1.7 (2026-04-02)
  - Colorized UI with ANSI codes
  - Cyan headers and borders
  - Magenta local currency conversions
  - Green savings and checkboxes
  - Yellow pro tips
  - White/bold USD amounts

v1.6 (2026-04-02)
  - Universal Global Build
  - 100+ currency support with Global Vault
  - Live exchange rate API integration (frankfurter.dev)
  - Smart fallback system (LIVE SYNC 🌐 or VAULT 💾)
  - Command line currency selection (-c flag)
  - Updated branding: "Buy me a Bento" Ko-fi link

v1.0 (2026-04-02)
  - Initial production release
  - Multi-project tracking
  - USD/CAD dual currency display
  - Historical data integration
  - Prompt caching savings calculator
  - Idle day cost verification

TROUBLESHOOTING
---------------
Q: "Currency 'XYZ' not supported"
A: Check the supported currencies list above. If your currency isn't listed,
   contact us at ko-fi.com/bboxtools to request it!

Q: "No session logs found"
A: Make sure you've run Claude Code at least once. The tool needs data to
   analyze.

Q: Numbers don't match the web dashboard exactly
A: Claudit uses the same pricing as Anthropic's API. Minor differences may
   occur due to rounding or if pricing changed recently. Always verify on
   the official dashboard.

Q: Exchange rates seem outdated
A: If LIVE SYNC fails, the tool uses April 2026 fallback rates. Check your
   internet connection or try again later.

LICENSE
-------
© 2026 Donald Peters | BentoBox Tools | All Rights Reserved

This software is provided "as is" for personal use. Redistribution or
commercial use requires explicit permission from the author.

CONTACT
-------
Found a bug? Have a feature request? Want to add a currency?
Support: https://ko-fi.com/bboxtools

================================================================================
  Liked the audit? Buy me a Bento: ko-fi.com/bboxtools
================================================================================
