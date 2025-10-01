# Frontend Conversation Persistence Integration Guide

## Overview
This document provides comprehensive guidance for implementing conversation persistence in the frontend application using the Azure Blob Storage-based conversation API that has been successfully implemented in the FastAPI backend.

## Backend Architecture Summary
The conversation system uses Azure Blob Storage for persistence with the following key features:
- **Storage**: Azure Blob Storage (consistent with existing file storage)
- **Security**: AES-256 encryption for all conversation data
- **Authentication**: User validation through existing UserSaltService
- **Structure**: Hierarchical blob organization by user/workspace/conversation

## API Endpoints Reference

### Base URL Structure
```
{API_BASE_URL}/api/v1/conversations
```

### 1. Create Conversation
**Endpoint:** `POST /api/v1/conversations/create`
**Purpose:** Create a new conversation with optional initial message

**Request Body:**
```json
{
  "user_id": "string",
  "workspace_id": "string", 
  "title": "string",
  "password": "string",
  "metadata": {},  // optional
  "initial_message": {  // optional
    "role": "user|assistant|system",
    "content": "string"
  }
}
```

**Response:**
```json
{
  "conversation_id": "conv_abc123...",
  "title": "Conversation Title",
  "workspace_id": "workspace_id",
  "created_at": "2025-09-19T21:18:25.670882Z",
  "initial_message_id": "msg_xyz789...",  // if initial_message provided
  "message": "Conversation created successfully"
}
```

### 2. List Conversations
**Endpoint:** `POST /api/v1/conversations/list`
**Purpose:** Get paginated list of conversations for a workspace

**Request Body:**
```json
{
  "user_id": "string",
  "password": "string",
  "workspace_id": "string",
  "limit": 10,      // optional, default 10
  "offset": 0       // optional, default 0
}
```

**Response:**
```json
{
  "conversations": [
    {
      "conversation_id": "conv_abc123...",
      "title": "Conversation Title",
      "message_count": 5,
      "last_message_at": "2025-09-19T21:20:15.123456Z",
      "created_at": "2025-09-19T21:18:25.670882Z",
      "updated_at": "2025-09-19T21:20:15.123456Z",
      "is_active": true,
      "metadata": {}
    }
  ],
  "total_count": 25,
  "offset": 0,
  "limit": 10,
  "has_more": true,
  "workspace_id": "workspace_id"
}
```

### 3. Get Conversation Details
**Endpoint:** `GET /api/v1/conversations/{conversation_id}`
**Purpose:** Get detailed conversation metadata

**Query Parameters:**
- `user_id`: string (required)
- `password`: string (required)

**Response:**
```json
{
  "conversation_id": "conv_abc123...",
  "title": "Conversation Title",
  "workspace_id": "workspace_id", 
  "created_at": "2025-09-19T21:18:25.670882Z",
  "updated_at": "2025-09-19T21:20:15.123456Z",
  "message_count": 5,
  "last_message_at": "2025-09-19T21:20:15.123456Z",
  "is_active": true,
  "metadata": {}
}
```

### 4. Add Message to Conversation
**Endpoint:** `POST /api/v1/conversations/{conversation_id}/messages`
**Purpose:** Add a new message to an existing conversation

**Request Body:**
```json
{
  "conversation_id": "conv_abc123...",
  "user_id": "string",
  "password": "string", 
  "workspace_id": "string",
  "role": "user|assistant|system",
  "content": "string",
  "metadata": {}  // optional
}
```

**Response:**
```json
{
  "message_id": "msg_xyz789...",
  "conversation_id": "conv_abc123...",
  "role": "user",
  "content": "Message content",
  "created_at": "2025-09-19T21:20:15.123456Z",
  "metadata": {},
  "message": "Message added successfully"
}
```

### 5. Get Conversation Messages
**Endpoint:** `POST /api/v1/conversations/{conversation_id}/messages/list`
**Purpose:** Get paginated messages for a conversation

**Request Body:**
```json
{
  "user_id": "string",
  "password": "string",
  "workspace_id": "string",
  "limit": 50,      // optional, default 50
  "offset": 0,      // optional, default 0
  "order": "asc"    // optional, "asc" or "desc", default "asc"
}
```

**Response:**
```json
{
  "messages": [
    {
      "message_id": "msg_xyz789...",
      "conversation_id": "conv_abc123...",
      "role": "user|assistant|system",
      "content": "Message content",
      "created_at": "2025-09-19T21:20:15.123456Z",
      "metadata": {}
    }
  ],
  "total_count": 5,
  "offset": 0,
  "limit": 50,
  "has_more": false,
  "conversation_id": "conv_abc123..."
}
```

