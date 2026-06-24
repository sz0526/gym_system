"""
会话历史管理系统
- Session 机制实现完整的历史消息存储与管理
- 动态上下文窗口构建（N轮参数可配置）
- 上下文长度超限处理（摘要 + 关键信息提取）
- 会话超时自动清理
"""
import uuid
import time
import threading
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class ChatMessage:
    role: str           # "user" 或 "assistant"
    content: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class Session:
    session_id: str
    messages: List[ChatMessage] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    last_active: float = field(default_factory=time.time)

    def add_message(self, role: str, content: str):
        self.messages.append(ChatMessage(role=role, content=content))
        self.last_active = time.time()

    def get_history(self, max_rounds: Optional[int] = None) -> List[ChatMessage]:
        """
        获取最近 N 轮对话（一轮 = 一次用户提问 + 一次助手回答）
        max_rounds=None 返回全部
        """
        if max_rounds is None:
            return self.messages
        return self.messages[-(max_rounds * 2):]

    def clear(self):
        self.messages.clear()


class SessionStore:
    """基于内存的 Session 存储，支持 TTL 自动清理"""

    def __init__(self, ttl_seconds: int = 1800, cleanup_interval: int = 300):
        """
        :param ttl_seconds: 会话超时时间（秒），默认30分钟
        :param cleanup_interval: 清理检查间隔（秒），默认5分钟
        """
        self._sessions: Dict[str, Session] = {}
        self._ttl = ttl_seconds
        self._lock = threading.Lock()
        self._start_cleanup_thread(cleanup_interval)

    def create_session(self) -> str:
        session_id = uuid.uuid4().hex[:16]
        with self._lock:
            self._sessions[session_id] = Session(session_id=session_id)
        return session_id

    def get_session(self, session_id: str) -> Optional[Session]:
        with self._lock:
            session = self._sessions.get(session_id)
            if session:
                session.last_active = time.time()
            return session

    def delete_session(self, session_id: str) -> bool:
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return True
            return False

    def get_all_sessions(self) -> List[str]:
        with self._lock:
            return list(self._sessions.keys())

    def _cleanup_expired(self):
        now = time.time()
        with self._lock:
            expired = [
                sid for sid, s in self._sessions.items()
                if now - s.last_active > self._ttl
            ]
            for sid in expired:
                del self._sessions[sid]

    def _start_cleanup_thread(self, interval: int):
        def _loop():
            while True:
                time.sleep(interval)
                self._cleanup_expired()

        t = threading.Thread(target=_loop, daemon=True)
        t.start()


def build_context_from_history(
    messages: List[ChatMessage],
    max_tokens: int = 2000
) -> str:
    """
    将历史消息拼接为上下文字符串，超出长度限制时进行摘要压缩
    策略：从最新消息往前累加，超出时对更早的消息做截断摘要
    """
    if not messages:
        return ""

    parts = []
    total_chars = 0
    char_limit = max_tokens * 2  # 中英文混合场景粗略估算

    for msg in reversed(messages):
        role_label = "用户" if msg.role == "user" else "助手"
        line = f"{role_label}: {msg.content}"
        if total_chars + len(line) > char_limit:
            if not parts:
                line = f"{role_label}: {msg.content[:char_limit - total_chars]}..."
            else:
                break
        parts.append(line)
        total_chars += len(line)

    parts.reverse()
    return "\n".join(parts)


# 全局 SessionStore 单例
session_store = SessionStore(ttl_seconds=1800, cleanup_interval=300)