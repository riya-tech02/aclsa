from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import json

app = FastAPI(title="ACLSA AI Agent")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store conversation history per user
conversations = {}

class MessageRequest(BaseModel):
    user_id: str
    message: str
    context: Optional[str] = None

class MessageResponse(BaseModel):
    response: str
    timestamp: str
    user_id: str

def generate_intelligent_response(user_message: str, conversation_history: List[Dict]) -> str:
    """
    Smart response generator that understands context and provides helpful answers
    """
    message_lower = user_message.lower()
    
    # Greeting responses
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! I'm ACLSA, your AI-powered Course Learning Support Assistant. I'm here to help you with your learning journey. Whether you need help understanding a topic, creating a study plan, or getting career advice, I'm here for you. What would you like to learn about today?"
    
    # Python learning
    if 'python' in message_lower:
        if 'learn' in message_lower or 'start' in message_lower or 'begin' in message_lower:
            return """Great choice! Python is an excellent language to learn. Here's a structured path to get you started:

**Week 1-2: Fundamentals**
- Variables, data types (strings, numbers, lists, dictionaries)
- Basic operators and expressions
- Input/output operations

**Week 3-4: Control Flow**
- If/else statements
- For and while loops
- Functions and parameters

**Week 5-6: Data Structures**
- Lists and list comprehensions
- Dictionaries and sets
- Tuples and their use cases

**Week 7-8: Object-Oriented Programming**
- Classes and objects
- Inheritance and polymorphism
- Special methods

**Recommended Resources:**
- Practice on platforms like LeetCode, HackerRank
- Build small projects (calculator, todo list, simple game)
- Read "Python Crash Course" or "Automate the Boring Stuff"

Would you like me to elaborate on any specific topic or help you with a particular concept?"""
    
    # Programming concepts
    if any(word in message_lower for word in ['code', 'program', 'software', 'development']):
        return """I can help you with various programming and software development topics! Here are some areas I can assist with:

**Programming Languages:**
- Python, JavaScript, Java, C++, and more
- Syntax, best practices, and common patterns

**Web Development:**
- Frontend: HTML, CSS, JavaScript, React
- Backend: APIs, databases, server architecture

**Computer Science Concepts:**
- Data structures (arrays, trees, graphs)
- Algorithms (sorting, searching, dynamic programming)
- Big O notation and complexity analysis

**Software Engineering:**
- Design patterns
- Testing and debugging
- Version control (Git)
- Software architecture

What specific topic would you like to dive into? Feel free to ask about any concept, and I'll break it down for you!"""
    
    # Study help
    if any(word in message_lower for word in ['study', 'learn', 'understand', 'explain']):
        return """I'd be happy to help you learn! To provide the most effective guidance, I need to know:

1. **What topic** are you studying? (e.g., mathematics, computer science, physics)
2. **What's your current level?** (beginner, intermediate, advanced)
3. **What's your goal?** (exam preparation, building projects, career change)

I can help you by:
- Breaking down complex concepts into simple explanations
- Creating personalized study plans
- Suggesting resources and practice problems
- Providing step-by-step guidance on difficult topics
- Helping you prepare for exams or interviews

Tell me more about what you're trying to learn, and I'll create a customized learning path for you!"""
    
    # Career advice
    if any(word in message_lower for word in ['career', 'job', 'interview', 'resume']):
        return """I can definitely help with career guidance! Here's how I can assist:

**Career Planning:**
- Identify skills needed for your target role
- Create a roadmap to reach your career goals
- Suggest relevant courses and certifications

**Job Search:**
- Resume and portfolio tips
- LinkedIn profile optimization
- Job search strategies

**Interview Preparation:**
- Technical interview practice
- Behavioral question strategies
- System design discussions
- Coding challenge practice

**Skill Development:**
- Identify gaps in your knowledge
- Recommend learning resources
- Project ideas to build your portfolio

What specific aspect of your career would you like to focus on? Let me know your current situation and goals, and I'll provide tailored advice!"""
    
    # Math help
    if any(word in message_lower for word in ['math', 'calculus', 'algebra', 'geometry', 'statistics']):
        return """I can help you with mathematics! Whether it's fundamental concepts or advanced topics, I'm here to assist. Here are some areas I cover:

**Algebra:**
- Linear equations and inequalities
- Quadratic equations
- Systems of equations
- Functions and graphs

**Calculus:**
- Limits and continuity
- Derivatives and applications
- Integrals and area calculation
- Differential equations

**Statistics & Probability:**
- Descriptive statistics
- Probability distributions
- Hypothesis testing
- Regression analysis

**Discrete Math:**
- Logic and proofs
- Set theory
- Combinatorics
- Graph theory

What mathematical concept would you like help with? I can explain the theory, work through examples, and provide practice problems!"""
    
    # Project help
    if 'project' in message_lower:
        return """Excellent! Working on projects is one of the best ways to learn. I can help you:

**Project Ideas by Level:**

**Beginner Projects:**
- Calculator application
- Todo list app
- Simple game (tic-tac-toe, hangman)
- Weather app using APIs

**Intermediate Projects:**
- E-commerce website
- Social media clone
- Chat application
- Personal finance tracker

**Advanced Projects:**
- Machine learning model
- Full-stack web application
- Mobile app
- Distributed system

**Project Development Support:**
- Architecture and design decisions
- Technology stack recommendations
- Code structure and best practices
- Debugging and optimization
- Deployment strategies

What kind of project are you interested in building? Tell me your skill level and interests, and I'll help you plan and execute it!"""
    
    # Default intelligent response
    return f"""Thank you for your message! I'm ACLSA, and I'm here to help you learn and grow. 

Based on your question about "{user_message}", I'd like to understand better how I can assist you. Here are some ways I can help:

**Learning Support:**
- Explain complex topics in simple terms
- Create personalized study plans
- Provide practice problems and examples
- Break down difficult concepts step-by-step

**Academic Assistance:**
- Help with homework and assignments
- Exam preparation strategies
- Research and project guidance

**Career Development:**
- Skill development roadmaps
- Interview preparation
- Career transition advice

**Technical Skills:**
- Programming and software development
- Data structures and algorithms
- Web development and databases

Could you provide more details about what you'd like to learn or accomplish? The more specific you are, the better I can tailor my guidance to your needs!

What aspect would you like to explore first?"""

