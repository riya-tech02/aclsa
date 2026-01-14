import { useState } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";

const API = import.meta.env.VITE_API_URL || "https://aclsa-agent.onrender.com";

export default function App() {
  const [messages, setMessages] = useState([
    { role: "agent", text: "Hello! I'm ACLSA, your AI-powered Course Learning Support Assistant. How can I help you today?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [auth, setAuth] = useState(true);  // Skip login for now
  const [mode, setMode] = useState("login");
  
  async function sendMessage() {
    if (!input.trim()) return;
    
    const userText = input;
    setMessages(m => [...m, { role: "user", text: userText }]);
    setInput("");
    setLoading(true);
    
    try {
      const res = await fetch(`${API}/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          user_id: localStorage.getItem("userId") || "user_" + Date.now(),
          message: userText,
          context: null
        })
      });
      
      const data = await res.json();
      
      if (data.response) {
        setMessages(m => [...m, { role: "agent", text: data.response }]);
      } else {
        setMessages(m => [...m, { 
          role: "agent", 
          text: "I apologize, but I didn't receive a proper response. Please try again." 
        }]);
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages(m => [...m, { 
        role: "agent", 
        text: "I'm having trouble connecting. Please check your internet connection and try again." 
      }]);
    } finally {
      setLoading(false);
    }
  }

  if (!auth) {
    return mode === "login" ? (
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100vh", background: "#020617" }}>
        <Login onLogin={() => setAuth(true)} />
        <p style={{ color: "#38bdf8", cursor: "pointer", marginTop: 10 }} onClick={() => setMode("register")}>
          Create account
        </p>
      </div>
    ) : (
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100vh", background: "#020617" }}>
        <Register onRegister={() => setMode("login")} />
        <p style={{ color: "#38bdf8", cursor: "pointer", marginTop: 10 }} onClick={() => setMode("login")}>
          Back to login
        </p>
      </div>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", background: "#020617", color: "#e5e7eb" }}>
      {/* Header */}
      <div style={{ padding: 20, borderBottom: "1px solid #1e293b", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2 style={{ margin: 0 }}>ACLSA Agent</h2>
        <button 
          onClick={() => {
            localStorage.removeItem("token");
            setAuth(false);
          }}
          style={{ padding: "8px 16px", borderRadius: 8, background: "#ef4444", color: "white", border: "none", cursor: "pointer" }}
        >
          Logout
        </button>
      </div>

      {/* Chat area */}
      <div style={{ flex: 1, padding: 20, overflowY: "auto", display: "flex", flexDirection: "column" }}>
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              maxWidth: "70%",
              padding: 16,
              marginBottom: 12,
              borderRadius: 12,
              background: m.role === "user" ? "#38bdf8" : "#1e293b",
              color: m.role === "user" ? "#000" : "#fff",
              alignSelf: m.role === "user" ? "flex-end" : "flex-start",
              boxShadow: "0 2px 8px rgba(0,0,0,0.3)"
            }}
          >
            <pre style={{ 
              whiteSpace: "pre-wrap", 
              wordWrap: "break-word",
              margin: 0,
              fontFamily: "inherit",
              fontSize: "14px",
              lineHeight: "1.5"
            }}>
              {m.text}
            </pre>
          </div>
        ))}
        
        {loading && (
          <div style={{
            maxWidth: "70%",
            padding: 16,
            marginBottom: 12,
            borderRadius: 12,
            background: "#1e293b",
            alignSelf: "flex-start",
          }}>
            <span>Thinking...</span>
          </div>
        )}
      </div>

      {/* Input area */}
      <div style={{ padding: 20, borderTop: "1px solid #1e293b" }}>
        <div style={{ display: "flex", gap: 12, maxWidth: "1200px", margin: "0 auto" }}>
          <input
            style={{ 
              flex: 1, 
              padding: 16, 
              borderRadius: 12, 
              border: "1px solid #1e293b",
              background: "#0f172a",
              color: "#e5e7eb",
              fontSize: "14px"
            }}
            placeholder="Ask me anything about learning..."
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && !loading && sendMessage()}
            disabled={loading}
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            style={{ 
              padding: "16px 32px", 
              borderRadius: 12, 
              background: loading || !input.trim() ? "#1e293b" : "#38bdf8", 
              color: loading || !input.trim() ? "#64748b" : "#000",
              fontWeight: "bold",
              border: "none",
              cursor: loading || !input.trim() ? "not-allowed" : "pointer",
              fontSize: "14px"
            }}
          >
            {loading ? "Sending..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}
// Updated Wed Jan 14 19:11:55 IST 2026
