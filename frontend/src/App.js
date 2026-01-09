import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API = process.env.REACT_APP_API_URL || 'https://aclsa-api.onrender.com';

function App() {
  const [user, setUser] = useState(null);
  const [state, setState] = useState(null);
  const [view, setView] = useState('home');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const savedUser = localStorage.getItem('aclsa_user');
    if (savedUser) {
      const parsed = JSON.parse(savedUser);
      setUser(parsed);
      loadState(parsed.id);
    }
  }, []);

  const loadState = async (userId) => {
    try {
      const res = await axios.post(`${API}/state/query`, {
        user_id: userId
      });
      setState(res.data);
    } catch (err) {
      console.error('Load failed', err);
    }
  };

  const createUser = async () => {
    setLoading(true);
    const userId = `user_${Date.now()}`;
    try {
      await axios.post(`${API}/state/initialize?user_id=${userId}`);
      const newUser = { id: userId, name: 'Professional User' };
      localStorage.setItem('aclsa_user', JSON.stringify(newUser));
      setUser(newUser);
      await loadState(userId);
    } catch (err) {
      alert('Failed to create user: ' + err.message);
    }
    setLoading(false);
  };

  if (!user) {
    return (
      <div style={{minHeight:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:'linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%)'}}>
        <div style={{textAlign:'center',color:'white',maxWidth:'600px',padding:'40px'}}>
          <div style={{fontSize:'80px',marginBottom:'20px'}}>🤖</div>
          <h1 style={{fontSize:'48px',fontWeight:'800',marginBottom:'10px'}}>ACLSA</h1>
          <p style={{fontSize:'20px',opacity:0.9,marginBottom:'40px'}}>Autonomous Career & Life Strategy Agent</p>
          <button onClick={createUser} disabled={loading} style={{padding:'18px 48px',fontSize:'18px',fontWeight:'700',background:'white',color:'#1e3a8a',border:'none',borderRadius:'12px',cursor:loading?'not-allowed':'pointer'}}>
            {loading ? 'Creating...' : 'Get Started →'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{display:'flex',minHeight:'100vh',fontFamily:'system-ui'}}>
      <aside style={{width:'260px',background:'#0f172a',color:'white',display:'flex',flexDirection:'column'}}>
        <div style={{padding:'24px',borderBottom:'1px solid #1e293b'}}>
          <div style={{fontSize:'32px',marginBottom:'8px'}}>🤖</div>
          <h2 style={{fontSize:'20px',fontWeight:'800'}}>ACLSA</h2>
        </div>
        <nav style={{flex:1,padding:'16px 0'}}>
          {[
            {icon:'🏠',label:'Dashboard',id:'home'},
            {icon:'📚',label:'Skills',id:'skills'},
            {icon:'🧠',label:'AI Insights',id:'insights'}
          ].map(item => (
            <button key={item.id} onClick={() => setView(item.id)} style={{width:'100%',padding:'14px 24px',background:view===item.id?'#1e40af':'transparent',color:view===item.id?'white':'#94a3b8',border:'none',textAlign:'left',cursor:'pointer',display:'flex',alignItems:'center',gap:'12px',fontSize:'15px',fontWeight:'500',transition:'all 0.2s'}}>
              <span style={{fontSize:'20px'}}>{item.icon}</span>
              {item.label}
            </button>
          ))}
        </nav>
      </aside>

      <main style={{flex:1,display:'flex',flexDirection:'column',background:'#f8fafc'}}>
        <header style={{background:'white',padding:'24px 32px',borderBottom:'1px solid #e2e8f0'}}>
          <h1 style={{fontSize:'28px',fontWeight:'700',marginBottom:'4px'}}>{view==='home'?'Dashboard':view==='skills'?'Skills':'AI Insights'}</h1>
          <p style={{color:'#64748b',fontSize:'14px'}}>Welcome back, {user.name}</p>
        </header>

        <div style={{padding:'32px',flex:1}}>
          {view === 'home' && <Dashboard state={state} userId={user.id} onRefresh={() => loadState(user.id)} />}
          {view === 'skills' && <Skills state={state} userId={user.id} onRefresh={() => loadState(user.id)} />}
          {view === 'insights' && <Insights userId={user.id} />}
        </div>
      </main>
    </div>
  );
}

