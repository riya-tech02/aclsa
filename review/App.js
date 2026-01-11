import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API = process.env.REACT_APP_API_URL || 'https://aclsa-api.onrender.com';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [view, setView] = useState('chat');
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (token) {
      loadUserData();
    }
  }, [token]);

  const loadUserData = async () => {
    try {
      const res = await axios.get(`${API}/dashboard/stats?token=${token}`);
      setUser(res.data);
    } catch (err) {
      localStorage.removeItem('token');
      setToken(null);
    }
  };

  if (!token) {
    return <AuthScreen onLogin={(t) => { setToken(t); localStorage.setItem('token', t); }} />;
  }

  return (
    <div className="app">
      <Sidebar view={view} setView={setView} onLogout={() => { localStorage.removeItem('token'); setToken(null); }} />
      <main className="main">
        {view === 'chat' && <ChatView token={token} />}
        {view === 'skills' && <SkillsView token={token} onUpdate={loadUserData} />}
        {view === 'dashboard' && <DashboardView token={token} user={user} />}
      </main>
    </div>
  );
}

function AuthScreen({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      if (isLogin) {
        const res = await axios.post(`${API}/auth/login`, { email, password });
        onLogin(res.data.token);
      } else {
        await axios.post(`${API}/auth/register`, { email, password, name });
        alert('Registration successful! Please login.');
        setIsLogin(true);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Authentication failed');
    }
  };

  return (
    <div className="auth-screen">
      <div className="auth-box">
        <h1>🤖 ACLSA</h1>
        <p>Your AI Career Strategist</p>
        
        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <input
              type="text"
              placeholder="Full Name"
              value={name}
              onChange={e => setName(e.target.value)}
              required
            />
          )}
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
          
          {error && <div className="error">{error}</div>}
          
          <button type="submit">{isLogin ? 'Login' : 'Sign Up'}</button>
        </form>
        
        <p className="toggle">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <span onClick={() => setIsLogin(!isLogin)}>
            {isLogin ? 'Sign Up' : 'Login'}
          </span>
        </p>
      </div>
    </div>
  );
}

function Sidebar({ view, setView, onLogout }) {
  return (
    <div className="sidebar">
      <div className="logo">
        <span>🤖</span>
        <h2>ACLSA</h2>
      </div>
      <nav>
        <button className={view==='dashboard'?'active':''} onClick={()=>setView('dashboard')}>
          📊 Dashboard
        </button>
        <button className={view==='skills'?'active':''} onClick={()=>setView('skills')}>
          📚 My Skills
        </button>
        <button className={view==='chat'?'active':''} onClick={()=>setView('chat')}>
          💬 AI Chat
        </button>
        <button onClick={onLogout} style={{marginTop:'auto',color:'#ef4444'}}>
          🚪 Logout
        </button>
      </nav>
    </div>
  );
}

function DashboardView({ token, user }) {
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    axios.post(`${API}/ai/analyze?token=${token}`).then(res => setAnalysis(res.data));
  }, []);

  if (!user) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{user.skills_count}</div>
          <div className="stat-label">Skills</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{user.total_practice_hours}</div>
          <div className="stat-label">Practice Hours</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{user.account_age_days}</div>
          <div className="stat-label">Days Active</div>
        </div>
      </div>

      {analysis && (
        <div className="analysis">
          <h2>AI Analysis</h2>
          <p><strong>Skill Level:</strong> {analysis.overview.skill_level}</p>
          <p><strong>Avg Proficiency:</strong> {analysis.overview.avg_proficiency}%</p>
          
          {analysis.strengths.length > 0 && (
            <div>
              <h3>💪 Strengths</h3>
              <ul>{analysis.strengths.map((s,i) => <li key={i}>{s}</li>)}</ul>
            </div>
          )}
          
          {analysis.recommendations.length > 0 && (
            <div>
              <h3>💡 Recommendations</h3>
              <ul>{analysis.recommendations.map((r,i) => <li key={i}>{r}</li>)}</ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function SkillsView({ token, onUpdate }) {
  const [skills, setSkills] = useState([]);
  const [showAdd, setShowAdd] = useState(false);
  const [newSkill, setNewSkill] = useState({ name: '', proficiency: 0.5, hours: 0 });

  useEffect(() => {
    loadSkills();
  }, []);

  const loadSkills = async () => {
    const res = await axios.get(`${API}/skills/list?token=${token}`);
    setSkills(res.data.skills);
  };

  const addSkill = async () => {
    await axios.post(`${API}/skills/add?token=${token}`, newSkill);
    setShowAdd(false);
    setNewSkill({ name: '', proficiency: 0.5, hours: 0 });
    loadSkills();
    onUpdate();
  };

  const deleteSkill = async (id) => {
    await axios.delete(`${API}/skills/${id}?token=${token}`);
    loadSkills();
    onUpdate();
  };

  return (
    <div className="skills-view">
      <div className="header">
        <h1>My Skills</h1>
        <button onClick={() => setShowAdd(true)} className="add-btn">+ Add Skill</button>
      </div>

      <div className="skills-grid">
        {skills.map(skill => (
          <div key={skill.id} className="skill-card">
            <h3>{skill.name}</h3>
            <div className="progress-bar">
              <div style={{width: `${skill.proficiency*100}%`}} />
            </div>
            <p>{(skill.proficiency*100).toFixed(0)}% • {skill.hours}h practiced</p>
            <button onClick={() => deleteSkill(skill.id)} className="delete-btn">Delete</button>
          </div>
        ))}
      </div>

      {showAdd && (
        <div className="modal" onClick={() => setShowAdd(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h2>Add New Skill</h2>
            <input
              type="text"
              placeholder="Skill name (e.g., Python, React)"
              value={newSkill.name}
              onChange={e => setNewSkill({...newSkill, name: e.target.value})}
            />
            <label>Proficiency: {(newSkill.proficiency*100).toFixed(0)}%</label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={newSkill.proficiency}
              onChange={e => setNewSkill({...newSkill, proficiency: parseFloat(e.target.value)})}
            />
            <input
              type="number"
              placeholder="Practice hours"
              value={newSkill.hours}
              onChange={e => setNewSkill({...newSkill, hours: parseInt(e.target.value)})}
            />
            <button onClick={addSkill}>Add Skill</button>
          </div>
        </div>
      )}
    </div>
  );
}

function ChatView({ token }) {
  const [messages, setMessages] = useState([{
    role: 'assistant',
    content: 'Hi! I analyze your actual skills and give personalized advice. Try asking: "What should I learn next?" or "Analyze my profile"'
  }]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!input.trim()) return;
    
    setMessages(prev => [...prev, { role: 'user', content: input }]);
    const msg = input;
    setInput('');
    setLoading(true);

    try {
      const res = await axios.post(`${API}/ai/chat?token=${token}`, { message: msg });
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: res.data.response,
        suggestions: res.data.suggestions
      }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error connecting to AI' }]);
    }
    
    setLoading(false);
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <div className="avatar">{msg.role === 'user' ? '👤' : '🤖'}</div>
            <div className="content">
              <div className="text">{msg.content}</div>
              {msg.suggestions && (
                <div className="suggestions">
                  {msg.suggestions.map((s, j) => (
                    <button key={j} onClick={() => {setInput(s); send();}}>{s}</button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && <div className="message assistant"><div className="avatar">🤖</div><div className="typing"><span/><span/><span/></div></div>}
      </div>

      <div className="input-area">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && send()}
          placeholder="Ask about your career, skills, or next steps..."
        />
        <button onClick={send} disabled={loading || !input.trim()}>➤</button>
      </div>
    </div>
  );
}

export default App;
