#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╭──────────────────────────────────────────────────────────────────────────────╮
│ BBox Claudit v1.9 - Claude Code Use/Cost Auditor                            │
│ © 2026 Donald Peters | BentoBox Tools | All Rights Reserved                 │
╰──────────────────────────────────────────────────────────────────────────────╯

Comprehensive cost analysis across all your Claude Code sessions.
Supports 100+ currencies with live exchange rates and offline fallback.
Professional BobAI-matched interface with perfect visual alignment.

Liked the audit? Buy me a Bento: ko-fi.com/bboxtools
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import subprocess

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# BobAI Color Palette - ANSI 256-Color Codes (Exact Match)
class Colors:
    """BobAI-matched color codes for terminal output."""
    CYAN = '\033[38;5;51m'         # Title (BBox Claudit v1.9)
    WHITE = '\033[38;5;255m'       # Subtitle (Claude Code Use/Cost Auditor)
    GREY = '\033[38;5;244m'        # Copyright info
    BOBAI_BLUE = '\033[38;5;39m'   # All borders and horizontal lines
    GREEN = '\033[38;5;82m'        # Liked the audit & savings
    MAGENTA = '\033[38;5;201m'     # Local currency conversions
    YELLOW = '\033[38;5;226m'      # Pro Tips
    BOLD = '\033[1m'               # Bold text
    WHITE_BOLD = '\033[1;97m'      # USD amounts (white + bold)
    RESET = '\033[0m'              # Reset to default

    @staticmethod
    def disable():
        """Disable colors for non-ANSI terminals."""
        Colors.CYAN = ''
        Colors.WHITE = ''
        Colors.GREY = ''
        Colors.BOBAI_BLUE = ''
        Colors.MAGENTA = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.BOLD = ''
        Colors.WHITE_BOLD = ''
        Colors.RESET = ''

# Disable colors on Windows without ANSI support (older terminals)
if sys.platform == 'win32':
    try:
        # Try to enable ANSI colors on Windows 10+
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass  # If it fails, colors will still work on modern terminals

# Claude API Pricing (2026 rates)
# Source: https://www.anthropic.com/pricing
PRICING = {
    'claude-sonnet-4-5': {
        'input': 0.003,
        'output': 0.015,
        'cache_write': 0.00375,
        'cache_read': 0.0003,
    },
    'claude-opus-4-6': {
        'input': 0.015,
        'output': 0.075,
        'cache_write': 0.01875,
        'cache_read': 0.0015,
    },
    'claude-haiku-4-5': {
        'input': 0.0008,
        'output': 0.004,
        'cache_write': 0.001,
        'cache_read': 0.00008,
    },
}

