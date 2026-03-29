---
name: openclaw-status-monitor
description: 管理 OpenClaw Agent 状态上传脚本，定时将 Agent 在线状态同步到云端监控平台
author: yanghao
version: 4.0.0
metadata:
  openclaw:
    categories: [system, monitor]
    tags: [openclaw, status, sync, monitor]
    user-invocable: true
---

## 脚本位置

```
~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py
```

## 两种运行模式

### 模式一：Cron 定时同步（默认）

OpenClaw 内置 cron 定时执行，单次调用上传脚本：

```bash
# OpenClaw cron 定时调用（无 start 参数）
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py
```

**触发命令**：说"同步状态"、"重启同步状态"等，OpenClaw 会定时触发执行。

### 模式二：守护进程模式

需要持续后台运行时，使用 `--fork` 启动真正的守护进程：

| 命令 | 说明 |
|------|------|
| `python3 scripts/status_uploader.py start --fork` | 启动守护进程 |
| `python3 scripts/status_uploader.py start --fork --interval 10` | 启动并指定间隔（分钟） |
| `python3 scripts/status_uploader.py stop` | 停止服务 |
| `python3 scripts/status_uploader.py status` | 查看服务状态 |
| `python3 scripts/status_uploader.py set-interval <分钟>` | 设置同步间隔 |
| `python3 scripts/status_uploader.py test` | 单次测试上传 |

**示例：**
```bash
# 启动守护进程
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py start --fork

# 指定 10 分钟间隔
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py start --fork --interval 10
```

## 触发条件

当满足以下任一条件时触发：

1. **首次初始化**：用户说"启用状态监控"、"开启监控同步"、"配置 status-monitor"
2. **手动触发**：用户发送"同步状态"、"同步 status-monitor"、"上传状态"等 → 单次执行
3. **定时同步**：OpenClaw cron 定时触发 → 单次执行
4. **查看状态**：用户发送"查看状态监控"、"状态监控状态"、"检查上传服务"
5. **停止服务**：用户发送"停止状态监控"、"停止上传服务"
6. **修改间隔**：用户发送"每10分钟同步一次"、"改成15分钟"等
7. **守护进程**：用户发送"启动状态监控"、"启动守护进程"、"后台运行"等 → 执行 `start --fork`

## 初始化流程（首次使用必须执行）

### 第一步：检查 Token 配置

执行技能时，首先检查以下位置是否有 Token：

1. 环境变量 `MONITOR_PLATFORM_TOKEN`
2. 文件 `~/.openclaw/credentials/openclaw-status-monitor.json`

### 第二步：Token 不存在时的处理

如果未找到 Token，必须引导用户注册/登录：

1. **提示用户**：
   ```
   检测到未配置监控 Token，正在引导您完成设置...

   请选择登录方式：
   1. 已有账号：访问 https://openclaw-agent-monitor.vercel.app 点击 Sign In 使用 Clerk 登录
   2. 新用户：访问 https://openclaw-agent-monitor.vercel.app 点击 Sign Up 注册

   登录后：
   - 进入 Settings 页面
   - 生成并复制 Agent Token
   - 告诉我生成的 Token
   ```

2. **等待用户回复 Token**

3. **保存 Token**：
   - 创建目录 `~/.openclaw/credentials/`
   - 保存到 `~/.openclaw/credentials/openclaw-status-monitor.json`：
     ```json
     {
       "agentToken": "用户提供的token",
       "createdAt": "2026-03-29T10:00:00.000Z",
       "monitorUrl": "https://openclaw-agent-monitor.vercel.app"
     }
     ```

4. **验证 Token**

### 第三步：Token 验证成功后

```
✅ Token 配置成功！

正在启动上传服务...
- 执行首次同步测试...
- ✅ 服务启动成功！

监控平台地址：https://openclaw-agent-monitor.vercel.app
上传间隔：5 分钟

启动命令：
python3 scripts/status_uploader.py start --fork

管理命令：
- 说"同步状态"手动触发一次上传
- 说"查看状态监控"检查服务状态
- 说"停止状态监控"停止服务
- 说"重启状态监控"重启服务
```

## 核心功能：管理上传脚本

### 1. 检查脚本是否存在

```bash
if [ -f ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py ]; then
  echo "脚本存在"
else
  echo "脚本不存在"
fi
```

### 2. 启动服务（推荐方式）

```bash
# 使用 --fork 启动守护进程（推荐）
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py start --fork --interval 10
```

### 3. 设置同步间隔

```bash
# 方式1：启动时指定
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py start --fork --interval 15

# 方式2：使用 set-interval 命令
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py set-interval 15
```

### 4. 停止服务

```bash
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py stop
```

### 5. 检查服务状态

```bash
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py status
```

### 6. 查看错误日志