function Dashboard({ state, userId, onRefresh }) {
  const skills = state?.nodes?.filter(n => n.node_type === 'skill') || [];
  const projects = state?.nodes?.filter(n => n.node_type === 'project') || [];

  const addSkill = async () => {
    try {
      await axios.post(`${process.env.REACT_APP_API_URL || 'https://aclsa-api.onrender.com'}/state/node`, {
        user_id: userId,
        node_type: 'skill',
        attributes: { name: 'Python Programming', proficiency: 0.75, hours: 400 }
      });
      onRefresh();
    } catch (err) {
      alert('Failed: ' + err.message);
    }
  };

  if (!state) {
    return <div style={{textAlign:'center',padding:'60px',color:'#64748b'}}>Loading your data...</div>;
  }

  return (
    <div style={{display:'flex',flexDirection:'column',gap:'24px'}}>
      <div style={{display:'grid',gridTemplateColumns:'repeat(4, 1fr)',gap:'20px'}}>
        {[
          {title:'Skills',value:skills.length,icon:'📚',color:'#3b82f6'},
          {title:'Projects',value:projects.length,icon:'💼',color:'#10b981'},
          {title:'Total Nodes',value:state.metadata?.num_nodes || 0,icon:'🔵',color:'#8b5cf6'},
          {title:'Graph Edges',value:state.metadata?.num_edges || 0,icon:'🔗',color:'#f59e0b'}
        ].map((stat,i) => (
          <div key={i} style={{background:'white',padding:'24px',borderRadius:'12px',boxShadow:'0 1px 3px rgba(0,0,0,0.1)',borderLeft:`4px solid ${stat.color}`}}>
            <div style={{display:'flex',alignItems:'center',gap:'16px'}}>
              <div style={{fontSize:'32px'}}>{stat.icon}</div>
              <div>
                <div style={{fontSize:'32px',fontWeight:'800',lineHeight:'1'}}>{stat.value}</div>
                <div style={{color:'#64748b',fontSize:'13px',fontWeight:'500',marginTop:'4px'}}>{stat.title}</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <button onClick={addSkill} style={{alignSelf:'flex-start',padding:'12px 24px',background:'#667eea',color:'white',border:'none',borderRadius:'8px',fontWeight:'600',cursor:'pointer'}}>+ Add Sample Skill</button>

      {state.nodes && state.nodes.length > 0 ? (
        <div style={{background:'white',borderRadius:'12px',boxShadow:'0 1px 3px rgba(0,0,0,0.1)',padding:'24px'}}>
          <h3 style={{fontSize:'18px',fontWeight:'700',marginBottom:'20px'}}>📊 Recent Activity</h3>
          {state.nodes.slice(0,5).map((node,i) => (
            <div key={i} style={{display:'flex',alignItems:'center',gap:'12px',padding:'12px',borderBottom:i<4?'1px solid #f1f5f9':'none'}}>
              <span style={{fontSize:'20px'}}>•</span>
              <div>
                <p style={{fontWeight:'600',fontSize:'15px'}}>{node.node_id}</p>
                <p style={{fontSize:'13px',color:'#64748b'}}>{node.node_type}</p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div style={{background:'white',borderRadius:'12px',boxShadow:'0 1px 3px rgba(0,0,0,0.1)',padding:'60px',textAlign:'center'}}>
          <p style={{color:'#64748b',fontSize:'18px'}}>No nodes yet. Click "Add Sample Skill" to get started!</p>
        </div>
      )}
    </div>
  );
}

function Skills({ state, userId, onRefresh }) {
  const skills = state?.nodes?.filter(n => n.node_type === 'skill') || [];

  return (
    <div>
      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill, minmax(300px, 1fr))',gap:'20px'}}>
        {skills.length > 0 ? skills.map((skill,i) => (
          <div key={i} style={{background:'white',padding:'24px',borderRadius:'12px',boxShadow:'0 1px 3px rgba(0,0,0,0.1)'}}>
            <h4 style={{fontSize:'18px',marginBottom:'16px',fontWeight:'700'}}>{skill.attributes?.name || skill.node_id}</h4>
            <div style={{height:'8px',background:'#e2e8f0',borderRadius:'4px',overflow:'hidden',marginBottom:'12px'}}>
              <div style={{height:'100%',width:`${(skill.attributes?.proficiency || 0.5)*100}%`,background:'linear-gradient(90deg, #667eea 0%, #764ba2 100%)'}} />
            </div>
            <p style={{color:'#64748b',fontSize:'14px'}}>{((skill.attributes?.proficiency || 0.5)*100).toFixed(0)}% proficiency</p>
          </div>
        )) : (
          <div style={{gridColumn:'1/-1',textAlign:'center',padding:'60px',color:'#64748b'}}>
            <p>No skills added yet</p>
          </div>
        )}
      </div>
    </div>
  );
}

function Insights({ userId }) {
  return (
    <div style={{textAlign:'center',padding:'60px',color:'#64748b'}}>
      <h3 style={{fontSize:'24px',marginBottom:'16px'}}>🧠 AI Insights</h3>
      <p>Coming soon - AI-powered recommendations</p>
    </div>
  );
}

export default App;
