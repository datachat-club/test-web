# Clash Rules

自定义 Shadowrocket 规则配置，每日自动从 [Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever) 同步基础规则，并合并本地自定义规则。

## 订阅地址

```
https://raw.githubusercontent.com/datachat-club/test-web/refs/heads/master/whitelist.conf
```

扫描二维码在手机上快速导入：

![订阅二维码](https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https%3A%2F%2Fraw.githubusercontent.com%2Fdatachat-club%2Ftest-web%2Frefs%2Fheads%2Fmaster%2Fwhitelist.conf)

## 自定义规则说明

| 文件 | 动作 | 说明 |
|------|------|------|
| `us.txt` | PROXY | 需要代理的境外服务 |
| `jp_tw.txt` | PROXY | 日本/台湾相关服务 |
| `cn.txt` | DIRECT | 直连的国内/特定服务 |

## 自动更新

GitHub Actions 每日 UTC 02:00（北京时间 10:00）自动拉取最新基础配置并重新合并。
