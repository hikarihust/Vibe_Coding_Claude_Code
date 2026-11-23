import ReactMarkdown from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import remarkGfm from "remark-gfm";
import type { ChatMessage } from "../App";

const MARKDOWN_STYLES = [
  "[&_p]:my-2 [&_ul]:my-2 [&_ul]:list-disc [&_ul]:pl-6 [&_ol]:my-2 [&_ol]:list-decimal [&_ol]:pl-6",
  "[&_h1]:my-3 [&_h1]:text-xl [&_h1]:font-semibold [&_h2]:my-3 [&_h2]:text-lg [&_h2]:font-semibold [&_h3]:my-2 [&_h3]:font-semibold",
  "[&_a]:text-brand-500 [&_a]:underline [&_blockquote]:border-l-4 [&_blockquote]:border-neutral-300 [&_blockquote]:pl-3",
  "[&_pre]:my-3 [&_pre]:overflow-x-auto [&_pre]:rounded-md [&_pre]:bg-[#0d1117] [&_pre]:p-3 [&_pre]:text-sm",
  "[&_code]:font-mono [&_:not(pre)>code]:rounded [&_:not(pre)>code]:bg-neutral-200 [&_:not(pre)>code]:px-1 dark:[&_:not(pre)>code]:bg-neutral-600",
  "[&_table]:my-3 [&_table]:border-collapse [&_th]:border [&_th]:border-neutral-300 [&_th]:px-2 [&_td]:border [&_td]:border-neutral-300 [&_td]:px-2",
].join(" ");

function TypingDots() {
  return (
    <span className="inline-flex gap-1 py-2" aria-label="Đang trả lời">
      {[0, 150, 300].map((delay) => (
        <span
          key={delay}
          className="h-2 w-2 animate-bounce rounded-full bg-neutral-400"
          style={{ animationDelay: `${delay}ms` }}
        />
      ))}
    </span>
  );
}

export default function MessageBubble({ message, typing }: { message: ChatMessage; typing: boolean }) {
  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[85%] whitespace-pre-wrap break-words rounded-2xl bg-brand-500 px-4 py-2 text-white">
          {message.content}
        </div>
      </div>
    );
  }

  if (message.error) {
    return (
      <div
        role="alert"
        className="rounded-md border border-danger-500 bg-danger-100 px-4 py-2 text-danger-600 dark:bg-transparent dark:text-danger-500"
      >
        ⚠ {message.content}
      </div>
    );
  }

  return (
    <div className="max-w-full break-words">
      {typing && message.content === "" ? (
        <TypingDots />
      ) : (
        <div className={MARKDOWN_STYLES}>
          <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]}>
            {message.content}
          </ReactMarkdown>
        </div>
      )}
    </div>
  );
}
