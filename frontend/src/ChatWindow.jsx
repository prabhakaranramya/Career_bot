import { useState, useRef, useEffect } from "react";
import Message from "./Message";

const SUGGESTED_PROMPTS = [
  "I want to switch to data science",
  "How do I become a software engineer?",
  "What skills should I learn for AI?",
  "I need a career roadmap",
];

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [userName, setUserName] = useState(null);
  const [userId] = useState("default_user");
  const [chatTitle] = useState("New Chat");
  const bottomRef = useRef(null);

  // Get time of day greeting
  const getTimeGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return "Good morning";
    if (hour < 18) return "Good afternoon";
    return "Good evening";
  };

  // Generate welcome message
  const getWelcomeMessage = (name) => {
    const timeGreeting = getTimeGreeting();
    return {
      role: "assistant",
      content: name
        ? `${timeGreeting}, ${name}! 👋 I'm CareerCompass AI, your personal career guide. I'm here to help you grow, switch careers, or figure out what skills to build next.\n\nWhat's on your mind career-wise today?`
        : `${timeGreeting}! 👋 I'm CareerCompass AI, your personal career guide. Before we start, what's your name?`,
    };
  };

  useEffect(() => {
    loadPreviousChat();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const loadPreviousChat = async () => {
    try {
      const res = await fetch("http://localhost:8000/load-chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId }),
      });
      const data = await res.json();
      if (data.history && data.history.length > 0) {
        setMessages(data.history);
        // Extract name from first user message if it exists
        const firstUserMsg = data.history.find(m => m.role === "user");
        if (firstUserMsg && !userName) {
          setUserName(firstUserMsg.content);
        }
      } else {
        // No previous chat, show welcome
        setMessages([getWelcomeMessage(null)]);
      }
    } catch (err) {
      console.error("Could not load previous chat:", err);
      setMessages([getWelcomeMessage(null)]);
    }
  };

  const sendMessage = async (text) => {
    const userText = text || input.trim();
    if (!userText) return;

    // If no name yet, first message is the user's name
    let processedUserName = userName;
    if (!userName && messages.length <= 1) {
      setUserName(userText);
      processedUserName = userText;
    }

    const newMessages = [...messages, { role: "user", content: userText }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userText,
          history: newMessages.slice(0, -1),
          user_id: userId,
          chat_title: chatTitle,
        }),
      });
      const data = await res.json();
      
      // If we just got the name, add a personalized greeting
      if (!userName && messages.length <= 1) {
        const personalizedGreeting = getWelcomeMessage(processedUserName);
        setMessages([
          ...newMessages,
          personalizedGreeting,
          { role: "assistant", content: data.reply }
        ]);
      } else {
        setMessages([...newMessages, { role: "assistant", content: data.reply }]);
      }
    } catch (err) {
      console.error("Error:", err);
      setMessages([...newMessages, {
        role: "assistant",
        content: "Sorry, I'm having trouble connecting. Make sure the backend is running on http://localhost:8000",
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    if (window.confirm("Clear chat from screen? Your data is saved in the database and can be recovered.")) {
      setMessages([getWelcomeMessage(null)]);
      setUserName(null);
    }
  };

  return (
    <div className="chat-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <img src="/avatar.png" alt="CareerCompass AI" className="sidebar-avatar-img" />
        <h2 className="sidebar-name">CareerCompass AI</h2>
        <p className="sidebar-role">Career Guide</p>
        <div className="sidebar-divider" />
        {userName && (
          <>
            <p className="sidebar-label">Your Profile</p>
            <div className="user-profile">
              <p className="user-name">{userName}</p>
            </div>
            <div className="sidebar-divider" />
          </>
        )}
        <p className="sidebar-label">Quick prompts</p>
        {SUGGESTED_PROMPTS.map((prompt) => (
          <button
            key={prompt}
            className="prompt-chip"
            onClick={() => sendMessage(prompt)}
            disabled={!userName}
          >
            {prompt}
          </button>
        ))}
      </aside>

      {/* Main chat */}
      <main className="chat-main">
        <div className="chat-header">
          <span className="online-dot" />
          <span>CareerCompass AI is online</span>
          <button className="clear-btn" onClick={clearChat} title="Clear chat from screen (data stays in database)">
            🗑️ Clear
          </button>
        </div>

        <div className="messages-area">
          {messages.map((msg, i) => (
            <Message key={i} role={msg.role} content={msg.content} />
          ))}
          {loading && (
            <div className="message bot">
              <img src="/avatar.png" alt="CareerCompass AI" className="msg-avatar-img" />
              <div className="bubble typing">
                <span /><span /><span />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="input-area">
          <textarea
            className="chat-input"
            placeholder={userName ? "Ask CareerCompass AI anything about your career..." : "Enter your name..."}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
            rows={1}
          />
          <button
            className="send-btn"
            onClick={() => sendMessage()}
            disabled={loading || !input.trim()}
          >
            ➤
          </button>
        </div>
      </main>
    </div>
  );
}