# Global Vault: Official April 2026 Fallback Exchange Rates (1 USD = X units)
CURRENCY_VAULT = {
    # Americas
    'USD': 1.0,
    'CAD': 1.39,
    'MXN': 18.02,
    'BRL': 5.25,
    'ARS': 1393.56,
    'CLP': 932.37,
    'COP': 3667.32,
    'PEN': 3.50,
    'UYU': 42.15,
    'VES': 68.50,
    'BOB': 6.91,
    'PYG': 7345.0,
    'CRC': 517.28,
    'GTQ': 7.83,
    'HNL': 24.68,
    'NIO': 36.75,
    'PAB': 1.0,
    'DOP': 60.23,
    'JMD': 158.92,
    'TTD': 6.79,
    'BSD': 1.0,
    'BBD': 2.0,
    'BZD': 2.0,
    'XCD': 2.70,  # East Caribbean Dollar

    # Europe
    'EUR': 0.87,
    'GBP': 0.75,
    'CHF': 0.800,
    'SEK': 9.56,
    'NOK': 9.74,
    'DKK': 6.52,
    'PLN': 3.74,
    'CZK': 21.43,
    'HUF': 339.09,
    'RON': 4.33,
    'BGN': 1.71,
    'HRK': 6.58,
    'ISK': 127.45,
    'RSD': 102.34,
    'BAM': 1.71,
    'MKD': 53.67,
    'ALL': 89.23,
    'MDL': 17.42,
    'UAH': 41.23,
    'BYN': 3.27,
    'RUB': 92.34,
    'GEL': 2.67,
    'AMD': 398.45,
    'AZN': 1.70,

    # Asia/Pacific
    'JPY': 159.8,
    'CNY': 6.9,
    'INR': 94.34,
    'AUD': 1.46,
    'NZD': 1.75,
    'HKD': 7.84,
    'SGD': 1.29,
    'KRW': 1519.58,
    'TWD': 32.05,
    'THB': 32.86,
    'IDR': 16987.0,
    'PHP': 60.77,
    'VND': 26330.0,
    'MYR': 4.15,
    'BND': 1.29,
    'KHR': 4098.0,
    'LAK': 22567.0,
    'MMK': 2098.0,
    'PKR': 278.56,
    'BDT': 119.87,
    'LKR': 298.45,
    'NPR': 151.02,
    'BTN': 94.34,
    'AFN': 70.23,
    'KZT': 523.67,
    'UZS': 12845.0,
    'KGS': 87.92,
    'TJS': 10.67,
    'TMT': 3.50,
    'MNT': 3456.0,

    # Middle East
    'TRY': 44.48,
    'ILS': 3.17,
    'AED': 3.67,
    'SAR': 3.75,
    'KWD': 0.31,
    'QAR': 3.64,
    'OMR': 0.385,
    'BHD': 0.377,
    'JOD': 0.709,
    'LBP': 89500.0,
    'SYP': 13002.0,
    'IQD': 1310.0,
    'YER': 250.45,

    # Africa
    'ZAR': 17.21,
    'EGP': 54.53,
    'NGN': 1678.92,
    'KES': 129.45,
    'GHS': 16.23,
    'TZS': 2678.0,
    'UGX': 3689.0,
    'MAD': 9.23,
    'TND': 2.98,
    'DZD': 127.34,
    'AOA': 923.45,
    'XOF': 572.67,  # West African CFA
    'XAF': 572.67,  # Central African CFA
    'ZMW': 27.45,
    'BWP': 12.67,
    'MUR': 43.21,
    'SCR': 13.92,
    'ETB': 123.45,
    'RWF': 1389.0,
    'MWK': 1834.0,
    'ZWL': 13.45,

    # Cryptocurrencies (for fun)
    'BTC': 0.000014,  # ~$71,000 per BTC
    'ETH': 0.00029,   # ~$3,450 per ETH
}


def get_claude_dir():
    """Get Claude data directory using portable path expansion."""
    home = os.path.expanduser('~')
    return Path(home) / '.claude'


def fetch_live_rate(currency_code):
    """Fetch live exchange rate from Frankfurter API (v2)."""
    try:
        import urllib.request
        import urllib.error

        # Try v2 endpoint first (as specified), fallback to v1 if needed
        urls = [
            f'https://api.frankfurter.dev/v2/latest?base=USD&symbols={currency_code}',
            f'https://api.frankfurter.dev/latest?base=USD&symbols={currency_code}'
        ]

        for url in urls:
            try:
                with urllib.request.urlopen(url, timeout=3) as response:
                    data = json.loads(response.read().decode())
                    rate = data.get('rates', {}).get(currency_code)
                    if rate:
                        return rate, 'LIVE'
            except:
                continue
    except:
        pass

    return None, None


def get_exchange_rate(currency_code):
    """Get exchange rate with live sync fallback to vault."""
    currency_code = currency_code.upper()

    # USD is always 1.0
    if currency_code == 'USD':
        return 1.0, 'BASE'

    # Try live API first
    live_rate, source = fetch_live_rate(currency_code)
    if live_rate:
        return live_rate, source

    # Fallback to vault
    vault_rate = CURRENCY_VAULT.get(currency_code)
    if vault_rate:
        return vault_rate, 'VAULT'

    # Currency not supported
    return None, None


