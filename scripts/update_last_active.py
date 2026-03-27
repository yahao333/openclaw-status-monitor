#!/usr/bin/env python3
"""
更新 JSON 数据中所有 agent 的 lastActive 时间为当前系统 ISO 时间
用法:
    python3 update_last_active.py                    # 从 stdin 读取
    python3 update_last_active.py data.json          # 从文件读取
    python3 update_last_active.py data.json -o out.json  # 输出到文件
"""

import json
import sys
from datetime import datetime, timezone


def get_current_iso_time() -> str:
    """获取当前系统 ISO 时间（UTC）"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def update_last_active(data: list) -> list:
    """递归更新所有 agent 的 lastActive 字段"""
    current_time = get_current_iso_time()

    if isinstance(data, list):
        result = []
        for item in data:
            result.append(update_last_active(item))
        return result
    elif isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if key == "lastActive":
                # 替换为当前时间，保留 en/zh 结构
                if isinstance(value, dict):
                    new_value = {}
                    for lang in value:
                        new_value[lang] = current_time
                    result[key] = new_value
                else:
                    result[key] = current_time
            else:
                result[key] = update_last_active(value)
        return result
    else:
        return data


def main():
    if len(sys.argv) > 1:
        # 从文件读取
        input_path = sys.argv[1]
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        # 从 stdin 读取
        data = json.load(sys.stdin)

    updated = update_last_active(data)

    if len(sys.argv) > 2 and sys.argv[2] == "-o":
        # 输出到文件
        output_path = sys.argv[3]
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(updated, f, ensure_ascii=False, indent=2)
        print(f"Updated data saved to {output_path}")
    else:
        # 输出到 stdout
        print(json.dumps(updated, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
