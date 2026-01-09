import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API = 'http://localhost:8000';

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
      const res = await axios.post('http://localhost:8001/state/query', {
        user_id: userId
      });
      setState(res.data);
    } catch (err) {
      console.error('Load failed');
    }
  };

  const createUser = async () => {
    setLoading(true);
    const userId = `user_${Date.now()}`;
    try {
      await axios.post(`http://localhost:8001/state/initialize?user_id=${userId}`);
      const newUser = { id: userId, name: 'Professional User' };
      localStorage.setItem('aclsa_user', JSON.stringify(newUser));
      setUser(newUser);
      await loadState(userId);
    } catch (err) {
      alert('Failed to create user');
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
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'20px',marginBottom:'40px'}}>
            <div style={{background:'rgba(255,255,255,0.1)',padding:'30px',borderRadius:'16px',backdropFilter:'blur(10px)'}}>
              <div style={{fontSize:'40px',marginBottom:'10px'}}>🧠</div>
              <h3 style={{fontSize:'18px',marginBottom:'8px'}}>AI Decisions</h3>
              <p style={{fontSize:'14px',opacity:0.8}}>Smart recommendations</p>
            </div>
            <div style={{background:'rgba(255,255,255,0.1)',padding:'30px',borderRadius:'16px',backdropFilter:'blur(10px)'}}>
              <div style={{fontSize:'40px',marginBottom:'10px'}}>📊</div>
              <h3 style={{fontSize:'18px',marginBottom:'8px'}}>Simulations</h3>
              <p style={{fontSize:'14px',opacity:0.8}}>Future predictions</p>
            </div>
          </div>
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
            {icon:'🧠',label:'AI Insights',id:'insights'},
            {icon:'🔮',label:'Simulations',id:'sims'}
          ].map(item => (
            <button key={item.id} onClick={() => setView(item.id)} style={{width:'100%',padding:'14px 24px',background:view===item.id?'#1e40af':'transparent',color:view===item.id?'white':'#94a3b8',border:'none',textAlign:'left',cursor:'pointer',display:'flex',alignItems:'center',gap:'12px',fontSize:'15px',fontWeight:'500',transition:'all 0.2s'}}>
              <span style={{fontSize:'20px'}}>{item.icon}</span>
              {item.label}
            </button>
          ))}
        </nav>
      </aside>

      <main style={{flex:1,display:'flex',flexDirection:'column',background:'#f8fafc'}}>
        <header style={{background:'white',padding:'24px 32px',borderBottom:'1px solid #e2e8f0',display:'flex',justifyContent:'space-between',alignItems:'center'}}>
          <div>
            <h1 style={{fontSize:'28px',fontWeight:'700',marginBottom:'4px'}}>{view==='home'?'Dashboard':view==='skills'?'Skills Management':view==='insights'?'AI Insights':'Simulations'}</h1>
            <p style={{color:'#64748b',fontSize:'14px'}}>Welcome back, {user.name}</p>
          </div>
          <button onClick={() => loadState(user.id)} style={{padding:'10px 20px',background:'#f1f5f9',border:'none',borderRadius:'8px',cursor:'pointer',fontWeight:'600'}}>🔄 Refresh</button>
        </header>

        <div style={{padding:'32px',flex:1}}>
          {view === 'home' && <Dashboard state={state} userId={user.id} onRefresh={() => loadState(user.id)} />}
          {view === 'skills' && <Skills state={state} userId={user.id} onRefresh={() => loadState(user.id)} />}
          {view === 'insights' && <Insights userId={user.id} />}
          {view === 'sims' && <Simulations userId={user.id} />}
        </div>
      </main>
    </div>
  );
}

