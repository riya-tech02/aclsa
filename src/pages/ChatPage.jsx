import { useState } from "react";
import { sendMessage } from "../api/agentApi";
import ChatWindow from "../components/Chat/ChatWindow";
import InputBox from "../components/Chat/InputBox";
import AnalysisPanel from "../features/analysis/AnalysisPanel";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { role: "agent", text: "Hello. I am ACLSA, your AI agent." }
  ]);
  const [analysis, setAnalysis] = useState(null);

  async function handleSend(text) {
    setMessages(prev => [...prev, { role: "user", text }]);
    const res = await sendMessage("riya", text);

    if (typeof res.response === "string") {
      setMessages(prev => [...prev, { role: "agent", text: res.response }]);
    } else {
      setMessages(prev => [...prev, { role: "agent", text: "Here is my analysis." }]);
      setAnalysis(res.response);
    }
  }

  return (
    <div className="page">
      <ChatWindow messages={messages} />
      <AnalysisPanel data={analysis} />
      <InputBox onSend={handleSend} />
    </div>
  );
}