def get_model_key(model_name):
    """Normalize model name to pricing key."""
    if not model_name:
        return 'claude-sonnet-4-5'
    model_lower = model_name.lower()
    if 'sonnet' in model_lower:
        return 'claude-sonnet-4-5'
    elif 'opus' in model_lower:
        return 'claude-opus-4-6'
    elif 'haiku' in model_lower:
        return 'claude-haiku-4-5'
    return 'claude-sonnet-4-5'


def calculate_cost_and_savings(usage, model_name):
    """Calculate cost and cache savings from usage data.
    Handles both snake_case (from JSONL) and camelCase (from stats-cache.json).
    """
    model_key = get_model_key(model_name)
    pricing = PRICING.get(model_key, PRICING['claude-sonnet-4-5'])

    cost = 0.0
    cache_savings = 0.0

    # Input tokens (handle both formats)
    input_tokens = usage.get('input_tokens', usage.get('inputTokens', 0))
    cost += (input_tokens / 1000) * pricing['input']

    # Output tokens (handle both formats)
    output_tokens = usage.get('output_tokens', usage.get('outputTokens', 0))
    cost += (output_tokens / 1000) * pricing['output']

    # Cache writes (cost) (handle both formats)
    cache_write = usage.get('cache_creation_input_tokens',
                           usage.get('cacheCreationInputTokens', 0))
    cost += (cache_write / 1000) * pricing['cache_write']

    # Cache reads (cost + savings calculation) (handle both formats)
    cache_read = usage.get('cache_read_input_tokens',
                          usage.get('cacheReadInputTokens', 0))
    cost += (cache_read / 1000) * pricing['cache_read']

    # Savings: what we would have paid without cache
    if cache_read > 0:
        full_price = (cache_read / 1000) * pricing['input']
        cache_price = (cache_read / 1000) * pricing['cache_read']
        cache_savings = full_price - cache_price

    return cost, cache_savings


def normalize_project_name(project_path):
    """Normalize project name for consistent grouping."""
    if not project_path:
        return 'Unknown'

    # Remove user-specific paths for portability
    home = os.path.expanduser('~')
    name = project_path.replace(home, '~')
    name = name.replace('C:\\Users\\', '')
    name = name.replace('C:\\', '')
    name = name.replace('/Users/', '')

    # Normalize separators to spaces
    name = name.replace('\\', ' ')
    name = name.replace('/', ' ')

    # Clean up multiple spaces
    name = ' '.join(name.split())

    return name


def parse_history_by_project():
    """Parse history.jsonl to get project activity counts."""
    claude_dir = get_claude_dir()
    history_file = claude_dir / 'history.jsonl'

    project_activity = defaultdict(int)

    if not history_file.exists():
        return project_activity

    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    project = entry.get('project', '')
                    if project:
                        project_name = normalize_project_name(project)
                        project_activity[project_name] += 1
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"Warning: Could not parse history.jsonl: {e}", file=sys.stderr)

    return project_activity


