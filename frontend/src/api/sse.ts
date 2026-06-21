export function createChatStream(
  message: string,
  onMessage: (text: string) => void,
  onError?: () => void
) {
  const es = new EventSource(
    "http://localhost:9000/api/chat/stream?message=" + encodeURIComponent(message)
  );

  let fullText = "";

  es.onmessage = (event) => {
    fullText += event.data;
    onMessage(fullText);
  };

  es.onerror = () => {
    es.close();
    onError?.();
  };

  return es;
}