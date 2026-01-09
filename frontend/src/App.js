import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API = process.env.REACT_APP_API_URL || 'https://aclsa-api.onrender.com';

function App() {
  const [user, setUser] = useState(null);
  const [view, setView] = useState('chat');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let saved = localStorage.getItem('aclsa_user');
    if (!saved) {
      const userId = `user_${Date.now()}`;
      axios.post(`${API}/state/initialize?user_id=${userId}`).then(() => {
        const newUser = { id: userId, name: 'You' };
        localStorage.setItem('aclsa_user', JSON.stringify(newUser));
        setUser(newUser);
        setMessages([{
          role: 'assistant',
          content: 'Hi! I\'m your AI career strategist. I can help you with skills, career planning, and personalized recommendations. What would you like to explore?'
        }]);
      });
    } else {
      setUser(JSON.parse(saved));
      setMessages([{
        role: 'assistant',
        content: 'Welcome back! How can I help you today?'
      }]);
    }
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await axios.post(`${API}/ai/chat`, {
        message: input,
        user_id: user.id
      });
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: res.data.response,
        suggestions: res.data.suggestions
      }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'I apologize, I\'m having trouble connecting. Please try again.'
      }]);
    }
    
    setLoading(false);
  };

  const getDecision = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API}/ai/decision`, { user_id: user.id });
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `🎯 **AI Recommendation**: ${res.data.recommended_action}\n\n**Why?** ${res.data.reasoning}\n\n**Expected Impact**: ${res.data.expected_outcomes.impact_score * 100}% improvement potential`,
        confidence: res.data.confidence
      }]);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  if (!user) return <div style={{padding:'40px',textAlign:'center'}}>Loading...</div>;

  return (
    <div className="app">
      <div className="sidebar">
        <div className="logo">
          <span style={{fontSize:'32px'}}>🤖</span>
          <h2>ACLSA</h2>
        </div>
        <nav>
          <button className={view==='chat'?'active':''} onClick={()=>setView('chat')}>
            💬 Chat
          </button>
          <button onClick={getDecision}>
            🎯 Get AI Decision
          </button>
        </nav>
      </div>

      <div className="main">
        <div className="chat-container">
          <div className="messages">
            {messages.map((msg, i) => (
              <div key={i} className={`message ${msg.role}`}>
                <div className="avatar">
                  {msg.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="content">
                  <div className="text">{msg.content}</div>
                  {msg.suggestions && (
                    <div className="suggestions">
                      {msg.suggestions.map((s, j) => (
                        <button key={j} onClick={() => {setInput(s); sendMessage();}}>
                          {s}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="message assistant">
                <div className="avatar">🤖</div>
                <div className="content">
                  <div className="typing">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="input-area">
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyPress={e => e.key === 'Enter' && sendMessage()}
              placeholder="Ask me anything about your career..."
            />
            <button onClick={sendMessage} disabled={loading || !input.trim()}>
              ➤
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