def parse_stats_cache():
    """Parse historical stats from stats-cache.json and attribute to projects."""
    claude_dir = get_claude_dir()
    stats_file = claude_dir / 'stats-cache.json'

    historical_data = {
        'cost': 0.0,
        'cache_savings': 0.0,
        'first_date': None,
        'daily_costs': {},
        'total_messages': 0,
        'projects': {},  # Cost per project
    }

    if not stats_file.exists():
        return historical_data

    try:
        with open(stats_file, 'r', encoding='utf-8') as f:
            stats = json.load(f)

        # Get model usage aggregates
        model_usage = stats.get('modelUsage', {})

        for model_name, usage in model_usage.items():
            cost, savings = calculate_cost_and_savings(usage, model_name)
            historical_data['cost'] += cost
            historical_data['cache_savings'] += savings

        # Get first session date
        first_session_str = stats.get('firstSessionDate')
        if first_session_str:
            historical_data['first_date'] = datetime.fromisoformat(first_session_str.replace('Z', '+00:00')).replace(tzinfo=None)

        # Get daily activity (approximate costs by token distribution)
        daily_activity = stats.get('dailyActivity', [])
        total_messages = sum(day.get('messageCount', 0) for day in daily_activity)
        historical_data['total_messages'] = total_messages

        # Distribute cost proportionally by message count
        if total_messages > 0 and historical_data['cost'] > 0:
            for day in daily_activity:
                date = day.get('date')
                msg_count = day.get('messageCount', 0)
                day_cost = (msg_count / total_messages) * historical_data['cost']
                historical_data['daily_costs'][date] = day_cost

        # Now attribute costs to projects based on history.jsonl
        project_activity = parse_history_by_project()
        total_activity = sum(project_activity.values())

        if total_activity > 0 and historical_data['cost'] > 0:
            for project_name, activity_count in project_activity.items():
                project_cost = (activity_count / total_activity) * historical_data['cost']
                historical_data['projects'][project_name] = {
                    'cost': project_cost,
                    'messages': int((activity_count / total_activity) * total_messages)
                }

    except Exception as e:
        print(f"Warning: Could not parse stats-cache.json: {e}", file=sys.stderr)

    return historical_data


def parse_all_sessions():
    """Parse all session logs and aggregate data."""
    claude_dir = get_claude_dir()
    projects_dir = claude_dir / 'projects'

    if not projects_dir.exists():
        print(f"Error: Projects directory not found at {projects_dir}")
        sys.exit(1)

    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    year_start = datetime(now.year, 1, 1)

    data = {
        'daily': defaultdict(float),
        'weekly': 0.0,
        'monthly': 0.0,
        'yearly': 0.0,
        'all_time': 0.0,
        'projects': defaultdict(lambda: {'cost': 0.0, 'messages': 0}),
        'models': defaultdict(float),
        'cache_savings': 0.0,
        'active_days': set(),
        'first_session': None,
        'last_session': None,
    }

    # First, load historical stats from stats-cache.json
    historical = parse_stats_cache()

    if historical['cost'] > 0:
        data['all_time'] += historical['cost']
        data['cache_savings'] += historical['cache_savings']

        if historical['first_date']:
            data['first_session'] = historical['first_date']

        # Add historical daily costs and determine timeframes
        for date_str, cost in historical['daily_costs'].items():
            data['daily'][date_str] += cost
            data['active_days'].add(date_str)

            # Parse date for timeframe bucketing
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')

                if date_obj >= week_ago:
                    data['weekly'] += cost
                if date_obj >= month_ago:
                    data['monthly'] += cost
                if date_obj >= year_start:
                    data['yearly'] += cost

            except ValueError:
                pass

        # Add historical projects (broken down by project name)
        for project_name, project_info in historical['projects'].items():
            data['projects'][project_name]['cost'] += project_info['cost']
            data['projects'][project_name]['messages'] += project_info['messages']

        data['models']['claude-sonnet-4-5'] += historical['cost']

    # Find all JSONL files
    jsonl_files = list(projects_dir.rglob('*.jsonl'))

    if not jsonl_files and historical['cost'] == 0:
        print("No session logs found.")
        sys.exit(0)

    for jsonl_file in jsonl_files:
        try:
            # Get project name from the session file's cwd field (more accurate)
            # or fallback to parent directory name
            project_name = None

            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line)

                        # Extract project name from cwd if not set yet
                        if project_name is None:
                            cwd = entry.get('cwd', '')
                            if cwd:
                                project_name = normalize_project_name(cwd)
                            else:
                                # Fallback to parent directory name
                                project_name = jsonl_file.parent.name.replace('C--Users-dpeters-', '')
                                project_name = project_name.replace('-', ' ')

                        # Look for assistant messages with usage
                        if entry.get('type') == 'assistant':
                            message = entry.get('message', {})
                            usage = message.get('usage', {})
                            model = message.get('model', 'claude-sonnet-4-5')
                            timestamp_str = entry.get('timestamp')

                            if usage and timestamp_str:
                                # Parse timestamp
                                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                                timestamp = timestamp.replace(tzinfo=None)  # Make naive for comparison
                                date_key = timestamp.strftime('%Y-%m-%d')

                                # Calculate cost and savings
                                cost, savings = calculate_cost_and_savings(usage, model)

                                # Track first/last session (compare with historical if exists)
                                if data['first_session'] is None:
                                    data['first_session'] = timestamp
                                elif timestamp < data['first_session']:
                                    data['first_session'] = timestamp

                                if data['last_session'] is None or timestamp > data['last_session']:
                                    data['last_session'] = timestamp

                                # All-time
                                data['all_time'] += cost
                                data['cache_savings'] += savings

                                # Daily
                                data['daily'][date_key] += cost
                                data['active_days'].add(date_key)

                                # Timeframe buckets
                                if timestamp >= week_ago:
                                    data['weekly'] += cost
                                if timestamp >= month_ago:
                                    data['monthly'] += cost
                                if timestamp >= year_start:
                                    data['yearly'] += cost

                                # Project breakdown
                                data['projects'][project_name]['cost'] += cost
                                data['projects'][project_name]['messages'] += 1

                                # Model breakdown
                                model_key = get_model_key(model)
                                data['models'][model_key] += cost

                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue

        except Exception as e:
            print(f"Error reading {jsonl_file}: {e}", file=sys.stderr)
            continue

    return data


