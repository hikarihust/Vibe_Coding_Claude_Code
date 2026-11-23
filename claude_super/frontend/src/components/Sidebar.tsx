import type { Session } from "../api";
import SessionItem from "./SessionItem";

type Props = {
  sessions: Session[];
  activeId: number | null;
  open: boolean;
  onClose: () => void;
  onNewChat: () => void;
  onSelect: (id: number) => void;
  onRename: (id: number, title: string) => void;
  onDelete: (id: number) => void;
};

export default function Sidebar({
  sessions,
  activeId,
  open,
  onClose,
  onNewChat,
  onSelect,
  onRename,
  onDelete,
}: Props) {
  return (
    <>
      {open && (
        <div
          onClick={onClose}
          aria-hidden="true"
          className="fixed inset-0 z-30 bg-neutral-900/50 md:hidden"
        />
      )}
      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-64 shrink-0 flex-col border-r border-neutral-200 bg-neutral-50 transition-transform md:static md:z-auto md:translate-x-0 dark:border-neutral-600 dark:bg-neutral-900 ${
          open ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="p-3">
          <button
            type="button"
            onClick={onNewChat}
            className="w-full rounded-md bg-brand-500 px-4 py-2 text-sm font-medium text-white hover:bg-brand-600"
          >
            + New Chat
          </button>
        </div>
        <ul className="flex-1 space-y-1 overflow-y-auto px-2 pb-3">
          {sessions.map((s) => (
            <SessionItem
              key={s.id}
              session={s}
              active={s.id === activeId}
              onSelect={() => onSelect(s.id)}
              onRename={(title) => onRename(s.id, title)}
              onDelete={() => onDelete(s.id)}
            />
          ))}
        </ul>
      </aside>
    </>
  );
}
