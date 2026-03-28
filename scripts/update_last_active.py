#!/usr/bin/env python3
"""
更新 JSON 数据中所有 agent 的 lastActive 时间为当前系统 ISO 时间
用法:
    python3 update_last_active.py                    # 从 stdin 读取
    python3 update_last_active.py data.json          # 从文件读取
    python3 update_last_active.py data.json -o out.json  # 输出到文件
"""

import json
import re
import sys
from datetime import datetime, timezone


def get_current_iso_time() -> str:
    """获取当前系统 ISO 时间（UTC）"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def is_valid_json(content: str) -> bool:
    """检查字符串是否是有效的 JSON"""
    try:
        json.loads(content)
        return True
    except (json.JSONDecodeError, ValueError):
        return False


def find_matching_quote(content: str, start: int) -> tuple:
    """
    从 start 位置（指向开始的引号）找到匹配的结束引号。
    返回 (end_index, escaped)，其中 escaped 表示是否被转义。
    """
    i = start + 1
    while i < len(content):
        c = content[i]
        if c == '\\':
            i += 2  # 跳过转义字符
            continue
        if c == '"':
            return (i, False)
        i += 1
    return (-1, False)


def fix_json_with_inline_newlines(content: str) -> str:
    """
    修复 JSON 中字符串内部未转义的换行符。
    例如: {"msg": "hello\nworld"} (字面换行) -> {"msg": "hello\\nworld"}
    """
    result = []
    i = 0
    in_string = False

    while i < len(content):
        c = content[i]

        if not in_string:
            if c == '"':
                in_string = True
                result.append(c)
            elif c not in '\r\n':
                # 裸换行符在字符串外，替换为空格（JSON 允许结构中的空白）
                result.append(c)
            # 忽略裸换行符（不在字符串内）
        else:
            # 在字符串内部
            if c == '\\':
                # 处理转义序列
                if i + 1 < len(content):
                    next_c = content[i + 1]
                    if next_c in 'nrt"\\/':
                        # 有效的转义序列，保留
                        result.append(c)
                        result.append(next_c)
                        i += 2
                        continue
                    elif next_c == 'u':
                        # Unicode 转义 \uXXXX
                        if i + 5 < len(content):
                            result.append(c)
                            result.append(content[i+1:i+6])
                            i += 6
                            continue
                # 不认识的转义，保留反斜杠
                result.append(c)
            elif c == '"':
                # 字符串结束
                in_string = False
                result.append(c)
            elif c in '\r\n':
                # 字符串内部的裸换行！转换为转义序列
                result.append('\\n')
                if c == '\r' and i + 1 < len(content) and content[i + 1] == '\n':
                    i += 2  # 跳过完整的 CRLF
                else:
                    i += 1
                continue
            else:
                result.append(c)

        i += 1

    return ''.join(result)


def preprocess_json(content: str) -> str:
    """
    预处理 JSON 内容，修复常见的格式问题。
    """
    # 首先尝试直接解析，如果成功就不需要处理
    if is_valid_json(content):
        return content

    # 修复字符串内部未转义的换行符
    fixed = fix_json_with_inline_newlines(content)

    # 再次检查
    if is_valid_json(fixed):
        return fixed

    # 如果还是无效，尝试更激进的清理
    # 移除所有控制字符（除了 \t, \n, \r 在字符串外的）
    cleaned = []
    i = 0
    while i < len(content):
        c = content[i]
        if c in '\r\n':
            cleaned.append(' ')
        elif ord(c) < 32 and c not in '\t':
            # 跳过其他控制字符
            pass
        else:
            cleaned.append(c)
        i += 1

    return ''.join(cleaned)


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
            raw_content = f.read()
    else:
        # 从 stdin 读取
        raw_content = sys.stdin.read()

    # 预处理并解析 JSON
    processed = preprocess_json(raw_content)
    data = json.loads(processed)

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
