from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import json
import re

app = FastAPI(title="ACLSA Agentic AI System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User conversations and learning progress
conversations = {}
user_profiles = {}
learning_plans = {}

class MessageRequest(BaseModel):
    user_id: str
    message: str
    context: Optional[str] = None

class MessageResponse(BaseModel):
    response: str
    timestamp: str
    user_id: str
    metadata: Optional[Dict] = None

# AGENTIC COMPONENTS

class Agent:
    """Main agentic AI that can plan, reason, and use tools"""
    
    def __init__(self):
        self.tools = {
            "create_study_plan": self.create_study_plan,
            "track_progress": self.track_progress,
            "recommend_resources": self.recommend_resources,
            "quiz_generator": self.generate_quiz,
            "code_explainer": self.explain_code,
            "career_advisor": self.career_advice
        }
    
    def analyze_intent(self, message: str) -> Dict:
        """Analyze user's intent and determine required actions"""
        message_lower = message.lower()
        
        intents = {
            "create_plan": any(w in message_lower for w in ['plan', 'roadmap', 'schedule', 'how to learn']),
            "progress_check": any(w in message_lower for w in ['progress', 'how am i doing', 'track']),
            "need_resources": any(w in message_lower for w in ['resource', 'book', 'course', 'tutorial', 'recommend']),
            "quiz_me": any(w in message_lower for w in ['quiz', 'test', 'practice', 'question']),
            "explain_code": any(w in message_lower for w in ['explain code', 'what does this do', 'how does']),
            "career_help": any(w in message_lower for w in ['career', 'job', 'interview', 'resume']),
            "general_question": True  # Default
        }
        
        # Extract topic
        topics = {
            "python": "python" in message_lower,
            "javascript": any(w in message_lower for w in ['javascript', 'js', 'react']),
            "web_dev": any(w in message_lower for w in ['web', 'html', 'css', 'frontend', 'backend']),
            "data_science": any(w in message_lower for w in ['data science', 'ml', 'machine learning', 'ai']),
            "general": True
        }
        
        active_topic = next((k for k, v in topics.items() if v), "general")
        active_intents = [k for k, v in intents.items() if v]
        
        return {
            "primary_intent": active_intents[0] if active_intents else "general_question",
            "all_intents": active_intents,
            "topic": active_topic,
            "message": message
        }
    
    def plan_response(self, intent_analysis: Dict, user_id: str) -> Dict:
        """Multi-step planning based on intent"""
        intent = intent_analysis["primary_intent"]
        topic = intent_analysis["topic"]
        
        plan = {
            "steps": [],
            "tools_needed": [],
            "context": {}
        }
        
        if intent == "create_plan":
            plan["steps"] = [
                "Assess current knowledge level",
                "Create personalized learning path",
                "Suggest resources and timeline",
                "Set milestones"
            ]
            plan["tools_needed"] = ["create_study_plan"]
            
        elif intent == "progress_check":
            plan["steps"] = ["Retrieve learning history", "Analyze progress", "Provide feedback"]
            plan["tools_needed"] = ["track_progress"]
            
        elif intent == "need_resources":
            plan["steps"] = ["Identify topic", "Curate resources", "Prioritize by level"]
            plan["tools_needed"] = ["recommend_resources"]
            
        elif intent == "quiz_me":
            plan["steps"] = ["Generate relevant questions", "Track answers", "Provide explanations"]
            plan["tools_needed"] = ["quiz_generator"]
            
        elif intent == "career_help":
            plan["steps"] = ["Assess skills", "Identify gaps", "Create action plan"]
            plan["tools_needed"] = ["career_advisor"]
        
        plan["context"] = {"topic": topic, "user_id": user_id}
        return plan
    
    def execute_plan(self, plan: Dict) -> str:
        """Execute the planned steps using available tools"""
        results = []
        
        for tool_name in plan["tools_needed"]:
            if tool_name in self.tools:
                result = self.tools[tool_name](plan["context"])
                results.append(result)
        
        # If no specific tools, provide intelligent response
        if not results:
            return self.general_response(plan["context"])
        
        return "\n\n".join(results)
    
    # TOOL IMPLEMENTATIONS
    
    def create_study_plan(self, context: Dict) -> str:
        topic = context.get("topic", "programming")
        
        plans = {
            "python": """📚 **Your Personalized Python Learning Plan**

**Phase 1: Foundations (Weeks 1-2)**
- ✓ Variables, data types, operators
- ✓ Control flow (if/else, loops)
- ✓ Functions and modules
- **Practice**: 30 min daily on HackerRank

**Phase 2: Data Structures (Weeks 3-4)**
- ✓ Lists, dictionaries, sets, tuples
- ✓ List comprehensions
- ✓ Working with files
- **Project**: Build a todo list CLI app

**Phase 3: OOP & Advanced (Weeks 5-6)**
- ✓ Classes and objects
- ✓ Inheritance, polymorphism
- ✓ Exception handling
- **Project**: Create a mini library management system

**Phase 4: Real-World Skills (Weeks 7-8)**
- ✓ Working with APIs
- ✓ Database basics (SQLite)
- ✓ Testing with pytest
- **Final Project**: Build a REST API

**Daily Commitment**: 1-2 hours
**Resources**: Python Crash Course, Real Python, Codecademy
**Check-ins**: Weekly progress reviews with me!

Ready to start? I'll track your progress!""",
            
            "web_dev": """🌐 **Web Development Mastery Plan**

**Month 1: Frontend Foundations**
- Week 1-2: HTML5 & CSS3 (Flexbox, Grid)
- Week 3-4: JavaScript ES6+ basics
- **Project**: Portfolio website

**Month 2: Interactive Web**
- Week 1-2: DOM manipulation, events
- Week 3-4: Fetch API, async/await
- **Project**: Weather dashboard app

**Month 3: Modern Framework**
- Week 1-4: React fundamentals
- **Project**: Todo app with React

**Month 4: Full Stack**
- Week 1-2: Node.js & Express
- Week 3-4: Database integration
- **Final Project**: Full-stack CRUD app

**Milestones**: Deploy 1 project monthly
**Resources**: MDN, FreeCodeCamp, Frontend Mentor""",
            
            "data_science": """📊 **Data Science Journey**

**Foundation (Month 1)**
- Python basics
- NumPy, Pandas
- Data visualization (Matplotlib, Seaborn)
- **Project**: Analyze a real dataset

**Statistics & ML (Month 2-3)**
- Statistical concepts
- Scikit-learn basics
- Linear regression, classification
- **Project**: Predictive model

**Advanced Topics (Month 4)**
- Neural networks intro
- Deep learning basics
- **Capstone**: End-to-end ML project

**Tools**: Jupyter, Kaggle
**Practice**: Daily Kaggle challenges""",
        }
        
        return plans.get(topic, self.general_learning_plan(topic))
    
    def track_progress(self, context: Dict) -> str:
        user_id = context["user_id"]
        
        # Simulate progress tracking
        return """📈 **Your Learning Progress**

**This Week:**
- ✅ Completed: 5 Python challenges
- ✅ Study time: 8.5 hours
- ✅ Projects: 1 in progress

**Overall Progress:**
- 🎯 Python Basics: 85% complete
- 🎯 Data Structures: 60% complete
- 🎯 OOP Concepts: 40% complete

**Strengths:** 
- Quick grasp of syntax
- Good problem-solving skills

**Areas to Improve:**
- Spend more time on OOP concepts
- Practice more complex algorithms

**Next Milestone:** Complete OOP module by Friday
**Recommendation:** Do 2 OOP practice problems today

Keep up the great work! 💪"""
    
    def recommend_resources(self, context: Dict) -> str:
        topic = context.get("topic", "general")
        
        resources = {
            "python": """📖 **Top Python Resources**

**📚 Books:**
- "Python Crash Course" by Eric Matthes (Beginner)
- "Fluent Python" by Luciano Ramalho (Advanced)
- "Automate the Boring Stuff" (Practical)

**💻 Online Platforms:**
- Real Python (realp

ython.com) - Excellent tutorials
- Python.org docs - Official reference
- Codecademy Python course - Interactive

**🎥 Video Courses:**
- "Complete Python Bootcamp" on Udemy
- Corey Schafer's YouTube channel
- freeCodeCamp Python course

**🏆 Practice:**
- LeetCode (Interview prep)
- HackerRank (Challenges)
- Project Euler (Math problems)

**🔧 Tools:**
- VS Code with Python extension
- PyCharm (IDE)
- Jupyter Notebooks

Start with "Python Crash Course" and practice on HackerRank daily!""",
            
            "javascript": """🚀 **JavaScript Learning Resources**

**Essential Reading:**
- "Eloquent JavaScript" (Free online)
- "You Don't Know JS" series
- MDN Web Docs

**Courses:**
- freeCodeCamp JavaScript
- JavaScript30 by Wes Bos
- The Odin Project

**Practice Platforms:**
- Codewars
- Exercism
- Frontend Mentor (Projects)

**Stay Updated:**
- JavaScript Weekly newsletter
- Dev.to JavaScript articles""",
        }
        
        return resources.get(topic, "I can recommend resources for any tech topic! Just specify what you're learning.")
    
    def generate_quiz(self, context: Dict) -> str:
        topic = context.get("topic", "python")
        
        return f"""🧠 **Quick {topic.title()} Quiz**

**Question 1:** What's the difference between a list and a tuple in Python?
a) Lists are mutable, tuples are immutable
b) Tuples are faster than lists
c) Lists use [], tuples use ()
d) All of the above

**Question 2:** What does this code output?
```python
x = [1, 2, 3]
y = x
y.append(4)
print(x)
```
a) [1, 2, 3]
b) [1, 2, 3, 4]
c) Error
d) None

**Question 3:** Which is the correct way to define a function?
a) function myFunc():
b) def myFunc():
c) func myFunc():
d) define myFunc():

Reply with your answers (e.g., "1a, 2b, 3b") and I'll check them!"""
    
    def explain_code(self, context: Dict) -> str:
        return """💡 **Code Explanation Assistant**

I can help explain code! Just paste the code and I'll break it down:

**I can explain:**
- What the code does
- How it works step-by-step
- Best practices and improvements
- Common pitfalls

**Example format:**
```
Explain this code:
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

Paste your code and I'll explain it clearly!"""
    
    def career_advice(self, context: Dict) -> str:
        return """💼 **Career Development Guidance**

**🎯 Career Path Planning:**
1. **Assess Your Skills**: What do you know well?
2. **Identify Gaps**: What does your target role require?
3. **Build Projects**: Create a portfolio
4. **Network**: LinkedIn, tech communities
5. **Apply Strategically**: Quality over quantity

**📝 Resume Tips:**
- Lead with impact (not just responsibilities)
- Quantify achievements
- Tailor to each job
- Keep it 1-2 pages

**🎤 Interview Prep:**
- Practice coding problems daily (LeetCode)
- Prepare STAR stories
- Research the company
- Ask thoughtful questions

**🚀 Quick Wins:**
- Build 2-3 portfolio projects
- Contribute to open source
- Write technical blog posts
- Get active on GitHub

**What's your target role?** I can create a specific action plan!"""
    
    def general_learning_plan(self, topic: str) -> str:
        return f"""📚 **Learning Plan for {topic.title()}**

**Phase 1: Foundation** (2-3 weeks)
- Understand core concepts
- Learn fundamental syntax/tools
- Small practice exercises

**Phase 2: Application** (3-4 weeks)
- Build small projects
- Apply concepts practically
- Debug and problem-solve

**Phase 3: Mastery** (4+ weeks)
- Complex projects
- Best practices
- Performance optimization

**Your next steps:**
1. Define specific learning goals
2. Allocate 1-2 hours daily
3. Build projects, not just tutorials
4. Join relevant communities

Tell me more about your goals and I'll create a detailed plan!"""
    
    def general_response(self, context: Dict) -> str:
        """Intelligent general responses"""
        message = context.get("message", "").lower()
        
        if any(w in message for w in ['hello', 'hi', 'hey']):
            return """👋 **Hello! I'm ACLSA - Your Agentic AI Learning Assistant**

I'm not just a chatbot - I'm your intelligent learning partner with:

✨ **Agentic Capabilities:**
- 🎯 Create personalized study plans
- 📊 Track your learning progress
- 🧠 Generate quizzes and practice problems
- 💡 Explain complex concepts
- 🚀 Provide career guidance
- 📚 Recommend curated resources

**I can help you:**
- Plan your learning journey
- Master programming languages
- Prepare for interviews
- Build real projects
- Advance your career

**Just tell me:** What would you like to learn or achieve today?"""
        
        return f"""I'm here to help you learn and grow! 

**I noticed you asked about:** "{context.get('message', '')}"

I can assist with:
- Creating custom learning plans
- Tracking your progress
- Recommending resources
- Generating practice quizzes
- Career guidance
- Code explanations

**How can I help you learn today?**"""

# Initialize agent
agent = Agent()

@app.get("/")
def root():
    return {
        "service": "ACLSA Agentic AI System",
        "version": "2.0",
        "capabilities": [
            "Multi-step planning",
            "Tool usage",
            "Progress tracking",
            "Personalized learning paths",
            "Career guidance"
        ]
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "agentic-ai"}

@app.post("/message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """Agentic AI endpoint with planning and tool use"""
    
    try:
        # Initialize user
        if request.user_id not in conversations:
            conversations[request.user_id] = []
            user_profiles[request.user_id] = {"topics": [], "level": "beginner"}
        
        # Add to conversation history
        conversations[request.user_id].append({
            "role": "user",
            "content": request.message,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # AGENTIC WORKFLOW
        # Step 1: Analyze intent
        intent_analysis = agent.analyze_intent(request.message)
        
        # Step 2: Create plan
        plan = agent.plan_response(intent_analysis, request.user_id)
        
        # Step 3: Execute plan
        response = agent.execute_plan(plan)
        
        # Add to conversation
        conversations[request.user_id].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {
                "intent": intent_analysis["primary_intent"],
                "tools_used": plan["tools_needed"]
            }
        })
        
        # Keep only last 20 messages
        if len(conversations[request.user_id]) > 20:
            conversations[request.user_id] = conversations[request.user_id][-20:]
        
        return MessageResponse(
            response=response,
            timestamp=datetime.utcnow().isoformat(),
            user_id=request.user_id,
            metadata={
                "intent": intent_analysis["primary_intent"],
                "topic": intent_analysis["topic"],
                "tools_used": plan["tools_needed"]
            }
        )
        
    except Exception as e:
        return MessageResponse(
            response=f"I encountered an error, but I'm still here to help! Could you rephrase your question?",
            timestamp=datetime.utcnow().isoformat(),
            user_id=request.user_id
        )

@app.get("/user/{user_id}/profile")
def get_user_profile(user_id: str):
    """Get user learning profile"""
    return user_profiles.get(user_id, {"message": "No profile found"})

@app.get("/user/{user_id}/history")
def get_conversation_history(user_id: str):
    """Get conversation history"""
    return {
        "user_id": user_id,
        "conversations": conversations.get(user_id, []),
        "total_messages": len(conversations.get(user_id, []))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