### 6. Enhanced Chat with Conversation Persistence
**Endpoint:** `POST /api/v1/conversations/chat`
**Purpose:** Send message and get AI response with automatic conversation persistence

**Request Body:**
```json
{
  "user_id": "string",
  "password": "string",
  "workspace_id": "string", 
  "message": "User's message content",
  "conversation_id": "conv_abc123...",  // optional, creates new if not provided
  "conversation_title": "New Chat",     // used if creating new conversation
  "system_prompt": "Custom system prompt",  // optional
  "temperature": 0.7,                   // optional
  "max_tokens": 1000                    // optional
}
```

**Response:**
```json
{
  "conversation_id": "conv_abc123...",
  "user_message_id": "msg_user123...",
  "assistant_message_id": "msg_assistant456...",
  "assistant_response": "AI generated response",
  "conversation_title": "Conversation Title",
  "created_new_conversation": false,
  "message_count": 6,
  "timestamp": "2025-09-19T21:20:15.123456Z"
}
```

## Frontend Implementation Guide

### 1. Authentication Context
All conversation API calls require user authentication. Ensure you have:
```javascript
const userContext = {
  userId: "current_user_id",
  password: "user_password",  // Store securely
  workspaceId: "current_workspace_id"
};
```

### 2. Conversation State Management
Recommended state structure:
```javascript
const conversationState = {
  currentConversation: {
    id: null,
    title: "",
    messages: [],
    isLoading: false,
    lastUpdated: null
  },
  conversationList: {
    conversations: [],
    totalCount: 0,
    hasMore: false,
    isLoading: false
  }
};
```

### 3. Core API Service Functions