function Dashboard({ state, userId, onRefresh }) {
  const skills = state?.nodes.filter(n => n.node_type === 'skill') || [];
  const projects = state?.nodes.filter(n => n.node_type === 'project') || [];

  const addSkill = async () => {
    try {
      await axios.post('http://localhost:8001/state/node', {
        user_id: userId,
        node_type: 'skill',
        attributes: { name: 'Python Programming', proficiency: 0.75, hours: 400 }
      });
      onRefresh();
    } catch (err) {
      alert('Failed');
    }
  };

  return (
    <div style={{display:'flex',flexDirection:'column',gap:'24px'}}>
      <div style={{display:'grid',gridTemplateColumns:'repeat(4, 1fr)',gap:'20px'}}>
        {[
          {title:'Skills',value:skills.length,icon:'📚',color:'#3b82f6'},
          {title:'Projects',value:projects.length,icon:'💼',color:'#10b981'},
          {title:'Total Nodes',value:state?.metadata.num_nodes || 0,icon:'🔵',color:'#8b5cf6'},
          {title:'Graph Edges',value:state?.metadata.num_edges || 0,icon:'🔗',color:'#f59e0b'}
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

      <div style={{background:'white',borderRadius:'12px',boxShadow:'0 1px 3px rgba(0,0,0,0.1)',overflow:'hidden'}}>
        <div style={{padding:'20px 24px',borderBottom:'1px solid #e2e8f0'}}>
          <h3 style={{fontSize:'18px',fontWeight:'700'}}>📊 Recent Activity</h3>
        </div>
        <div style={{padding:'24px'}}>
          {state?.nodes.slice(0,5).map((node,i) => (
            <div key={i} style={{display:'flex',alignItems:'center',gap:'12px',padding:'12px',borderBottom:i<4?'1px solid #f1f5f9':'none'}}>
              <span style={{fontSize:'20px'}}>•</span>
              <div style={{flex:1}}>
                <p style={{fontWeight:'600',fontSize:'15px'}}>{node.node_id}</p>
                <p style={{fontSize:'13px',color:'#64748b'}}>{node.node_type}</p>
              </div>
            </div>
          ))}
          {!state && <p style={{color:'#64748b'}}>No data yet</p>}
        </div>
      </div>
    </div>
  );
}

function Skills({ state, userId, onRefresh }) {
  const skills = state?.nodes.filter(n => n.node_type === 'skill') || [];
  const [showAdd, setShowAdd] = useState(false);
  const [newSkill, setNewSkill] = useState({ name: '', proficiency: 0.5 });

  const addSkill = async () => {
    try {
      await axios.post('http://localhost:8001/state/node', {
        user_id: userId,
        node_type: 'skill',
        attributes: newSkill
      });
      setShowAdd(false);
      setNewSkill({ name: '', proficiency: 0.5 });
      onRefresh();
    } catch (err) {
      alert('Failed');
    }
  };

  return (
    <div>
      <button onClick={() => setShowAdd(true)} style={{marginBottom:'24px',padding:'12px 24px',background:'#667eea',color:'white',border:'none',borderRadius:'8px',fontWeight:'600',cursor:'pointer'}}>+ Add Skill</button>
      
      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill, minmax(300px, 1fr))',gap:'20px'}}>
        {skills.map((skill,i) => (
          <div key={i} style={{background:'white',padding:'24px',borderRadius:'12px',boxShadow:'0 1px 3px rgba(0,0,0,0.1)'}}>
            <h4 style={{fontSize:'18px',marginBottom:'16px',fontWeight:'700'}}>{skill.attributes.name || skill.node_id}</h4>
            <div style={{height:'8px',background:'#e2e8f0',borderRadius:'4px',overflow:'hidden',marginBottom:'12px'}}>
              <div style={{height:'100%',width:`${(skill.attributes.proficiency || 0.5)*100}%`,background:'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',transition:'width 0.3s'}} />
            </div>
            <p style={{color:'#64748b',fontSize:'14px'}}>{((skill.attributes.proficiency || 0.5)*100).toFixed(0)}% proficiency</p>
          </div>
        ))}
      </div>

      {showAdd && (
        <div onClick={() => setShowAdd(false)} style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:'rgba(0,0,0,0.5)',display:'flex',alignItems:'center',justifyContent:'center',zIndex:1000}}>
          <div onClick={e => e.stopPropagation()} style={{background:'white',padding:'32px',borderRadius:'16px',maxWidth:'500px',width:'90%'}}>
            <h3 style={{fontSize:'24px',marginBottom:'24px'}}>Add New Skill</h3>
            <input type="text" placeholder="Skill name" value={newSkill.name} onChange={e => setNewSkill({...newSkill, name: e.target.value})} style={{width:'100%',padding:'12px',border:'1px solid #e2e8f0',borderRadius:'8px',fontSize:'16px',marginBottom:'16px'}} />
            <label style={{display:'block',marginBottom:'8px'}}>Proficiency: {(newSkill.proficiency*100).toFixed(0)}%</label>
            <input type="range" min="0" max="1" step="0.1" value={newSkill.proficiency} onChange={e => setNewSkill({...newSkill, proficiency: parseFloat(e.target.value)})} style={{width:'100%',marginBottom:'24px'}} />
            <button onClick={addSkill} style={{width:'100%',padding:'12px',background:'#667eea',color:'white',border:'none',borderRadius:'8px',fontWeight:'700',cursor:'pointer'}}>Add Skill</button>
          </div>
        </div>
      )}
    </div>
  );
}

