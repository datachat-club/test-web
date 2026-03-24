"""
Fetches the base Shadowrocket whitelist config and merges custom rules from local .txt files.
Also generates README.md with a QR code for the raw config URL.
"""

import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import quote

BASE_URL = "https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/sr_top500_whitelist.conf"
RAW_CONF_URL = "https://raw.githubusercontent.com/datachat-club/test-web/refs/heads/master/whitelist.conf"

# Ordered mapping: filename -> Shadowrocket action
RULE_FILES = [
    ("us.txt", "PROXY"),
    ("jp_tw.txt", "PROXY"),
    ("cn.txt", "DIRECT"),
]


def parse_clash_rules(filepath: Path, action: str) -> list[str]:
    """Convert Clash YAML rule list to Shadowrocket rule lines."""
    rules = []
    for line in filepath.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("- "):
            rule = line[2:]
            rules.append(f"{rule},{action}")
    return rules


def build_custom_block() -> str:
    lines = []
    for filename, action in RULE_FILES:
        path = Path(filename)
        if not path.exists():
            print(f"Warning: {filename} not found, skipping.", file=sys.stderr)
            continue
        rules = parse_clash_rules(path, action)
        lines.append(f"# Custom rules from {filename}")
        lines.extend(rules)
        lines.append("")
    return "\n".join(lines)


def fetch_base_config() -> str:
    print(f"Fetching base config from {BASE_URL} ...")
    with urllib.request.urlopen(BASE_URL, timeout=30) as resp:
        return resp.read().decode("utf-8")


def merge(base: str, custom_block: str) -> str:
    """Insert custom rules immediately after the [Rule] section header."""
    return re.sub(
        r"(\[Rule\]\r?\n)",
        lambda m: m.group(1) + custom_block + "\n",
        base,
        count=1,
    )


def generate_readme() -> str:
    encoded_url = quote(RAW_CONF_URL, safe="")
    qr_img_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_url}"
    return f"""# Clash Rules

自定义 Shadowrocket 规则配置，每日自动从 [Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever) 同步基础规则，并合并本地自定义规则。

## 订阅地址

```
{RAW_CONF_URL}
```

扫描二维码在手机上快速导入：

![订阅二维码]({qr_img_url})

## 自定义规则说明

| 文件 | 动作 | 说明 |
|------|------|------|
| `us.txt` | PROXY | 需要代理的境外服务 |
| `jp_tw.txt` | PROXY | 日本/台湾相关服务 |
| `cn.txt` | DIRECT | 直连的国内/特定服务 |

## 自动更新

GitHub Actions 每日 UTC 02:00（北京时间 10:00）自动拉取最新基础配置并重新合并。
"""


def main():
    base = fetch_base_config()
    custom_block = build_custom_block()
    merged = merge(base, custom_block)

    Path("whitelist.conf").write_text(merged, encoding="utf-8")
    print("whitelist.conf updated.")

    Path("README.md").write_text(generate_readme(), encoding="utf-8")
    print("README.md generated.")


if __name__ == "__main__":
    main()
