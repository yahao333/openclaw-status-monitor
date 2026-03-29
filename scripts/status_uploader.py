#!/usr/bin/env python3
"""
OpenClaw Agent Status Uploader
定时将 Agent 在线状态上传到监控平台
"""

import os
import sys
import json
import time
import signal
import logging
from datetime import datetime, timezone
from pathlib import Path

# 配置
HOME = Path.home()
CREDENTIALS_FILE = HOME / ".openclaw/credentials/openclaw-status-monitor.json"
AGENTS_DIR = HOME / ".openclaw/agents"
OPENCLAW_JSON = HOME / ".openclaw/openclaw.json"
LOG_DIR = HOME / ".openclaw/logs"
PID_FILE = HOME / ".openclaw/logs/status_uploader.pid"
LOG_FILE = LOG_DIR / "status_uploader.log"
ERROR_LOG_FILE = LOG_DIR / "status_uploader_error.log"
SYNC_INTERVAL = 300  # 5分钟

# 确保日志目录存在
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_token():
    """加载 Token"""
    if os.environ.get("MONITOR_PLATFORM_TOKEN"):
        return os.environ["MONITOR_PLATFORM_TOKEN"]

    if CREDENTIALS_FILE.exists():
        with open(CREDENTIALS_FILE) as f:
            data = json.load(f)
            return data.get("agentToken")

    return None


def get_monitor_url():
    """获取监控平台 URL"""
    if os.environ.get("OPENCLAW_MONITOR_URL"):
        return os.environ["OPENCLAW_MONITOR_URL"]

    if CREDENTIALS_FILE.exists():
        with open(CREDENTIALS_FILE) as f:
            data = json.load(f)
            return data.get("monitorUrl", "https://openclaw-agent-monitor.vercel.app")

    return "https://openclaw-agent-monitor.vercel.app"


def get_agent_ids():
    """从 openclaw.json 获取 agent ID 列表"""
    if not OPENCLAW_JSON.exists():
        return []

    try:
        with open(OPENCLAW_JSON) as f:
            data = json.load(f)
            return [a["id"] for a in data.get("agents", {}).get("list", [])]
    except Exception as e:
        logger.error(f"读取 openclaw.json 失败: {e}")
        return []


def get_all_agents():
    """获取所有 agent ID 列表"""
    return get_agent_ids()


def upload_status(agent_ids):
    """上传状态到监控平台"""
    import urllib.request
    import urllib.error

    token = load_token()
    if not token:
        logger.error("未找到 Token")
        return False

    url = f"{get_monitor_url()}/api/upload"

    # 转换为 API 期望的格式 [{id: "agentId"}, ...]
    agents = [{"id": aid} for aid in agent_ids]

    try:
        data = json.dumps(agents).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "x-agent-token": token
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 200:
                logger.info(f"上传成功: {agent_ids}")
                return True
            else:
                logger.error(f"上传失败: HTTP {response.status}")
                return False

    except urllib.error.HTTPError as e:
        logger.error(f"HTTP 错误: {e.code} - {e.reason}")
        with open(ERROR_LOG_FILE, "a") as f:
            f.write(f"{datetime.now(timezone.utc).isoformat()} - HTTP {e.code}: {e.reason}\n")
        return False
    except urllib.error.URLError as e:
        logger.error(f"网络错误: {e.reason}")
        with open(ERROR_LOG_FILE, "a") as f:
            f.write(f"{datetime.now(timezone.utc).isoformat()} - Network: {e.reason}\n")
        return False
    except Exception as e:
        logger.error(f"上传异常: {e}")
        with open(ERROR_LOG_FILE, "a") as f:
            f.write(f"{datetime.now(timezone.utc).isoformat()} - Exception: {e}\n")
        return False


def save_pid():
    """保存 PID"""
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))


def is_running():
    """检查进程是否在运行"""
    if not PID_FILE.exists():
        return False

    try:
        with open(PID_FILE) as f:
            pid = int(f.read().strip())

        # 检查进程是否存在
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, ValueError, PermissionError):
        # 进程不存在或无权限
        PID_FILE.unlink(missing_ok=True)
        return False


def cleanup():
    """清理 PID 文件"""
    PID_FILE.unlink(missing_ok=True)


def daemon_mode():
    """守护进程模式"""
    # 首次检查
    token = load_token()
    if not token:
        logger.error("未配置 Token，请先运行 'openclaw skills enable status-monitor' 配置")
        sys.exit(1)

    # 保存 PID
    save_pid()
    logger.info(f"状态上传服务启动，PID: {os.getpid()}")
    logger.info(f"上传间隔: {SYNC_INTERVAL} 秒")

    # 设置信号处理
    def signal_handler(signum, frame):
        logger.info("收到停止信号，正在退出...")
        cleanup()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            agents = get_all_agents()
            if agents:
                upload_status(agents)
            else:
                logger.info("无 Agent，跳过本次上传")
        except Exception as e:
            logger.error(f"执行异常: {e}")
            with open(ERROR_LOG_FILE, "a") as f:
                f.write(f"{datetime.now(timezone.utc).isoformat()} - Loop Exception: {e}\n")

        time.sleep(SYNC_INTERVAL)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "start":
            if is_running():
                print("服务已在运行中")
                sys.exit(0)
            daemon_mode()
        elif cmd == "stop":
            if PID_FILE.exists():
                with open(PID_FILE) as f:
                    pid = int(f.read().strip())
                try:
                    os.kill(pid, signal.SIGTERM)
                    print(f"已发送停止信号到 PID {pid}")
                except ProcessLookupError:
                    print("进程不存在")
                    cleanup()
            else:
                print("服务未运行")
        elif cmd == "status":
            if is_running():
                with open(PID_FILE) as f:
                    pid = f.read().strip()
                print(f"服务正在运行，PID: {pid}")
            else:
                print("服务未运行")
        elif cmd == "test":
            agents = get_all_agents()
            print(f"所有 Agent: {agents}")
            if agents:
                upload_status(agents)
        else:
            print(f"未知命令: {cmd}")
            print("用法: status_uploader.py [start|stop|status|test]")
    else:
        # 单次执行
        agents = get_all_agents()
        if agents:
            upload_status(agents)
        else:
            print("无 Agent")