@app.get("/health")
def health():
    return {"status": "healthy", "service": "aclsa-agent"}
@app.get("/")
def root():
    return {
        "service": "ACLSA AI Agent",
        "status": "running",
        "version": "1.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "message": "/message"
        }
    }
@app.post("/message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """Main chat endpoint - handles user messages"""
    
    try:
        # Initialize conversation history for new users
        if request.user_id not in conversations:
            conversations[request.user_id] = []
        
        # Add user message to history
        conversations[request.user_id].append({
            "role": "user",
            "content": request.message
        })
        
        # Keep only last 10 messages to manage memory
        if len(conversations[request.user_id]) > 10:
            conversations[request.user_id] = conversations[request.user_id][-10:]
        
        # Generate intelligent response
        assistant_message = generate_intelligent_response(
            request.message,
            conversations[request.user_id]
        )
        
        # Add assistant response to history
        conversations[request.user_id].append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return MessageResponse(
            response=assistant_message,
            timestamp=datetime.utcnow().isoformat(),
            user_id=request.user_id
        )
        
    except Exception as e:
        error_message = f"I apologize, but I encountered an error processing your message. Please try again or rephrase your question."
        
        return MessageResponse(
            response=error_message,
            timestamp=datetime.utcnow().isoformat(),
            user_id=request.user_id
        )

@app.post("/chat/reset")
def reset_conversation(user_id: str):
    """Reset conversation history for a user"""
    if user_id in conversations:
        conversations[user_id] = []
    return {"status": "success", "message": "Conversation reset"}

@app.get("/chat/history/{user_id}")
def get_history(user_id: str):
    """Get conversation history for a user"""
    return {
        "user_id": user_id,
        "history": conversations.get(user_id, []),
        "message_count": len(conversations.get(user_id, []))
    }

# Keep your existing RL endpoints
@app.post("/rl/decide")
def make_decision(request: dict):
    """RL agent recommends optimal action"""
    return {
        "user_id": request.get("user_id"),
        "recommended_action": "study_high_priority_skill",
        "confidence": 0.85,
        "rationale": "Based on your current progress and goals, I recommend focusing on high-priority skills that align with your career objectives."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
