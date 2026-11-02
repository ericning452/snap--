import argparse
import asyncio
import base64
import io
import os
import sys
from mss import mss
from PIL import Image
import websockets

def capture_screen(monitor_idx: int = 1, quality: int = 70) -> str:
    """截取指定屏幕并压缩转换为 Base64 编码的 JPEG 字符串"""
    with mss() as sct:
        if monitor_idx >= len(sct.monitors):
            monitor_idx = 1
        monitor = sct.monitors[monitor_idx]
        grab_img = sct.grab(monitor)
        img = Image.frombytes("RGB", grab_img.size, grab_img.bgra, "raw", "BGRX")

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality)
        return base64.b64encode(buf.getvalue()).decode()

async def run_client(ws_url: str, monitor_idx: int = 1, quality: int = 70):
    print(f"[*] 准备连接服务器: {ws_url}")
    while True:
        try:
            async with websockets.connect(ws_url) as ws:
                print("✅ 已成功连接到 WebSocket 服务器，等待截屏指令...")
                while True:
                    msg = await ws.recv()
                    if msg == "capture":
                        print("📸 收到截屏指令，正在截屏...")
                        base64_data = capture_screen(monitor_idx, quality)
                        await ws.send(base64_data)
                        print("🚀 截屏数据已发送成功")
        except (websockets.exceptions.ConnectionClosed, OSError) as e:
            print(f"⚠️ 连接断开或连接失败: {e}，3 秒后尝试重连...")
            await asyncio.sleep(3)
        except asyncio.CancelledError:
            print("\n客户端已安全退出。")
            break
        except Exception as e:
            print(f"❌ 运行异常: {e}，3 秒后重试...")
            await asyncio.sleep(3)

def main():
    default_url = os.getenv("WS_URL", "ws://localhost:8000/ws")

    parser = argparse.ArgumentParser(description="Snap Demo 截屏客户端代理")
    parser.add_argument("--url", default=default_url, help=f"WebSocket 服务器地址 (默认: {default_url})")
    parser.add_argument("--monitor", type=int, default=1, help="截取的显示器序号 (默认: 1 为主屏幕)")
    parser.add_argument("--quality", type=int, default=70, help="图片压缩质量 1-100 (默认: 70)")
    args = parser.parse_args()

    try:
        asyncio.run(run_client(args.url, args.monitor, args.quality))
    except KeyboardInterrupt:
        print("\n用户手动终止程序。")

if __name__ == "__main__":
    main()
