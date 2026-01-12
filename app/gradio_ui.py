# app/gradio_ui.py
import gradio as gr
import requests
import json
import uuid

API = "http://localhost:8000/chat/stream"


def chat(message, history):
    # 为每次对话创建一个固定的session_id，确保在同一会话中保持一致性
    session_id = getattr(chat, 'session_id', None)
    if session_id is None:
        session_id = str(uuid.uuid4())
        chat.session_id = session_id
    
    resp = requests.post(
        API,
        stream=True,
        json={"query": message, "session_id": session_id},
        headers={"Content-Type": "application/json"},
    )
    buffer = ""
    for line in resp.iter_lines(decode_unicode=True):
        if line.startswith("data:"):
            chunk = json.loads(line[5:])["content"]
            buffer += chunk
            yield gr.ChatMessage(role="assistant", content=buffer)


gradio_app = gr.ChatInterface(chat,type='messages', title="FastAPI-Agent Chat")
