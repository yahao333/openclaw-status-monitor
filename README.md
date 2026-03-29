# OpenClaw Status Monitor

**Never ask "Are you there?" again.**

A skill that auto-syncs your OpenClaw agents' status to a cloud dashboard, so you can see who's online and what they're doing — without interrupting them.

[中文介绍](./README_cn.md)

## The Problem

```
You: "Are you there?"
Agent: "Yes, I'm here."
You: "What are you working on?"
Agent: "..."
```

Every. Single. Time.

Your agents are running 24/7, but you have no idea what they're doing without asking. That's friction.

## The Solution

A live dashboard that shows:

- ✅ Which agents are online
- 📊 Real-time activity status
- 🔔 Automatic offline detection (5-minute threshold)

## Features

- **Zero-Check-In Required** - See agent status at a glance, never interrupt their flow
- **Automatic Offline Detection** - Dashboard marks agents offline after 5 minutes of no heartbeat
- **Scheduled Sync** - Auto-updates every 5 minutes via background script
- **Real-time Updates** - SSE notifications when agents report in
- **Multi-Agent** - All your agents, one dashboard
- **Simple Integration** - Only uploads agent IDs; all business logic handled by dashboard

## Quick Start

For detailed installation instructions, see [INSTALL.md](./INSTALL.md).

**Basic steps:**
1. Install to OpenClaw skills directory
2. Run `openclaw gateway restart`
3. Tell OpenClaw: "enable status monitoring"

Then visit **https://openclaw-agent-monitor.vercel.app** to see your dashboard.

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  OpenClaw  │────▶│  Uploader    │────▶│    Dashboard     │
│   Agents   │     │  Script      │     │  (see who's up) │
│   (IDs)    │     │  (Python)    │     │  Offline detect  │
└─────────────┘     └──────────────┘     └─────────────────┘
```

The skill manages a Python uploader script that runs as a daemon. It only uploads agent IDs — the dashboard handles:
- Storing agent metadata (name, greeting, etc.)
- Calculating online/offline status
- Generating greetings and display

## Script Management

The skill provides simple commands to manage the uploader:

### Basic Management (status_uploader.py)

| Command | Description |
|---------|-------------|
| `python3 scripts/status_uploader.py start` | Start the uploader daemon |
| `python3 scripts/status_uploader.py start --interval 10` | Start with custom interval (minutes) |
| `python3 scripts/status_uploader.py stop` | Stop the uploader daemon |
| `python3 scripts/status_uploader.py status` | Check daemon status and interval |
| `python3 scripts/status_uploader.py set-interval 10` | Change sync interval |
| `python3 scripts/status_uploader.py test` | Run a one-time upload test |


## Documentation

- [INSTALL.md](./INSTALL.md) - Detailed installation guide
- [README_cn.md](./README_cn.md) - 中文介绍

## Related

- [OpenClaw Agent Monitor](https://github.com/yahao333/openclaw-agent-monitor) - The monitoring dashboard

## License

MIT
