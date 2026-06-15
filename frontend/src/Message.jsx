export default function Message({ role, content }) {
  const isBot = role === "assistant";

  return (
    <div className={`message ${isBot ? "bot" : "user"}`}>
      {isBot && <img src="/avatar.png" alt="CareerCompass AI" className="msg-avatar-img" />}
      <div className="bubble">
        {content.split("\n").map((line, i) => (
          <span key={i}>
            {line}
            {i < content.split("\n").length - 1 && <br />}
          </span>
        ))}
      </div>
    </div>
  );
}