import { useCallback, useEffect, useState } from "react";
import { deleteSession, listSessions, renameSession, type Session } from "./api";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";

export default function App() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeId, setActiveId] = useState<number | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

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

  const newChat = () => {
    setActiveId(null);
    setSidebarOpen(false);
  };

  const selectSession = (id: number) => {
    setActiveId(id);
    setSidebarOpen(false);
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
        <main className="flex min-w-0 flex-1 flex-col" />
      </div>
    </div>
  );
}
