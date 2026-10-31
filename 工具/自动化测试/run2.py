# -*- coding: utf-8 -*-
"""
aa-bridge 桥接调用器：把本地 .aardio 源码发给运行中的 aacli 服务执行。

用法:
    python run2.py 脚本.aardio

token 优先级: 环境变量 AA_BRIDGE_TOKEN > %LOCALAPPDATA%\\aardio\\autos\\aa-bridge.table
服务地址: 环境变量 AA_BRIDGE_URL（默认 http://127.0.0.1:9123/api/tools/call）
"""
import sys
import os
import re
import json
import urllib.request

URL = os.environ.get("AA_BRIDGE_URL", "http://127.0.0.1:9123/api/tools/call")


def read_token():
    env = os.environ.get("AA_BRIDGE_TOKEN", "").strip()
    if env:
        return env
    table = os.path.join(os.environ.get("LOCALAPPDATA", ""), "aardio", "autos", "aa-bridge.table")
    if os.path.exists(table):
        txt = open(table, encoding="utf-8-sig", errors="replace").read()
        m = re.search(r'token\s*=\s*"([^"]+)"', txt)
        if m:
            return m.group(1)
    return ""


def call(name, args, token):
    body = json.dumps({"name": name, "arguments": args}).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json",
        "X-AA-Token": token,
    })
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read().decode("utf-8", "replace")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python run2.py 脚本.aardio")
        sys.exit(2)
    token = read_token()
    if not token:
        print("未找到桥接 token：请先启动 aacli.exe，或设置环境变量 AA_BRIDGE_TOKEN")
        sys.exit(3)
    code = open(sys.argv[1], "rb").read().decode("utf-8")
    print(call("execute_code", {"code": code}, token))