```
~/.openclaw/logs/status_uploader_error.log
~/.openclaw/logs/status_uploader.log
```

```bash
# 查看最近错误
tail -50 ~/.openclaw/logs/status_uploader_error.log

# 查看服务运行日志
tail -50 ~/.openclaw/logs/status_uploader.log
```

**日志轮转**：日志文件超过 10MB 时自动轮转，格式为 `status_uploader.20260329_183500.log`

### 7. 手动触发一次上传

```bash
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py test
```

### 上传逻辑（简化版）

脚本只负责从 `openclaw.json` 读取所有 agent ID 并上传，**不做任何离线判断**。

离线判断由监控平台（openclaw-agent-monitor）处理：
- 监控平台根据上传时间自动更新 `lastActiveTimestamp`
- 如果超过 5 分钟没有上传，监控平台自动标记为离线

## 存储配置

### Token 存储位置

`~/.openclaw/credentials/openclaw-status-monitor.json`：

```json
{
  "agentToken": "e2d3262f-b626-4850-af11-5f2cb1c0dcad",
  "createdAt": "2026-01-26T10:00:00.000Z",
  "monitorUrl": "https://openclaw-agent-monitor.vercel.app",
  "syncIntervalMinutes": 5
}
```

## 日志位置

- 服务日志：`~/.openclaw/logs/status_uploader.log`
- 错误日志：`~/.openclaw/logs/status_uploader_error.log`
- PID 文件：`~/.openclaw/logs/status_uploader.pid`
- Token 配置：`~/.openclaw/credentials/openclaw-status-monitor.json`

## 错误处理

### 1. 缺少 Token

**初始化时**：
```
❌ 未检测到监控 Token

请先完成以下步骤：

1. 访问 https://openclaw-agent-monitor.vercel.app
2. 点击 Sign In / Sign Up 登录或注册账号
3. 登录后在 Settings 页面生成 Agent Token
4. 将 Token 发送给我

示例：我的 Token 是 abc123-def456...
```

### 2. 脚本不存在

```
❌ 上传脚本不存在

请重新安装技能或联系开发者。
```

### 3. 服务启动失败

检查错误日志：
```
cat ~/.openclaw/logs/status_uploader_error.log
```

常见错误：
- Token 未配置
- 网络连接失败
- 端口被占用

### 4. Token 无效

```
❌ Token 验证失败

您提供的 Token 可能已过期或无效。

请重新获取 Token：
1. 登录 https://openclaw-agent-monitor.vercel.app
2. 进入 Settings 页面
3. 点击 Generate 生成新 Token
4. 将新 Token 发送给我
```

## 示例对话

### 首次启用

**User:** 启用状态监控
**Agent:**
正在检查监控配置...

❌ 未检测到 Agent Token

请先完成以下步骤：

1. 访问 https://openclaw-agent-monitor.vercel.app
2. 点击 **Sign In** 登录（支持 Google/GitHub 等）
3. 登录后在 **Settings** 页面生成 Agent Token
4. 将 Token 发送给我

---

**User:** 我的 Token 是 e2d3262f-b626-4850-af11-5f2cb1c0dcad
**Agent:**
正在验证 Token...

✅ Token 验证成功！

正在启动上传服务...
- 执行首次同步测试...
- ✅ 服务启动成功！

---

✅ **状态监控已启用！**

- 监控平台：https://openclaw-agent-monitor.vercel.app
- 上传间隔：5 分钟
- 服务状态：运行中

管理命令：
- 说"同步状态"手动触发一次上传
- 说"查看状态监控"检查服务状态
- 说"停止状态监控"停止服务

### 查看服务状态

**User:** 查看状态监控
**Agent:**
正在检查上传服务状态...

✅ 服务正在运行
   PID: 12345
   同步间隔: 5 分钟
   日志文件: ~/.openclaw/logs/status_uploader.log

最近运行日志：
```
2026-03-29 10:30:01 - INFO - 上传成功: ['main', 'coding']
2026-03-29 10:35:02 - INFO - 上传成功: ['main', 'coding']
```

错误日志：无

### 停止服务

**User:** 停止状态监控
**Agent:**
正在停止上传服务...

✅ 服务已停止

如需重新启动，请说"启动状态监控"。

### 手动同步

**User:** 同步状态
**Agent:**
正在执行手动上传...

在线 Agent：['main', 'coding']
上传结果：✅ 成功

### 重启服务

**User:** 重启状态监控
**Agent:**
正在重启上传服务...

✅ 服务已重启，PID: 67890

### 检查错误

**User:** 查看状态监控错误日志
**Agent:**
正在检查错误日志...

最近错误：
```
2026-03-29 09:15:03 - HTTP 401: Unauthorized
2026-03-29 09:20:01 - Network: [Errno 8] nodename nor servname provided
```

建议：请检查 Token 是否正确，或检查网络连接。
