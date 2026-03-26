# OpenClaw Status Monitor

定时将 OpenClaw Agent 状态同步到云端监控平台，根据 SOUL.md 个性生成随机问候语。

## Features

- **Scheduled Sync** - Auto-sync every 30 minutes (configurable)
- **SOUL-based Greetings** - Generate random greetings based on each agent's SOUL.md personality
- **Easy Setup** - First-time initialization guides you through token configuration
- **Multiple Agents** - Supports all OpenClaw agents with individual greetings

## Quick Start

### 1. Install

```bash
cd ~/.openclaw/skills
git clone git@github.com:yahao333/openclaw-status-monitor.git
mv openclaw-status-monitor openclaw-status-monitor.skill
```

### 2. Restart OpenClaw

```bash
openclaw restart
```

### 3. Enable

Tell OpenClaw:
```
enable status monitoring
```

## Greeting Examples

| Agent Style | English | Chinese |
|-------------|---------|---------|
| concise | ⚡ Running lean and mean, ready to assist | 简洁高效，随时待命 |
| thorough | 🔧 Every detail covered, always | 细致入微，使命必达 |
| resourceful | 💡 Creative mode activated | 创意模式已激活 |
| casual | 🎯 Let's make magic happen | 轻松一刻，效率加倍 |
| helpful | 🤝 Here to help, always | 全心全意，助你前行 |

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| Sync Interval | 30 min | Configurable: 5/10/15/30/60 min |
| Monitor URL | Vercel Deploy | Your monitoring platform |

## Documentation

- [INSTALL.md](./INSTALL.md) - Detailed installation guide
- [SKILL.md](./SKILL.md) - Full skill specification

## License

MIT
