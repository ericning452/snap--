# Snap Demo (Web 远程屏幕快照工具)

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

一个轻量、极简的远程屏幕截取与 Web 实时查看演示工具。通过 WebSocket 实现网页控制端与后台客户端的双向指令及画面的即时传输。

---

## 🌟 核心特性

- **极简架构**：基于 FastAPI + WebSocket 构建事件中继，无第三方重量级框架依赖。
- **高性能截屏**：使用 `mss` 库高效抓取屏幕帧，并通过 `Pillow` 进行 JPEG 压缩与 Base64 编码传输。
- **现代化 Web 界面**：原生轻量控制页面，支持实时连接状态感知与一键截屏预览。
- **高可用性**：客户端内置自动断线重连机制，服务端支持跨平台与命令行自定义端口传参。

---

## 📐 架构设计

```text
┌─────────────────┐      1. 发送 capture 指令       ┌────────────────────────┐
│  Web 控制网页   ├───────────────────────────────►│                        │
│ (static/index)  │                                │  FastAPI WebSocket 中继│
│                 │◄───────────────────────────────┤   (main.py: /ws)       │
└─────────────────┘      4. 回传 Base64 图片并渲染   └───────────┬────────────┘
                                                                 │
                                          2. 转发 capture 指令   │  ▲ 3. 回传 Base64 图片
                                                                 ▼  │
                                                   ┌────────────────────────┐
                                                   │    PC 端截屏代理服务    │
                                                   │    (pc_service.py)     │
                                                   └────────────────────────┘
```

---

## 🚀 快速开始

### 1. 克隆仓库并安装依赖

推荐使用 Python 虚拟环境运行：

```bash
git clone https://github.com/your-username/snap-demo.git
cd snap-demo

# 创建并激活虚拟环境 (可选)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

# 安装依赖包
pip install -r requirements.txt
```

### 2. 启动 WebSocket 服务端

在终端中启动中继服务：

```bash
python main.py
```
> 默认监听 `http://0.0.0.0:8000`。可通过参数修改：`python main.py --host 127.0.0.1 --port 8080`

### 3. 启动 PC 端截屏客户端

在需要被截取屏幕的电脑上打开新终端运行：

```bash
python pc_service.py
```
> 如果服务端运行在远端服务器或局域网其他设备，可以通过 `--url` 参数指定：
> ```bash
> python pc_service.py --url ws://192.168.1.100:8000/ws
> ```
> 还可以通过 `--monitor 1` 选择显示器，或者通过 `--quality 80` 调整截图质量。

### 4. 访问控制页面

在浏览器打开：[http://localhost:8000](http://localhost:8000)（如果是局域网其他设备，请将 `localhost` 替换为服务端的局域网 IP）。
页面显示“已连接”后，点击 **“📸 点击截取屏幕”** 按钮即可实时获取当前桌面快照。

---

## 📁 目录结构

```text
snap-demo/
├── .gitignore          # Git 忽略文件（已过滤 .venv 及缓存）
├── LICENSE             # MIT 开源许可证
├── README.md           # 项目使用与配置说明
├── requirements.txt    # Python 核心依赖清单
├── main.py             # FastAPI 服务端（静态托管 + WebSocket 中继）
├── pc_service.py       # PC 端截屏客户端（监听指令并抓取屏幕）
└── static/
    └── index.html      # 前端 Web 控制界面
```

---

## ⚙️ 命令行参数说明

### 服务端 (`main.py`)
| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `--host` | `str` | `0.0.0.0` | 服务绑定的主机地址 |
| `--port` | `int` | `8000` | 服务监听的 HTTP / WS 端口 |

### 客户端 (`pc_service.py`)
| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `--url` | `str` | `ws://localhost:8000/ws` | 服务端 WebSocket 连接地址（支持读取 `WS_URL` 环境变量） |
| `--monitor` | `int` | `1` | 显示器编号（`1` 通常为主屏幕，`2` 为扩展副屏） |
| `--quality` | `int` | `70` | JPEG 图片压缩质量（1-100） |

---

## ⚠️ 安全与隐私警示

- **无身份认证**：本项目为技术原型演示（Demo），默认**未内置 Token 或登录鉴权**机制。
- **网络暴露风险**：请勿在未开启防火墙限制的情况下将其直接暴露在公网环境下，否则任何能访问该端口的访客都可以通过页面截取你当前的桌面画面。
- **推荐环境**：建议仅在受信任的局域网或内网隧道/个人测试环境中使用。如需公网部署，建议在 WebSocket 握手阶段增加 API Key 或 Basic Auth 认证。

---

## 📄 开源许可证

本项目采用 [MIT License](LICENSE) 授权开源。欢迎提 Issue 与 PR！