def get_org_billing_url():
    """Extract organization ID and generate billing URL."""
    try:
        result = subprocess.run(['claude', 'auth', 'status', '--text'],
                              capture_output=True, text=True, timeout=5)

        if result.returncode == 0:
            # Try to extract org ID (though it may not be in the output)
            output = result.stdout

            # Look for org ID pattern
            if 'org_' in output:
                for line in output.split('\n'):
                    if 'org_' in line:
                        # Extract org_xxxxx
                        import re
                        match = re.search(r'(org_[a-zA-Z0-9]+)', line)
                        if match:
                            org_id = match.group(1)
                            return f"https://console.anthropic.com/settings/{org_id}/billing"

            # Default to general billing page
            return "https://console.anthropic.com/settings/billing"
    except:
        pass

    return "https://console.anthropic.com/settings/billing"


def format_currency(amount, currency_code, exchange_rate, color_local=True):
    """Format as USD and specified currency with BobAI colors."""
    # USD in white/bold
    usd = f"{Colors.WHITE_BOLD}${amount:.2f} USD{Colors.RESET}"

    if currency_code == 'USD':
        return usd

    converted = amount * exchange_rate

    # Local currency in magenta
    local_color = Colors.MAGENTA if color_local else ''
    reset = Colors.RESET if color_local else ''

    # Format based on typical currency display
    if exchange_rate > 100:  # Large numbers (JPY, KRW, etc.)
        return f"{usd} {local_color}({converted:,.0f} {currency_code}){reset}"
    elif exchange_rate < 0.01:  # Crypto
        return f"{usd} {local_color}({converted:.6f} {currency_code}){reset}"
    else:
        return f"{usd} {local_color}({converted:,.2f} {currency_code}){reset}"


