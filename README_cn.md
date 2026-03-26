# OpenClaw 状态监控

定时将 OpenClaw Agent 状态同步到云端监控平台，根据 SOUL.md 个性生成随机问候语。

## 功能特性

- **定时同步** - 默认每 30 分钟自动同步（可配置）
- **SOUL 个性问候** - 根据每个 Agent 的 SOUL.md 生成随机问候语
- **简易配置** - 首次使用自动引导配置 Token
- **多 Agent 支持** - 支持所有 OpenClaw Agent，单独生成问候语

## 快速开始

### 1. 安装

```bash
cd ~/.openclaw/skills
git clone git@github.com:yahao333/openclaw-status-monitor.git
mv openclaw-status-monitor openclaw-status-monitor.skill
```

### 2. 重启 OpenClaw

```bash
openclaw restart
```

### 3. 启用

对 OpenClaw 说：
```
启用状态监控
```

## 问候语示例

| Agent 风格 | 英文 | 中文 |
|------------|------|------|
| 简洁型 | ⚡ Running lean and mean, ready to assist | 简洁高效，随时待命 |
| 细致型 | 🔧 Every detail covered, always | 细致入微，使命必达 |
| 创意型 | 💡 Creative mode activated | 创意模式已激活 |
| 轻松型 | 🎯 Let's make magic happen | 轻松一刻，效率加倍 |
| 帮助型 | 🤝 Here to help, always | 全心全意，助你前行 |

## 配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| 同步间隔 | 30 分钟 | 可配置：5/10/15/30/60 分钟 |
| 监控地址 | Vercel 部署 | 你的监控平台地址 |

## 相关文档

- [INSTALL.md](./INSTALL.md) - 详细安装指南
- [SKILL.md](./SKILL.md) - 完整技能说明

## 开源协议

MIT
