![image](https://github.com/user-attachments/assets/6170ac45-1a29-4f1d-9dad-c34fa3816e54)

# Stateful Multi-Agent Systems in ADK

This project demonstrates how to build a **stateful multi-agent system** using ADK (Agent Development Kit), combining persistent state management with specialized agent delegation. The result is an intelligent agent ecosystem that remembers user information across interactions and leverages specialized domain expertise.

## What is a Stateful Multi-Agent System?

A **Stateful Multi-Agent System** combines two core patterns:

- **State Management:** Persisting information about users and conversations across interactions.
- **Multi-Agent Architecture:** Distributing tasks among specialized agents based on their expertise.

**Key Benefits:**

- Remembers user information and interaction history.
- Routes queries to the most appropriate specialized agent.
- Provides personalized responses based on past interactions.
- Maintains context across multiple agent delegates.

This example implements a customer service system for an online course platform, where specialized agents handle different aspects of customer support while sharing a common state.

## Project Structure

```
7-stateful-multi-agent/
│
├── customer_service_agent/         # Main agent package
│   ├── __init__.py                 # Required for ADK discovery
│   ├── agent.py                    # Root agent definition
│   └── sub_agents/                 # Specialized agents
│       ├── course_support_agent/   # Handles course content questions
│       ├── order_agent/            # Manages order history and refunds
│       ├── policy_agent/           # Answers policy questions
│       └── sales_agent/            # Handles course purchases
│
├── main.py                         # Application entry point with session setup
├── utils.py                        # Helper functions for state management
├── .env                            # Environment variables
└── README.md                       # This documentation
```


## Key Components

### 1. Session Management

The example uses `InMemorySessionService` to store session state:

```python
session_service = InMemorySessionService()

def initialize_state():
    """Initialize the session state with default values."""
    return {
        "user_name": "Brandon Hancock",
        "purchased_courses": [""],
        "interaction_history": [],
    }

# Create a new session with initial state
session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initialize_state(),
)
```


### 2. State Sharing Across Agents

All agents in the system can access the same session state, enabling:

- The root agent to track interaction history.
- The sales agent to update purchased courses.
- The course support agent to check if a user has purchased specific courses.
- All agents to personalize responses based on user information.


### 3. Multi-Agent Delegation

The customer service agent routes queries to specialized sub-agents:

```python
customer_service_agent = Agent(
    name="customer_service",
    model="gemini-2.0-flash",
    description="Customer service agent for AI Developer Accelerator community",
    instruction="""
    You are the primary customer service agent for the AI Developer Accelerator community.
    Your role is to help users with their questions and direct them to the appropriate specialized agent.
    # ... detailed instructions ...
    """,
    sub_agents=[policy_agent, sales_agent, course_support_agent, order_agent],
    tools=[get_current_time],
)
```


## How It Works

- **Initial Session Creation:**
A new session is created with user information and an empty interaction history. Session state is initialized with default values.
- **Conversation Tracking:**
Each user message is added to `interaction_history` in the session state. Agents can review past interactions to maintain context.
- **Query Routing:**
The root agent analyzes the user query and decides which specialist should handle it. Specialized agents receive the full state context when delegated to.
- **State Updates:**
When a user purchases a course, the sales agent updates `purchased_courses`. These updates are available to all agents for future interactions.
- **Personalized Responses:**
Agents tailor responses based on purchase history and previous interactions. Different paths are taken based on what the user has already purchased.


## Getting Started

### Setup

1. **Activate the virtual environment** from the root directory:
    - macOS/Linux:

```
source ../.venv/bin/activate
```

    - Windows CMD:

```
..\.venv\Scripts\activate.bat
```

    - Windows PowerShell:

```
..\.venv\Scripts\Activate.ps1
```

2. **Set your Google API key** in the `.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```


### Running the Example

To run the stateful multi-agent example:

```
python main.py
```

This will:

- Initialize a new session with default state.
- Start an interactive conversation with the customer service agent.
- Track all interactions in the session state.
- Allow specialized agents to handle specific queries.


## Example Conversation Flow

Try this conversation flow to test the system:

1. **General query:**
_"What courses do you offer?"_
(Root agent routes to sales agent)
2. **Purchase request:**
_"I want to buy the AI Marketing Platform course"_
(Sales agent processes the purchase and updates state)
3. **Course content inquiry:**
_"Can you tell me about the content in the AI Marketing Platform course?"_
(Root agent routes to course support agent, which now has access)
4. **Refund policy:**
_"What's your refund policy?"_
(Root agent routes to policy agent)

Notice how the system remembers your purchase across different specialized agents!

## Advanced Features

### 1. Interaction History Tracking

The system maintains a history of interactions to provide context:

```python
# Update interaction history with the user's query
add_user_query_to_history(
    session_service, APP_NAME, USER_ID, SESSION_ID, user_input
)
```


### 2. Dynamic Access Control

The system implements conditional access to certain agents. For example, the course support agent is only available for courses the user has purchased.

### 3. State-Based Personalization

All agents tailor responses based on session state:

- If the user hasn't purchased any courses yet, encourage them to explore the AI Marketing Platform.
- If the user has purchased courses, offer support for those specific courses.


## Production Considerations

For a production implementation, consider:

- **Persistent Storage:** Replace `InMemorySessionService` with `DatabaseSessionService` to persist state across application restarts.
- **User Authentication:** Implement proper user authentication to securely identify users.
- **Error Handling:** Add robust error handling for agent failures and state corruption.
- **Monitoring:** Implement logging and monitoring to track system performance.

```