def print_report(data, currency_code, exchange_rate, rate_source):
    """Print comprehensive cost report with BobAI-matched colors."""

    # BobAI Blue borders and headers
    print(f"\n{Colors.BOBAI_BLUE}{'═'*80}{Colors.RESET}")
    print(f"{Colors.CYAN}💰 CLAUDE CODE - USAGE & COST BREAKDOWN{Colors.RESET}")
    print(f"{Colors.BOBAI_BLUE}{'═'*80}{Colors.RESET}")
    print()

    # ============ TIME-BASED COSTS ============
    source_icon = "🌐" if rate_source == "LIVE" else "💾" if rate_source == "VAULT" else ""
    rate_label = f"{Colors.GREEN}LIVE SYNC {source_icon}{Colors.RESET}" if rate_source == "LIVE" else f"{Colors.MAGENTA}VAULT {source_icon}{Colors.RESET}" if rate_source == "VAULT" else ""

    if currency_code != 'USD':
        print(f"{Colors.CYAN}📅 COST BY TIMEFRAME {Colors.RESET}(1 USD = {Colors.MAGENTA}{exchange_rate:.4f} {currency_code}{Colors.RESET} - {rate_label})")
    else:
        print(f"{Colors.CYAN}📅 COST BY TIMEFRAME{Colors.RESET}")
    print(f"{Colors.BOBAI_BLUE}{'─' * 80}{Colors.RESET}")

    # Today
    today_key = datetime.now().strftime('%Y-%m-%d')
    today_cost = data['daily'].get(today_key, 0.0)
    print(f"  Today:          {format_currency(today_cost, currency_code, exchange_rate)}")

    # Weekly
    print(f"  Last 7 Days:    {format_currency(data['weekly'], currency_code, exchange_rate)}")

    # Monthly
    print(f"  Last 30 Days:   {format_currency(data['monthly'], currency_code, exchange_rate)}")

    # Yearly
    print(f"  This Year:      {format_currency(data['yearly'], currency_code, exchange_rate)}")

    # All-time
    print(f"  All-Time:       {format_currency(data['all_time'], currency_code, exchange_rate)}")
    print()

    # ============ PROJECT BREAKDOWN ============
    print(f"{Colors.CYAN}📁 COST BY PROJECT{Colors.RESET}")
    print(f"{Colors.BOBAI_BLUE}{'─' * 80}{Colors.RESET}")

    # Sort projects by cost (highest first)
    sorted_projects = sorted(data['projects'].items(),
                           key=lambda x: x[1]['cost'], reverse=True)

    searchable_obc_cost = 0.0
    other_projects_cost = 0.0
    misc_projects = []
    misc_cost = 0.0
    misc_messages = 0

    MISC_THRESHOLD = 0.05  # Group projects under $0.05 into Miscellaneous

    for project_name, info in sorted_projects:
        cost = info['cost']
        messages = info['messages']

        # Check if SEARCHABLE OBC
        is_searchable = 'SEARCHABLE OBC' in project_name.upper()

        if is_searchable:
            searchable_obc_cost += cost
            marker = " 🎯"
            # Always show SEARCHABLE OBC
            print(f"  {project_name[:45]:<45} {format_currency(cost, 'USD', 1.0):>15} ({messages:>4} msgs){marker}")
        elif cost < MISC_THRESHOLD:
            # Group small projects
            misc_projects.append(project_name)
            misc_cost += cost
            misc_messages += messages
            other_projects_cost += cost
        else:
            # Show significant projects
            other_projects_cost += cost
            marker = ""
            print(f"  {project_name[:45]:<45} {format_currency(cost, 'USD', 1.0):>15} ({messages:>4} msgs){marker}")

    # Show miscellaneous if any
    if misc_cost > 0:
        print(f"  {'Miscellaneous / Quick Tasks':<45} {format_currency(misc_cost, 'USD', 1.0):>15} ({misc_messages:>4} msgs)")
        print(f"    (includes {len(misc_projects)} small projects)")

    if searchable_obc_cost > 0 or other_projects_cost > 0:
        print(f"{Colors.BOBAI_BLUE}{'─' * 80}{Colors.RESET}")
        if searchable_obc_cost > 0:
            print(f"  {'SEARCHABLE OBC (Total)':<45} {format_currency(searchable_obc_cost, 'USD', 1.0):>15}")
        print(f"  {'Other Projects (Total)':<45} {format_currency(other_projects_cost, 'USD', 1.0):>15}")
    print()

    # ============ MODEL BREAKDOWN ============
    print(f"{Colors.CYAN}🤖 COST BY MODEL{Colors.RESET}")
    print(f"{Colors.BOBAI_BLUE}{'─' * 80}{Colors.RESET}")

    for model, cost in sorted(data['models'].items()):
        model_name = model.replace('claude-', '').upper()
        print(f"  {model_name:<25} {format_currency(cost, 'USD', 1.0):>15}")
    print()

    # ============ PROMPT CACHING SAVINGS ============
    print(f"{Colors.CYAN}💾 PROMPT CACHING SAVINGS{Colors.RESET}")
    print(f"{Colors.BOBAI_BLUE}{'─' * 80}{Colors.RESET}")
    total_without_cache = data['all_time'] + data['cache_savings']
    savings_percent = (data['cache_savings'] / total_without_cache * 100) if total_without_cache > 0 else 0

    print(f"  Without Caching:     {format_currency(total_without_cache, currency_code, exchange_rate)}")
    print(f"  With Caching:        {format_currency(data['all_time'], currency_code, exchange_rate)}")
    print(f"  {Colors.GREEN}💰 Total Saved:{Colors.RESET}      {format_currency(data['cache_savings'], currency_code, exchange_rate)} {Colors.GREEN}({savings_percent:.1f}%){Colors.RESET}")
    print()

    # ============ USAGE EFFICIENCY ============
    print(f"{Colors.CYAN}📊 USAGE EFFICIENCY - THE ANXIETY KILLER{Colors.RESET}")
    print(f"{Colors.BOBAI_BLUE}{'─' * 80}{Colors.RESET}")

    active_days = len(data['active_days'])

    if data['first_session']:
        # Use last session if available, otherwise use today
        last_date = data['last_session'] if data['last_session'] else datetime.now()
        project_age_days = (last_date - data['first_session']).days + 1
        idle_days = max(0, project_age_days - active_days)

        avg_daily_when_active = data['all_time'] / active_days if active_days > 0 else 0

        print(f"  Project Age:         {project_age_days} days (since {data['first_session'].strftime('%b %d, %Y')})")
        print(f"  Active Days:         {active_days} days")
        print(f"  {Colors.GREEN}Idle Days:           {idle_days} days (cost: $0.00) ✅{Colors.RESET}")
        print(f"  Avg Cost/Active Day: {format_currency(avg_daily_when_active, 'USD', 1.0)}")
        print(f"  First Session:       {data['first_session'].strftime('%Y-%m-%d')}")
        if data['last_session']:
            print(f"  Last Session:        {data['last_session'].strftime('%Y-%m-%d')}")

        print()
        if idle_days > 0:
            print(f"  {Colors.GREEN}💡 You only pay when you use Claude - {idle_days} idle days cost nothing!{Colors.RESET}")
        else:
            print(f"  {Colors.GREEN}💡 You only pay when you use Claude - idle days cost nothing!{Colors.RESET}")
    else:
        print(f"  Active Days:         {active_days}")
        if active_days > 0:
            avg_daily = data['all_time'] / active_days
            print(f"  Avg Cost/Active Day: {format_currency(avg_daily, 'USD', 1.0)}")

    print()

    # ============ BILLING LINK ============
    print(f"{Colors.CYAN}🔗 VERIFY ON WEB{Colors.RESET}")
    print(f"{Colors.BOBAI_BLUE}{'─' * 80}{Colors.RESET}")
    billing_url = get_org_billing_url()
    print(f"  Direct Billing Dashboard:")
    print(f"  {Colors.BOBAI_BLUE}{billing_url}{Colors.RESET}")
    print()

    print(f"{Colors.BOBAI_BLUE}{'═'*80}{Colors.RESET}")
    today_key = datetime.now().strftime('%Y-%m-%d')
    today_cost = data['daily'].get(today_key, 0.0)
    print(f"\n{Colors.GREEN}✅ Daily Spend:{Colors.RESET}   {format_currency(today_cost, currency_code, exchange_rate)}")
    print(f"{Colors.GREEN}✅ Weekly Spend:{Colors.RESET}  {format_currency(data['weekly'], currency_code, exchange_rate)}")
    print(f"{Colors.GREEN}✅ Monthly Spend:{Colors.RESET} {format_currency(data['monthly'], currency_code, exchange_rate)}")
    print(f"{Colors.GREEN}✅ Yearly Spend:{Colors.RESET}  {format_currency(data['yearly'], currency_code, exchange_rate)}")
    print(f"{Colors.BOBAI_BLUE}{'═'*80}{Colors.RESET}")

    # ============ PRO TIP ============
    print(f"\n{Colors.YELLOW}💡 PRO TIP:{Colors.RESET} Prompt cache expires after 5 minutes of inactivity.")
    print(f"   {Colors.YELLOW}Keep sessions active to maximize your savings!{Colors.RESET}\n")


