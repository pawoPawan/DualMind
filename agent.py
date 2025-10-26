"""
Google ADK Agent Implementation
Reference: https://google.github.io/adk-docs/
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ChatAgent:
    """ADK-based Chat Agent with session management"""
    
    def __init__(self):
        """Initialize the ADK agent"""
        # Initialize Gemini API
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        
        # Store chat sessions
        self.sessions = {}
        
        # Model configuration
        self.model_id = "gemini-2.0-flash-exp"
        self.model = genai.GenerativeModel(self.model_id)
        
        print(f"✓ ADK Agent initialized with model: {self.model_id}")
    
    def create_session(self, session_id: str):
        """Create a new chat session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "history": [],
                "chat": self.model.start_chat(history=[])
            }
            print(f"✓ Created new session: {session_id}")
        return session_id
    
    def chat(self, session_id: str, message: str) -> str:
        """Send a message and get response"""
        # Create session if it doesn't exist
        self.create_session(session_id)
        
        session = self.sessions[session_id]
        
        # Add user message to history
        session["history"].append({
            "role": "user",
            "content": message
        })
        
        try:
            # Use Gemini API to generate response
            response = session["chat"].send_message(message)
            
            # Extract response text
            response_text = response.text
            
            # Add assistant response to history
            session["history"].append({
                "role": "assistant",
                "content": response_text
            })
            
            return response_text
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"✗ {error_msg}")
            return error_msg
    
    def get_history(self, session_id: str):
        """Get conversation history for a session"""
        if session_id in self.sessions:
            return self.sessions[session_id]["history"]
        return []
    
    def clear_session(self, session_id: str):
        """Clear a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            print(f"✓ Cleared session: {session_id}")
    
    def list_sessions(self):
        """List all active sessions"""
        return list(self.sessions.keys())


# Create global agent instance
agent = ChatAgent()


if __name__ == "__main__":
    # Test the agent
    print("\n" + "="*60)
    print("Testing Google ADK Agent")
    print("="*60 + "\n")
    
    session_id = "test_session"
    
    # Test conversation
    print("User: Hello! My name is Alice.")
    response = agent.chat(session_id, "Hello! My name is Alice.")
    print(f"Agent: {response}\n")
    
    print("User: What's my name?")
    response = agent.chat(session_id, "What's my name?")
    print(f"Agent: {response}\n")
    
    # Show history
    print("Conversation History:")
    for msg in agent.get_history(session_id):
        print(f"  {msg['role']}: {msg['content'][:50]}...")

