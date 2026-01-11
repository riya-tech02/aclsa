from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import secrets
from typing import Dict, List
import random

app = FastAPI(title="ACLSA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
users_db = {}
sessions = {}
user_data = {}

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class SkillAdd(BaseModel):
    name: str
    proficiency: float
    hours: int = 0

@app.post("/auth/register")
def register(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    users_db[user.email] = {
        "email": user.email,
        "password": user.password,
        "name": user.name,
        "created_at": datetime.now().isoformat()
    }
    
    user_data[user.email] = {
        "skills": [],
        "projects": [],
        "goals": [],
        "chat_history": []
    }
    
    return {"message": "Registration successful", "email": user.email}

@app.post("/auth/login")
def login(user: UserLogin):
    if user.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if users_db[user.email]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = secrets.token_urlsafe(32)
    sessions[token] = {
        "email": user.email,
        "expires": (datetime.now() + timedelta(days=7)).isoformat()
    }
    
    return {
        "token": token,
        "user": {
            "email": user.email,
            "name": users_db[user.email]["name"]
        }
    }

@app.post("/skills/add")
def add_skill(skill: SkillAdd, token: str):
    if token not in sessions:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    email = sessions[token]["email"]
    
    skill_obj = {
        "id": len(user_data[email]["skills"]) + 1,
        "name": skill.name,
        "proficiency": skill.proficiency,
        "hours": skill.hours,
        "added_at": datetime.now().isoformat()
    }
    
    user_data[email]["skills"].append(skill_obj)
    
    return {"message": "Skill added", "skill": skill_obj}

@app.get("/skills/list")
def list_skills(token: str):
    if token not in sessions:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    email = sessions[token]["email"]
    return {"skills": user_data[email]["skills"]}

@app.delete("/skills/{skill_id}")
def delete_skill(skill_id: int, token: str):
    if token not in sessions:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    email = sessions[token]["email"]
    user_data[email]["skills"] = [s for s in user_data[email]["skills"] if s["id"] != skill_id]
    
    return {"message": "Skill deleted"}

def generate_real_advice(message: str, skills: list, user_name: str) -> str:
    """Generate context-aware, actionable advice like a real career coach"""
    msg_lower = message.lower()
    
    # Skill-specific advice
    skill_names = [s["name"] for s in skills] if skills else []
    avg_prof = sum(s["proficiency"] for s in skills) / len(skills) if skills else 0
    
    # Career planning questions
    if any(word in msg_lower for word in ["career", "job", "work", "salary", "interview"]):
        if "interview" in msg_lower:
            return f"""For interview preparation, here's a proven strategy:

**Technical Prep** (if applicable):
- Practice coding problems daily on LeetCode/HackerRank
- Review system design fundamentals
- Prepare 5-7 projects to discuss in detail

**Behavioral Prep**:
- Use STAR method (Situation, Task, Action, Result)
- Prepare stories for: leadership, conflict, failure, success
- Research the company thoroughly

**Day Before**:
- Review your resume deeply
- Prepare 3-5 thoughtful questions for interviewers
- Get good sleep!

**During Interview**:
- Think out loud during technical problems
- Ask clarifying questions
- Show enthusiasm for the role

Want specific help with any of these areas?"""
        
        elif "salary" in msg_lower or "negotiate" in msg_lower:
            return f"""Salary negotiation tips based on current market:

**Research Phase**:
- Check Glassdoor, Levels.fyi, Blind for market rates
- Consider: location, company size, your experience level
- Know your walk-away number

**Negotiation Strategy**:
1. Let them make the first offer
2. When asked about expectations, give a range (market rate + 10-20%)
3. Don't accept immediately - "I need to think about the complete package"
4. Negotiate benefits too: equity, PTO, signing bonus, remote work

**Scripts**:
- "Based on my research and experience, I was expecting something in the $X-Y range"
- "Is there flexibility on the base salary?"
- "Can we discuss the equity component?"

**Red Flags**:
- Companies that won't negotiate at all
- Lowball offers with vague "future potential"

What's your current situation? I can give more specific advice."""
        
        else:
            if skills:
                return f"""Based on your skills in {', '.join(skill_names[:3])}, here's my honest career advice:

**Immediate Actions** (This Week):
- Update your LinkedIn with specific projects and quantifiable achievements
- Start building in public - share your work on Twitter/GitHub
- Reach out to 5 people in your target roles for informational interviews

**Short-term** (1-3 Months):
- Build 2-3 portfolio projects that solve real problems
- Write technical blog posts explaining concepts you've learned
- Attend local meetups or online communities in your field

**Medium-term** (3-6 Months):
- Apply to companies where your skills match 70%+ of requirements (don't wait for 100%)
- Practice technical interviews weekly
- Build relationships with recruiters in your target companies

**Market Reality Check**:
- Entry-level: Focus on demonstrable skills over credentials
- Mid-level: Showcase impact and ownership
- Senior: Leadership and system design matter most

What's your current career stage? I can give more targeted advice."""
            else:
                return f"""Let's build your career roadmap, {user_name}. First, I need to understand your situation:

**Tell me about**:
1. What field/industry interests you? (software, data, design, etc.)
2. Current situation: student, career change, unemployed, looking to level up?
3. Timeline: when do you need results?

**Meanwhile, here's what works**:
- Pick ONE in-demand skill and go deep (not wide)
- Build real projects, not just tutorials
- Network relentlessly - 50%+ of jobs come from connections
- Document your learning journey publicly

Once you add your skills, I can give you a personalized 90-day action plan. What area are you interested in?"""
    
    # Learning questions
    elif any(word in msg_lower for word in ["learn", "study", "course", "tutorial"]):
        if not skills:
            return f"""Let me help you start learning effectively:

**Step 1: Choose Your Path** (Pick ONE):
- **Software Development**: High demand, good pay, remote-friendly
  → Start with: Python or JavaScript
- **Data Science**: Growing field, analytical
  → Start with: Python + SQL + Statistics
- **Web Development**: Fast entry, lots of jobs
  → Start with: HTML/CSS → JavaScript → React
- **Design**: Creative + technical
  → Start with: Figma + UI/UX fundamentals

**Step 2: Learning Strategy**:
❌ Don't: Watch 50 tutorials without building
✅ Do: Tutorial → Build project → Tutorial → Build project

**Free Resources**:
- freeCodeCamp (web dev)
- CS50 (computer science fundamentals)
- The Odin Project (full stack)
- fast.ai (machine learning)

**My Recommendation**: 
Pick Python if you want versatility. Learn for 2 hours daily for 90 days. Build one project every 2 weeks.

What interests you most? I'll create a specific roadmap."""
        
        else:
            next_skills = {
                "Python": ["Django/FastAPI", "Data structures & algorithms", "System design", "Docker/Kubernetes"],
                "JavaScript": ["React/Next.js", "Node.js/Express", "TypeScript", "Testing (Jest/Cypress)"],
                "React": ["Next.js", "TypeScript", "State management (Redux/Zustand)", "Testing"],
                "Machine Learning": ["MLOps", "Deep Learning", "Production ML", "Model deployment"],
                "SQL": ["Database design", "Query optimization", "PostgreSQL", "Data warehousing"]
            }
            
            suggestions = []
            for skill in skills[:2]:
                if skill["name"] in next_skills:
                    suggestions.extend(next_skills[skill["name"]][:2])
            
            return f"""Based on your current skills ({', '.join(skill_names)}), here's your learning roadmap:

**Next Skills to Learn**:
{chr(10).join(f"- **{s}**: Complements your existing knowledge" for s in suggestions[:3]) if suggestions else "- Advanced techniques in your current skills"}

**Learning Approach**:
1. **Theory** (20%): Understand concepts deeply
2. **Practice** (50%): Build real projects
3. **Teaching** (30%): Write blogs, help others

**Concrete Plan**:
Week 1-2: Tutorial + documentation reading
Week 3-4: Build a small project using the skill
Week 5-6: Refactor, add tests, deploy
Week 7-8: Write about what you learned

**Resources**:
- Documentation (always start here)
- YouTube for visual learning
- GitHub for code examples
- Twitter/Dev.to for current best practices

**Reality Check**:
- Proficiency takes 100-300 hours, not 10
- Build projects you'd actually use
- Code reviews speed up learning 10x

Want a specific tutorial recommendation for any of these?"""
    
    # Productivity/time management
    elif any(word in msg_lower for word in ["time", "productive", "focus", "distract", "motivation"]):
        return f"""Let me give you practical productivity advice that actually works:

**The Real Problem**:
It's not about time management - it's about energy and attention management.

**What Actually Works**:

**1. Deep Work Blocks** (Most Important)
- 90-minute focused sessions
- Phone in another room (seriously)
- One task only
- Do 2-3 blocks per day

**2. Energy Management**
- Peak hours (usually morning): hard tasks
- Afternoon slump: meetings, admin
- Evening: light learning, reading

**3. The 2-Minute Rule**
- If it takes <2 min, do it now
- Prevents task buildup

**4. Pomodoro (When Stuck)**
- 25 min work, 5 min break
- 4 cycles, then 15-30 min break

**What DOESN'T Work**:
❌ Working 12-hour days
❌ Multitasking
❌ Saying "I'll be more disciplined"
❌ Complex productivity systems

**Your Action Plan** (Start Today):
1. Block 2 hours tomorrow morning for your hardest task
2. Turn off ALL notifications during that time
3. Track your actual focused hours (probably 3-4 max)

**Mindset Shift**:
- Stop measuring time spent
- Start measuring: did I complete the important thing?

Having trouble with any specific aspect? I can drill deeper."""
    
    # Specific skill questions
    elif any(word in msg_lower for word in ["python", "javascript", "react", "sql", "programming", "code"]):
        return f"""Let me give you practical advice on leveling up technically:

**The Truth About Programming Skills**:
Reading code >>> Writing code for learning
Building projects >>> Tutorials
Struggling >>> Watching explanations

**Your Path Forward**:

**Phase 1: Fundamentals** (Can't skip this)
- Data structures: arrays, objects, maps
- Algorithms: sorting, searching, recursion
- Time/space complexity basics
- Practice on LeetCode Easy

**Phase 2: Build Real Things**
- Clone existing apps (Twitter, Airbnb, etc.)
- Build tools you'd actually use
- Deploy everything (Vercel, Heroku, Railway)
- Get users (even 10 is valuable feedback)

**Phase 3: Professional Skills**
- Version control (Git) - mandatory
- Testing - makes you stand out
- Code review - learn by reviewing others' code
- Documentation - shows seniority

**Common Mistakes**:
❌ Tutorial hell (watching 50 courses)
❌ Not deploying projects
❌ Ignoring fundamentals
❌ Learning 10 things at once

**What Hiring Managers Actually Want**:
1. Can you solve problems?
2. Can you work with others?
3. Do you write clean, maintainable code?
4. Can you learn quickly?

**Proof of Skills**:
- Live projects with users
- Clean GitHub with good READMEs
- Technical blog posts
- Contributions to open source

Where are you stuck? I can give specific guidance."""
    
    # General advice or casual questions
    else:
        if not skills:
            return f"""Hey {user_name}! I'm your AI career strategist, and I give real, actionable advice based on YOUR specific situation.

**I can help you with**:
- Career planning and job search strategy
- Learning roadmaps and skill development
- Interview preparation
- Salary negotiation
- Productivity and time management
- Technical skill development
- Portfolio and personal branding

**To give you the best advice, I need to know**:
1. Add your skills (use the "My Skills" tab)
2. Tell me what you're working toward

**Quick wins while you're here**:
- "How do I prepare for interviews?"
- "What should I learn next?"
- "How do I find a job?"
- "Help me be more productive"

What's on your mind? Be specific and I'll give you a detailed, actionable plan."""
        else:
            return f"""Got it! With your background in {', '.join(skill_names)}, here's what I think:

**Your Current Position**:
- Skill level: {"Beginner" if avg_prof < 0.5 else "Intermediate" if avg_prof < 0.75 else "Advanced"}
- Market readiness: {avg_prof * 100:.0f}%

**What This Means**:
{"You're building foundations - focus on depth, not breadth. Master these skills before adding new ones." if avg_prof < 0.5 else "You're ready to start applying these skills. Build projects and start interviewing." if avg_prof < 0.75 else "You're at an advanced level. Focus on teaching others, building products, or specializing further."}

**Next Steps**:
1. {"Practice fundamentals daily" if avg_prof < 0.5 else "Build 2-3 portfolio projects" if avg_prof < 0.75 else "Contribute to open source or start your own project"}
2. {"Watch tutorials and follow along" if avg_prof < 0.5 else "Apply for jobs (you're ready!)" if avg_prof < 0.75 else "Network with senior people in your field"}
3. {"Join beginner communities" if avg_prof < 0.5 else "Practice technical interviews" if avg_prof < 0.75 else "Consider mentoring others"}

**Ask me**:
- "Create a 90-day plan for me"
- "What projects should I build?"
- "How do I get my first job?"
- "What are my weak points?"

What specific help do you need?"""

    return "I'm here to help! Ask me about careers, learning, interviews, or productivity."

@app.post("/ai/chat")
def ai_chat(data: Dict, token: str):
    if token not in sessions:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    email = sessions[token]["email"]
    message = data.get("message", "")
    
    skills = user_data[email]["skills"]
    user_name = users_db[email]["name"]
    
    # Generate real, helpful response
    response = generate_real_advice(message, skills, user_name)
    
    # Save chat history
    user_data[email]["chat_history"].append({
        "user": message,
        "assistant": response,
        "timestamp": datetime.now().isoformat()
    })
    
    # Dynamic suggestions based on context
    suggestions = []
    if not skills:
        suggestions = ["What skills should I learn?", "How do I start?", "Create a roadmap for me"]
    else:
        suggestions = ["What should I learn next?", "How do I get a job?", "Interview tips", "90-day action plan"]
    
    return {
        "response": response,
        "suggestions": suggestions
    }

@app.post("/ai/analyze")
def analyze_profile(token: str):
    if token not in sessions:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    email = sessions[token]["email"]
    skills = user_data[email]["skills"]
    
    if not skills:
        return {"message": "Add skills first to get analysis"}
    
    total_hours = sum(s["hours"] for s in skills)
    avg_prof = sum(s["proficiency"] for s in skills) / len(skills)
    
    strengths = [s["name"] for s in skills if s["proficiency"] > 0.7]
    needs_work = [s["name"] for s in skills if s["proficiency"] < 0.5]
    
    analysis = {
        "overview": {
            "total_skills": len(skills),
            "practice_hours": total_hours,
            "avg_proficiency": round(avg_prof * 100, 1),
            "skill_level": "Beginner" if avg_prof < 0.5 else "Intermediate" if avg_prof < 0.75 else "Advanced"
        },
        "strengths": strengths,
        "areas_to_improve": needs_work,
        "recommendations": []
    }
    
    if total_hours < 1000:
        analysis["recommendations"].append("⏰ Aim for 10,000 hours for world-class expertise")
    
    if len(skills) < 3:
        analysis["recommendations"].append("🎯 Add complementary skills to become T-shaped")
    
    if avg_prof < 0.7:
        analysis["recommendations"].append("📈 Focus on mastering current skills before adding new ones")
    else:
        analysis["recommendations"].append("🚀 You're ready to apply - start building projects and interviewing!")
    
    return analysis

@app.get("/dashboard/stats")
def get_stats(token: str):
    if token not in sessions:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    email = sessions[token]["email"]
    data = user_data[email]
    
    return {
        "skills_count": len(data["skills"]),
        "total_practice_hours": sum(s["hours"] for s in data["skills"]),
        "projects_count": len(data["projects"]),
        "goals_count": len(data["goals"]),
        "account_age_days": (datetime.now() - datetime.fromisoformat(users_db[email]["created_at"])).days
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
