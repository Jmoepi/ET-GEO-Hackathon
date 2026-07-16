import { useState, useRef, useEffect } from "react";
import { useCopilotChat } from "@/hooks/useApi";
import { Send, Bot, User, Loader2 } from "lucide-react";
import { cn } from "@/utils/lib";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export function CopilotPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hello! I'm the VineMind AI Copilot. I can explain irrigation recommendations, compare vineyard blocks, and summarise stress trends. I never generate irrigation advice myself — I only interpret data from the Decision Intelligence Engine.\n\nTry asking:\n- Why should I irrigate Block A12?\n- What are the current stress trends?\n- Compare blocks A12 and B05",
    },
  ]);
  const [input, setInput] = useState("");
  const chat = useCopilotChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || chat.isPending) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text }]);

    try {
      const res = await chat.mutateAsync(text);
      setMessages((prev) => [...prev, { role: "assistant", content: res.answer }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, I encountered an error processing your request. Please try again." },
      ]);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-120px)]">
      <div className="mb-4">
        <h1 className="text-2xl font-bold text-text-primary">AI Copilot</h1>
        <p className="text-text-secondary mt-1">Ask questions about vineyard irrigation data</p>
      </div>

      <div className="flex-1 bg-surface-card rounded-xl border border-surface-border flex flex-col overflow-hidden">
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, i) => (
            <div key={i} className={cn("flex gap-3", msg.role === "user" ? "justify-end" : "justify-start")}>
              {msg.role === "assistant" && (
                <div className="w-8 h-8 rounded-full bg-vineyard-500/20 flex items-center justify-center shrink-0">
                  <Bot className="w-4 h-4 text-vineyard-500" />
                </div>
              )}
              <div
                className={cn(
                  "max-w-[70%] rounded-xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap",
                  msg.role === "user"
                    ? "bg-vineyard-500/20 text-text-primary"
                    : "bg-surface text-text-primary"
                )}
              >
                {msg.content}
              </div>
              {msg.role === "user" && (
                <div className="w-8 h-8 rounded-full bg-surface-border flex items-center justify-center shrink-0">
                  <User className="w-4 h-4 text-text-muted" />
                </div>
              )}
            </div>
          ))}
          {chat.isPending && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-full bg-vineyard-500/20 flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4 text-vineyard-500" />
              </div>
              <div className="bg-surface rounded-xl px-4 py-3">
                <Loader2 className="w-4 h-4 text-text-muted animate-spin" />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-4 border-t border-surface-border">
          <div className="flex gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Ask about vineyard stress, recommendations, or trends..."
              className="flex-1 bg-surface-input border border-surface-border rounded-lg px-4 py-2.5 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-vineyard-500/50"
              disabled={chat.isPending}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || chat.isPending}
              className="px-4 py-2.5 bg-vineyard-500 text-white rounded-lg text-sm font-medium hover:bg-vineyard-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
          <p className="text-xs text-text-muted mt-2">
            Responses are based on Decision Evidence Packages only. The Copilot never generates irrigation advice.
          </p>
        </div>
      </div>
    </div>
  );
}
