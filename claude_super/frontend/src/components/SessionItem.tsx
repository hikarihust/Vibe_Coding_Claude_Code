import { useEffect, useRef, useState } from "react";
import type { Session } from "../api";

type Props = {
  session: Session;
  active: boolean;
  onSelect: () => void;
  onRename: (title: string) => void;
  onDelete: () => void;
};

export default function SessionItem({ session, active, onSelect, onRename, onDelete }: Props) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(session.title);
  const rootRef = useRef<HTMLLIElement>(null);
  // Chặn blur lưu tên sau khi đã Enter/Esc (input bị gỡ khỏi DOM vẫn có thể bắn blur).
  const doneRef = useRef(false);

  useEffect(() => {
    if (!menuOpen) return;
    const onPointer = (e: PointerEvent) => {
      if (!rootRef.current?.contains(e.target as Node)) setMenuOpen(false);
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setMenuOpen(false);
    };
    document.addEventListener("pointerdown", onPointer);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("pointerdown", onPointer);
      document.removeEventListener("keydown", onKey);
    };
  }, [menuOpen]);

  const startEditing = () => {
    setMenuOpen(false);
    setDraft(session.title);
    doneRef.current = false;
    setEditing(true);
  };

  const cancel = () => {
    doneRef.current = true;
    setEditing(false);
  };

  const commit = () => {
    if (doneRef.current) return;
    doneRef.current = true;
    setEditing(false);
    const title = draft.trim();
    if (title && title !== session.title) onRename(title);
  };

  if (editing) {
    return (
      <li className="px-2 py-1">
        <input
          autoFocus
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onBlur={commit}
          onKeyDown={(e) => {
            if (e.key === "Enter") commit();
            if (e.key === "Escape") cancel();
          }}
          aria-label="Tên session"
          className="w-full rounded-md border border-brand-500 bg-neutral-0 px-2 py-1 text-sm outline-none dark:bg-neutral-900"
        />
      </li>
    );
  }

  return (
    <li ref={rootRef} className="group relative">
      <div
        className={`flex items-center rounded-md ${
          active
            ? "bg-neutral-200 dark:bg-neutral-600"
            : "hover:bg-neutral-100 dark:hover:bg-neutral-600/60"
        }`}
      >
        <button
          type="button"
          onClick={onSelect}
          title={session.title}
          className="min-w-0 flex-1 truncate px-3 py-2 text-left text-sm"
        >
          {session.title}
        </button>
        <button
          type="button"
          aria-label="Tuỳ chọn"
          aria-haspopup="menu"
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((o) => !o)}
          className={`mr-1 rounded px-2 py-1 text-sm leading-none text-neutral-500 hover:bg-neutral-200 focus:opacity-100 dark:text-neutral-300 dark:hover:bg-neutral-500 ${
            menuOpen ? "opacity-100" : "md:opacity-0 md:group-hover:opacity-100"
          }`}
        >
          ...
        </button>
      </div>
      {menuOpen && (
        <div
          role="menu"
          className="absolute right-1 top-full z-20 mt-1 w-32 overflow-hidden rounded-md border border-neutral-200 bg-neutral-0 py-1 text-sm shadow-lg dark:border-neutral-600 dark:bg-neutral-900"
        >
          <button
            type="button"
            role="menuitem"
            onClick={startEditing}
            className="block w-full px-3 py-2 text-left hover:bg-neutral-100 dark:hover:bg-neutral-600"
          >
            Đổi tên
          </button>
          <button
            type="button"
            role="menuitem"
            onClick={() => {
              setMenuOpen(false);
              onDelete();
            }}
            className="block w-full px-3 py-2 text-left text-danger-600 hover:bg-danger-100 dark:text-danger-500 dark:hover:bg-neutral-600"
          >
            Xoá
          </button>
        </div>
      )}
    </li>
  );
}
