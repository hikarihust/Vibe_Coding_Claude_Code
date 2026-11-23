import { useLayoutEffect, useRef, useState } from "react";

const MAX_HEIGHT = 200;

export default function Composer({ disabled, onSend }: { disabled: boolean; onSend: (text: string) => void }) {
  const [text, setText] = useState("");
  const ref = useRef<HTMLTextAreaElement>(null);
  const canSend = !disabled && text.trim() !== "";

  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, MAX_HEIGHT)}px`;
  }, [text]);

  const send = () => {
    if (!canSend) return;
    onSend(text.trim());
    setText("");
  };

  return (
    <div className="border-t border-neutral-200 bg-neutral-0 dark:border-neutral-600 dark:bg-neutral-900">
      <form
        className="mx-auto flex max-w-3xl items-end gap-2 px-4 py-3"
        onSubmit={(e) => {
          e.preventDefault();
          send();
        }}
      >
        <textarea
          ref={ref}
          rows={1}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            // Bỏ qua Enter khi bộ gõ (Unikey/IME) đang soạn chữ có dấu.
            if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) {
              e.preventDefault();
              send();
            }
          }}
          placeholder="Nhập câu hỏi... (Enter để gửi, Shift+Enter để xuống dòng)"
          aria-label="Nội dung tin nhắn"
          className="min-h-10 flex-1 resize-none overflow-y-auto rounded-md border border-neutral-300 bg-neutral-0 px-3 py-2 outline-none focus:border-brand-500 dark:border-neutral-600 dark:bg-neutral-900"
        />
        <button
          type="submit"
          disabled={!canSend}
          className="h-10 rounded-md bg-brand-500 px-4 font-medium text-white hover:bg-brand-600 disabled:cursor-not-allowed disabled:bg-neutral-300 dark:disabled:bg-neutral-600"
        >
          Send
        </button>
      </form>
    </div>
  );
}
