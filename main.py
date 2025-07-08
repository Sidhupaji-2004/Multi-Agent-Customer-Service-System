from customer_service_agent.agent import customer_service_agent 
from dotenv import load_dotenv 
from google.adk.runners import Runner 
from google.adk.sessions import InMemorySessionService 
import asyncio

load_dotenv() 

session_service = InMemorySessionService() 

initial_state = {
    "user_name": "Siddharth Sen", 
    "purchased_courses": [], 
    "interaction_history": []
}

async def main_async(): 
    APP_NAME = "Customer Support", 
    USERID = "aiwithsid" 
    
    new_session = session_service.create_session(
        app_name=APP_NAME, 
        user_id=USERID, 
        state=initial_state
    )
    
    SESSION_ID = new_session.id
    print(f"Created new session: {SESSION_ID}")
    
    
    runner = Runner(
        agent = customer_service_agent, 
        app_name = APP_NAME, 
        session_service = session_service
    )
    
    print("Welcome to customer service support")
    print("Type exit or quit to end the conversation.\n")
    
    while True: 
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit']: 
            print("Ending conversation: Goodbye")
            break
        
        # updation of interaction history with the user's query
        
    
    # ===== PART 6: State Examination =====
    # Show final session state
    final_session = session_service.get_session(
        app_name=APP_NAME, user_id=USERID, session_id=SESSION_ID
    )
    print("\nFinal Session State:")
    for key, value in final_session.state.items():
        print(f"{key}: {value}")
        
def main():
    """Entry point for the application."""
    asyncio.run(main_async())


if __name__ == "__main__": 
    main()