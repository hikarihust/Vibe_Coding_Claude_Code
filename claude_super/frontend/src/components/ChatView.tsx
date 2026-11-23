import { useEffect, useRef } from "react";
import type { ChatMessage } from "../App";
import MessageBubble from "./MessageBubble";

export default function ChatView({ messages, streaming }: { messages: ChatMessage[]; streaming: boolean }) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ block: "end" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="mx-auto flex max-w-3xl flex-col gap-4 px-4 py-6">
        {messages.length === 0 ? (
          <p className="mt-24 text-center text-xl text-neutral-500 dark:text-neutral-300">
            Bạn muốn hỏi gì hôm nay?
          </p>
        ) : (
          messages.map((m, i) => (
            <MessageBubble key={m.key} message={m} typing={streaming && i === messages.length - 1} />
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
