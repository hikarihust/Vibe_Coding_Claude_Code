import { useTheme } from "../useTheme";

export default function Header({ onMenuClick }: { onMenuClick: () => void }) {
  const { theme, toggle } = useTheme();
  const isDark = theme === "dark";

  return (
    <header className="flex h-14 shrink-0 items-center gap-2 border-b border-neutral-200 bg-neutral-0 px-4 dark:border-neutral-600 dark:bg-neutral-900">
      <button
        type="button"
        onClick={onMenuClick}
        aria-label="Mở danh sách chat"
        className="rounded-md p-2 text-xl leading-none hover:bg-neutral-100 md:hidden dark:hover:bg-neutral-600"
      >
        ☰
      </button>
      <h1 className="flex-1 truncate text-lg font-semibold">AI Coding's Chatbot</h1>
      <button
        type="button"
        onClick={toggle}
        aria-label={isDark ? "Chuyển sang light mode" : "Chuyển sang dark mode"}
        title={isDark ? "Chuyển sang light mode" : "Chuyển sang dark mode"}
        className="rounded-md p-2 text-lg leading-none hover:bg-neutral-100 dark:hover:bg-neutral-600"
      >
        {isDark ? "☀️" : "🌙"}
      </button>
    </header>
  );
}
