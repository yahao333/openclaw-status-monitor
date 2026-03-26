# OpenClaw 状态监控

**再也不用问"在吗？"。**

一个自动同步 OpenClaw Agent 状态到云端仪表盘的技能，让你一眼看清谁在线、他们在干什么——无需打断他们。

## 痛点

```
你：在吗？
Agent：在的。
你：最近在忙什么？
Agent：...
```

每次都要问。每次都打断。

你的 Agent 24 小时运行，但你不知道他们在干什么。

## 解决方案

一个实时仪表盘，展示：

- ✅ 哪些 Agent 在线
- 💬 每个 Agent 在"想"什么（基于 SOUL.md 个性）
- 📊 活动状态和趋势
- 🔔 当事件发生时实时通知

## 功能特性

- **无需问"在吗"** - 一眼看清状态，不打断 Agent 的工作节奏
- **SOUL 个性问候** - 每个 Agent 的问候语反映真实个性
- **定时同步** - 默认每 30 分钟自动更新（可配置）
- **实时更新** - Agent 上报时 SSE 通知
- **多 Agent 支持** - 所有 Agent，一个仪表盘

## 问候语示例

| Agent 风格 | 他们会说 |
|------------|----------|
| 💡 足智多谋 | "创意模式已激活，随时准备攻克难题" |
| ⚡ 简洁高效 | "轻装上阵，高效出击，随时待命" |
| 🔧 细致入微 | "系统就绪，滴水不漏" |
| 🎯 轻松活泼 | "嘿！让我们一起创造精彩吧" |

## 快速开始

```bash
# 1. 安装
cd ~/.openclaw/skills
git clone git@github.com:yahao333/openclaw-status-monitor.git
mv openclaw-status-monitor openclaw-status-monitor.skill

# 2. 重启
openclaw gateway restart

# 3. 启用
# 对 OpenClaw 说："启用状态监控"
```

然后访问你的仪表盘：**https://openclaw-agent-monitor.vercel.app**

## 工作原理

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  OpenClaw  │────▶│  每30分钟   │────▶│    仪表盘       │
│   Agents   │     │    同步     │     │  (查看在线状态) │
└─────────────┘     └──────────────┘     └─────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   SOUL.md    │───▶ 生成问候语
                    └──────────────┘
```

## 相关文档

- [INSTALL.md](./INSTALL.md) - 详细安装指南
- [README.md](./README.md) - English introduction

## 相关项目

- [OpenClaw Agent Monitor](https://github.com/yahao333/openclaw-agent-monitor) - 监控仪表盘

## 开源协议

MIT
