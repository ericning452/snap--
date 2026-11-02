import argparse
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="Snap Demo Server")

# 保存所有活动的 WebSocket 连接
connections: set[WebSocket] = set()

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.add(websocket)
    try:
        while True:
            msg = await websocket.receive_text()
            # 广播消息给其他所有客户端
            # 例如：前端发送 "capture" -> 转发给 pc_service；pc_service 发送 base64 图片 -> 转发给前端
            for conn in list(connections):
                if conn != websocket:
                    try:
                        await conn.send_text(msg)
                    except Exception:
                        pass
    except WebSocketDisconnect:
        pass
    finally:
        connections.discard(websocket)

# 确保 static 目录存在并挂载静态前端
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Snap Demo WebSocket & Web Server")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址 (默认: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="监听端口 (默认: 8000)")
    args = parser.parse_args()

    print(f"🚀 服务已启动: http://{args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)
