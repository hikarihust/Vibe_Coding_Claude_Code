import { useCallback, useEffect, useRef, useState } from "react";
import {
  createSession,
  deleteSession,
  listMessages,
  listSessions,
  renameSession,
  streamMessage,
  type Session,
} from "./api";
import ChatView from "./components/ChatView";
import Composer from "./components/Composer";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";

export type ChatMessage = {
  key: string;
  role: "user" | "assistant";
  content: string;
  error?: boolean;
};

let localKey = 0;
const nextKey = () => `local-${++localKey}`;

export default function App() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeId, setActiveId] = useState<number | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [streaming, setStreaming] = useState(false);
  const abortRef = useRef<AbortController | null>(null);
  // Tăng mỗi lần đổi khung chat, để bỏ kết quả load lịch sử đến muộn.
  const viewRef = useRef(0);

  const refreshSessions = useCallback(async () => {
    try {
      setSessions(await listSessions());
    } catch (err) {
      console.error(err);
    }
  }, []);

  useEffect(() => {
    void refreshSessions();
  }, [refreshSessions]);

  const stopStreaming = () => {
    abortRef.current?.abort();
    abortRef.current = null;
    setStreaming(false);
  };

  const newChat = () => {
    stopStreaming();
    viewRef.current++;
    setActiveId(null);
    setMessages([]);
    setSidebarOpen(false);
  };

  const selectSession = async (id: number) => {
    // Bấm lại session đang mở không được huỷ câu trả lời đang stream.
    if (id === activeId) {
      setSidebarOpen(false);
      return;
    }
    stopStreaming();
    const view = ++viewRef.current;
    setActiveId(id);
    setMessages([]);
    setSidebarOpen(false);
    try {
      const loaded = await listMessages(id);
      if (view !== viewRef.current) return;
      setMessages(loaded.map((m) => ({ key: `m-${m.id}`, role: m.role, content: m.content })));
    } catch (err) {
      if (view !== viewRef.current) return;
      setMessages([{ key: nextKey(), role: "assistant", content: (err as Error).message, error: true }]);
    }
  };

  const send = async (text: string) => {
    const controller = new AbortController();
    abortRef.current = controller;
    setStreaming(true);

    const replyKey = nextKey();
    const updateReply = (fn: (m: ChatMessage) => ChatMessage) =>
      setMessages((list) => list.map((m) => (m.key === replyKey ? fn(m) : m)));

    setMessages((list) => [
      ...list,
      { key: nextKey(), role: "user", content: text },
      { key: replyKey, role: "assistant", content: "" },
    ]);

    try {
      let sessionId = activeId;
      if (sessionId === null) {
        const created = await createSession(text);
        if (controller.signal.aborted) return;
        setSessions((list) => [created, ...list]);
        setActiveId(created.id);
        sessionId = created.id;
      }
      await streamMessage(
        sessionId,
        text,
        (chunk) => {
          if (!controller.signal.aborted) updateReply((m) => ({ ...m, content: m.content + chunk }));
        },
        controller.signal,
      );
      if (!controller.signal.aborted) void refreshSessions();
    } catch (err) {
      if (controller.signal.aborted) return;
      // Câu trả lời dở dang không được lưu ở backend, nên thay hẳn bằng thông báo lỗi.
      updateReply((m) => ({ ...m, content: (err as Error).message, error: true }));
    } finally {
      if (abortRef.current === controller) {
        abortRef.current = null;
        setStreaming(false);
      }
    }
  };

  const handleRename = async (id: number, title: string) => {
    try {
      const updated = await renameSession(id, title);
      setSessions((list) => list.map((s) => (s.id === id ? updated : s)));
    } catch (err) {
      window.alert((err as Error).message);
    }
  };

  const handleDelete = async (id: number) => {
    const session = sessions.find((s) => s.id === id);
    if (!session || !window.confirm(`Xoá "${session.title}"?`)) return;
    try {
      await deleteSession(id);
      setSessions((list) => list.filter((s) => s.id !== id));
      if (id === activeId) newChat();
    } catch (err) {
      window.alert((err as Error).message);
    }
  };

  return (
    <div className="flex h-full flex-col bg-neutral-0 font-sans text-neutral-900 dark:bg-neutral-900 dark:text-neutral-50">
      <Header onMenuClick={() => setSidebarOpen(true)} />
      <div className="flex min-h-0 flex-1">
        <Sidebar
          sessions={sessions}
          activeId={activeId}
          open={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          onNewChat={newChat}
          onSelect={selectSession}
          onRename={handleRename}
          onDelete={handleDelete}
        />
        <main className="flex min-w-0 flex-1 flex-col">
          <ChatView messages={messages} streaming={streaming} />
          <Composer disabled={streaming} onSend={send} />
        </main>
      </div>
    </div>
  );
}
