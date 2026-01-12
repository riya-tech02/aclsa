import { useState } from "react";

export default function InputBox({ onSend }) {
  const [text, setText] = useState("");

  function send() {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  }

  return (
    <div className="input-box">
      <input
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="Talk to ACLSA..."
        onKeyDown={e => e.key === "Enter" && send()}
      />
      <button onClick={send}>Send</button>
    </div>
  );
}
