export type Session = { id: number; title: string; updated_at: string };
export type Message = {
  id: number;
  role: "user" | "assistant";
  content: string;
  created_at: string;
};

async function request(path: string, init?: RequestInit): Promise<Response> {
  const res = await fetch(`/api${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!res.ok) {
    let message = `HTTP ${res.status}`;
    try {
      const data = await res.json();
      if (typeof data?.detail === "string") message = data.detail;
    } catch {
      // body không phải JSON: giữ thông báo HTTP status
    }
    throw new Error(message);
  }
  return res;
}

export async function listSessions(): Promise<Session[]> {
  return (await request("/sessions")).json();
}

export async function createSession(firstMessage: string): Promise<Session> {
  const res = await request("/sessions", {
    method: "POST",
    body: JSON.stringify({ first_message: firstMessage }),
  });
  return res.json();
}

export async function listMessages(sessionId: number): Promise<Message[]> {
  return (await request(`/sessions/${sessionId}/messages`)).json();
}

export async function renameSession(sessionId: number, title: string): Promise<Session> {
  const res = await request(`/sessions/${sessionId}`, {
    method: "PATCH",
    body: JSON.stringify({ title }),
  });
  return res.json();
}

export async function deleteSession(sessionId: number): Promise<void> {
  await request(`/sessions/${sessionId}`, { method: "DELETE" });
}

export async function streamMessage(
  sessionId: number,
  content: string,
  onChunk: (text: string) => void,
  signal: AbortSignal,
): Promise<void> {
  const res = await request(`/sessions/${sessionId}/messages`, {
    method: "POST",
    body: JSON.stringify({ content }),
    signal,
  });
  if (!res.body) throw new Error("Không nhận được dữ liệu stream");
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const text = decoder.decode(value, { stream: true });
    if (text) onChunk(text);
  }
  const rest = decoder.decode();
  if (rest) onChunk(rest);
}