def main():
    """Main entry point."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='BBox Claudit - Global Claude Code Cost Auditor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  claudit           # Default (CAD)
  claudit -c EUR    # Euros
  claudit -c JPY    # Japanese Yen
  claudit -c GBP    # British Pounds

Supported: 100+ currencies from the Global Vault
        """
    )
    parser.add_argument('-c', '--currency', default='CAD',
                       help='ISO 4217 currency code (default: CAD)')

    args = parser.parse_args()

    # Get exchange rate
    currency_code = args.currency.upper()
    exchange_rate, rate_source = get_exchange_rate(currency_code)

    if exchange_rate is None:
        print(f"Error: Currency '{currency_code}' not supported.")
        print(f"Try: USD, CAD, EUR, GBP, JPY, CNY, INR, AUD, or 100+ others.")
        sys.exit(1)

    # Print header with BobAI-matched rounded Unicode box (Snug Fit)
    _h1 = "BBox Claudit v1.9"
    _h2 = "Claude Code Use/Cost Auditor"
    _h3 = "\u00a9 2026 Donald Peters | BentoBox Tools"
    _h4 = "All Rights Reserved"
    _w = max(len(_h1), len(_h2), len(_h3), len(_h4)) + 2
    print(f"\n{Colors.BOBAI_BLUE}╭{'─'*_w}╮{Colors.RESET}")
    print(f"{Colors.BOBAI_BLUE}│{Colors.RESET} {Colors.CYAN}{Colors.BOLD}{_h1}{Colors.RESET}{' '*(_w-1-len(_h1))}{Colors.BOBAI_BLUE}│{Colors.RESET}")
    print(f"{Colors.BOBAI_BLUE}│{Colors.RESET} {Colors.WHITE}{_h2}{Colors.RESET}{' '*(_w-1-len(_h2))}{Colors.BOBAI_BLUE}│{Colors.RESET}")
    print(f"{Colors.BOBAI_BLUE}│{Colors.RESET}{' '*_w}{Colors.BOBAI_BLUE}│{Colors.RESET}")
    print(f"{Colors.BOBAI_BLUE}│{Colors.RESET} {Colors.GREY}{_h3}{Colors.RESET}{' '*(_w-1-len(_h3))}{Colors.BOBAI_BLUE}│{Colors.RESET}")
    print(f"{Colors.BOBAI_BLUE}│{Colors.RESET} {Colors.GREY}{_h4}{Colors.RESET}{' '*(_w-1-len(_h4))}{Colors.BOBAI_BLUE}│{Colors.RESET}")
    print(f"{Colors.BOBAI_BLUE}╰{'─'*_w}╯{Colors.RESET}")
    print(f"{Colors.GREEN}Liked the audit? Buy me a Bento: https://ko-fi.com/bboxtools{Colors.RESET}")

    print(f"\n{Colors.YELLOW}🔍 Scanning Claude Code session logs...{Colors.RESET}")
    data = parse_all_sessions()
    print_report(data, currency_code, exchange_rate, rate_source)


if __name__ == '__main__':
    main()
