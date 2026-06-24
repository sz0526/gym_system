export function createChatStream(
  message: string,
  onMessage: (text: string) => void,
  onError?: () => void
) {
  const memberAccount = localStorage.getItem('memberAccount') ?? '';

  const params = new URLSearchParams({
    content: message,
    memberAccount   // 带上用户账号
  });

  const es = new EventSource("/api/chat/stream?" + params.toString());

  let fullText = "";

  es.onmessage = (event) => {
    if (!event.data) return;
    fullText += event.data;
    onMessage(fullText);
  };

  es.onerror = (err) => {
    console.error("SSE error:", err);
    es.close();
    onError?.();
  };

  return es;
}