function Insights({ userId }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetch = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API}/decision/recommend`, { user_id: userId, context: 'career' });
      setData(res.data);
    } catch (err) {
      alert('Failed');
    }
    setLoading(false);
  };

  useEffect(() => { fetch(); }, []);

  if (loading) return <p>Loading...</p>;
  if (!data) return <button onClick={fetch}>Get Insights</button>;

  return (
    <div style={{display:'flex',flexDirection:'column',gap:'20px'}}>
      <div style={{background:'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',padding:'40px',borderRadius:'16px',color:'white',boxShadow:'0 10px 40px rgba(102,126,234,0.3)'}}>
        <h3 style={{fontSize:'20px',marginBottom:'16px',opacity:0.9}}>🧠 Recommended Action</h3>
        <p style={{fontSize:'36px',fontWeight:'800',marginBottom:'16px',textTransform:'capitalize'}}>{data.recommendation.recommended_action.replace(/_/g, ' ')}</p>
        <p style={{fontSize:'18px',opacity:0.9}}>Confidence: {(data.recommendation.confidence*100).toFixed(0)}%</p>
      </div>

      <div style={{background:'white',padding:'32px',borderRadius:'12px',boxShadow:'0 1px 3px rgba(0,0,0,0.1)'}}>
        <h4 style={{fontSize:'20px',marginBottom:'16px',fontWeight:'700'}}>💡 Rationale</h4>
        <p style={{color:'#475569',lineHeight:'1.6'}}>{data.recommendation.rationale}</p>
      </div>

      <div style={{background:'white',padding:'32px',borderRadius:'12px',boxShadow:'0 1px 3px rgba(0,0,0,0.1)'}}>
        <h4 style={{fontSize:'20px',marginBottom:'16px',fontWeight:'700'}}>✅ Ethics Validation</h4>
        <p style={{marginBottom:'8px'}}>Status: <strong>{data.validation.approved ? '✅ Approved' : '❌ Rejected'}</strong></p>
        <p style={{marginBottom:'8px'}}>Safety Score: <strong>{(data.validation.safety_score*100).toFixed(0)}%</strong></p>
        <p style={{color:'#475569',lineHeight:'1.6'}}>{data.validation.explanation}</p>
      </div>
    </div>
  );
}

function Simulations({ userId }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API}/analytics/simulate`, { user_id: userId, horizon_days: 90, num_simulations: 50 });
      setData(res.data);
    } catch (err) {
      alert('Failed');
    }
    setLoading(false);
  };

  return (
    <div>
      <button onClick={run} disabled={loading} style={{marginBottom:'24px',padding:'16px 32px',background:'#667eea',color:'white',border:'none',borderRadius:'8px',fontSize:'16px',fontWeight:'700',cursor:loading?'not-allowed':'pointer'}}>
        {loading ? 'Running...' : '🔮 Run Simulation'}
      </button>

      {data && (
        <div style={{display:'flex',flexDirection:'column',gap:'20px'}}>
          <div style={{display:'grid',gridTemplateColumns:'repeat(3, 1fr)',gap:'20px'}}>
            {[
              {title:'Mean Outcome',value:`${(data.statistics.mean_outcome*100).toFixed(0)}%`,icon:'📊'},
              {title:'Best Case',value:`${(data.statistics.best_case*100).toFixed(0)}%`,icon:'🏆'},
              {title:'Worst Case',value:`${(data.statistics.worst_case*100).toFixed(0)}%`,icon:'⚠️'}
            ].map((s,i) => (
              <div key={i} style={{background:'white',padding:'32px',borderRadius:'12px',textAlign:'center',boxShadow:'0 1px 3px rgba(0,0,0,0.1)'}}>
                <div style={{fontSize:'40px',marginBottom:'12px'}}>{s.icon}</div>
                <div style={{fontSize:'36px',fontWeight:'800',marginBottom:'8px'}}>{s.value}</div>
                <div style={{color:'#64748b',fontSize:'14px'}}>{s.title}</div>
              </div>
            ))}
          </div>

          <div style={{background:'white',padding:'32px',borderRadius:'12px',boxShadow:'0 1px 3px rgba(0,0,0,0.1)'}}>
            <h4 style={{fontSize:'20px',marginBottom:'16px',fontWeight:'700'}}>💡 Recommendation</h4>
            <p style={{color:'#475569',fontSize:'16px',lineHeight:'1.6'}}>{data.recommendation}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