#### Create New Conversation
```javascript
async function createConversation(title, initialMessage = null) {
  const response = await fetch(`${API_BASE}/api/v1/conversations/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userContext.userId,
      password: userContext.password,
      workspace_id: userContext.workspaceId,
      title: title,
      initial_message: initialMessage
    })
  });
  
  if (!response.ok) throw new Error('Failed to create conversation');
  return await response.json();
}
```

#### Load Conversation List
```javascript
async function loadConversations(limit = 10, offset = 0) {
  const response = await fetch(`${API_BASE}/api/v1/conversations/list`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userContext.userId,
      password: userContext.password,
      workspace_id: userContext.workspaceId,
      limit: limit,
      offset: offset
    })
  });
  
  if (!response.ok) throw new Error('Failed to load conversations');
  return await response.json();
}
```

#### Send Message with Chat
```javascript
async function sendMessage(message, conversationId = null, conversationTitle = "New Chat") {
  const response = await fetch(`${API_BASE}/api/v1/conversations/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userContext.userId,
      password: userContext.password,
      workspace_id: userContext.workspaceId,
      message: message,
      conversation_id: conversationId,
      conversation_title: conversationTitle
    })
  });
  
  if (!response.ok) throw new Error('Failed to send message');
  return await response.json();
}
```

#### Load Conversation Messages
```javascript
async function loadMessages(conversationId, limit = 50, offset = 0) {
  const response = await fetch(`${API_BASE}/api/v1/conversations/${conversationId}/messages/list`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userContext.userId,
      password: userContext.password,
      workspace_id: userContext.workspaceId,
      limit: limit,
      offset: offset,
      order: "asc"
    })
  });
  
  if (!response.ok) throw new Error('Failed to load messages');
  return await response.json();
}
```

### 4. UI/UX Implementation Patterns

#### Conversation Sidebar
```javascript
// Display conversation list with infinite scroll
function ConversationSidebar() {
  const [conversations, setConversations] = useState([]);
  const [hasMore, setHasMore] = useState(false);
  
  const loadMore = async () => {
    const result = await loadConversations(10, conversations.length);
    setConversations(prev => [...prev, ...result.conversations]);
    setHasMore(result.has_more);
  };
  
  return (
    <div className="conversation-sidebar">
      {conversations.map(conv => (
        <ConversationItem 
          key={conv.conversation_id}
          conversation={conv}
          onClick={() => selectConversation(conv.conversation_id)}
        />
      ))}
      {hasMore && <button onClick={loadMore}>Load More</button>}
    </div>
  );
}
```

#### Chat Interface
```javascript
function ChatInterface() {
  const [currentConversation, setCurrentConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  
  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;
    
    // Add user message to UI immediately
    const userMessage = {
      role: "user",
      content: inputMessage,
      created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage("");
    
    try {
      // Send to API and get response
      const result = await sendMessage(
        inputMessage, 
        currentConversation?.id,
        currentConversation?.title || "New Chat"
      );
      
      // Add assistant response
      const assistantMessage = {
        role: "assistant", 
        content: result.assistant_response,
        created_at: result.timestamp
      };
      setMessages(prev => [...prev, assistantMessage]);
      
      // Update conversation context
      if (result.created_new_conversation) {
        setCurrentConversation({
          id: result.conversation_id,
          title: result.conversation_title
        });
      }
      
    } catch (error) {
      console.error("Failed to send message:", error);
      // Handle error state
    }
  };
  
  return (
    <div className="chat-interface">
      <MessageList messages={messages} />
      <MessageInput 
        value={inputMessage}
        onChange={setInputMessage}
        onSend={handleSendMessage}
      />
    </div>
  );
}
```

### 5. Error Handling
Common error scenarios and handling:

```javascript
function handleApiError(error, operation) {
  if (error.status === 401) {
    // Invalid credentials
    redirectToLogin();
  } else if (error.status === 404) {
    // Conversation not found
    showError("Conversation not found");
  } else if (error.status === 500) {
    // Server error
    showError(`${operation} failed. Please try again.`);
  } else {
    // Generic error
    showError("An unexpected error occurred");
  }
}
```

### 6. Performance Optimizations

#### Message Virtualization
For conversations with many messages, implement virtual scrolling:
```javascript
// Use libraries like react-window or react-virtualized
import { FixedSizeList as List } from 'react-window';

function VirtualizedMessageList({ messages }) {
  return (
    <List
      height={600}
      itemCount={messages.length}
      itemSize={80}
      itemData={messages}
    >
      {MessageItem}
    </List>
  );
}
```

#### Conversation Caching
```javascript
// Cache conversations in localStorage/sessionStorage
const conversationCache = {
  set(conversationId, data) {
    localStorage.setItem(`conv_${conversationId}`, JSON.stringify(data));
  },
  get(conversationId) {
    const data = localStorage.getItem(`conv_${conversationId}`);
    return data ? JSON.parse(data) : null;
  },
  clear(conversationId = null) {
    if (conversationId) {
      localStorage.removeItem(`conv_${conversationId}`);
    } else {
      // Clear all conversation cache
      Object.keys(localStorage)
        .filter(key => key.startsWith('conv_'))
        .forEach(key => localStorage.removeItem(key));
    }
  }
};
```

### 7. Security Considerations

- **Never log passwords** in frontend code
- **Validate user input** before sending to API
- **Handle authentication errors** gracefully
- **Clear sensitive data** on logout
- **Use HTTPS** for all API calls

### 8. Testing Strategy

#### Unit Tests
```javascript
// Test API service functions
describe('ConversationAPI', () => {
  test('creates conversation successfully', async () => {
    const result = await createConversation('Test Chat');
    expect(result.conversation_id).toMatch(/^conv_/);
    expect(result.title).toBe('Test Chat');
  });
  
  test('loads conversation list', async () => {
    const result = await loadConversations(5);
    expect(Array.isArray(result.conversations)).toBe(true);
    expect(result.limit).toBe(5);
  });
});
```

#### Integration Tests
```javascript
// Test full conversation flow
describe('Conversation Flow', () => {
  test('complete conversation lifecycle', async () => {
    // Create conversation
    const newConv = await createConversation('Integration Test');
    
    // Send message
    const chatResult = await sendMessage('Hello', newConv.conversation_id);
    expect(chatResult.assistant_response).toBeTruthy();
    
    // Load messages
    const messages = await loadMessages(newConv.conversation_id);
    expect(messages.messages.length).toBe(2); // user + assistant
  });
});
```

## Summary
This conversation persistence system provides:
- **Persistent Storage**: All conversations saved to Azure Blob Storage
- **Real-time Chat**: Immediate AI responses with conversation context
- **Scalable Architecture**: Handles multiple conversations per user/workspace
- **Secure Encryption**: All data encrypted with AES-256
- **Flexible API**: Supports various frontend frameworks and patterns

The backend is fully implemented and tested. Focus your frontend development on the API integration patterns outlined above for a robust conversation experience similar to ChatGPT or Claude interfaces.