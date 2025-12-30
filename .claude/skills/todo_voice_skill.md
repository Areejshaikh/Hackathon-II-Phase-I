---
description: Enables voice command functionality for todo application using speech recognition.
responsibilities:
  - Capture and process voice input for task commands
  - Convert speech to structured task data
  - Support voice-based task CRUD operations
  - Provide voice feedback and confirmation
  - Handle multiple languages for speech recognition
rules:
  - Voice input requires confirmation before execution
  - Handle recognition errors gracefully
  - Support microphone permission and access
  - Fallback to text input when voice fails
scope:
  - Used by: todo-voice-agent
---

## User Input

```text
$ARGUMENTS
```

## Implementation Requirements

Implement a skill that enables voice command functionality for the todo application.

### Requirements

1. **Voice Input Capture**:
   - Activate microphone for voice input
   - Handle permission requests
   - Manage audio recording state
   - Support push-to-talk and continuous modes
   - Noise cancellation and filtering

2. **Speech Recognition**:
   - Convert audio to text
   - Support multiple languages (English, Urdu, etc.)
   - Confidence scoring for results
   - Handle ambiguous recognition
   - Custom vocabulary for task-related terms

3. **Command Parsing**:
   - Parse natural language commands
   - Extract task title, description, priority
   - Identify intended action (add, complete, delete)
   - Handle follow-up questions
   - Support phrases like "add task", "mark complete", etc.

4. **Voice Feedback**:
   - Text-to-speech confirmation
   - Read back task details for verification
   - Success/failure audio cues
   - Helpful prompts for re-speaking

5. **Task Voice Commands**:
   - "Add [task title]" - Create new task
   - "Complete [task title or ID]" - Mark task done
   - "Delete [task title or ID]" - Remove task
   - "List tasks" - Read out all tasks
   - "What's due today" - Read due tasks
   - "Remind me to [task]" - Add with reminder

6. **Error Handling**:
   - "I didn't understand" prompts
   - Timeout handling
   - Low confidence handling
   - Fallback to text input option
   - Cancel operation on "cancel" command

### Output

Return structured results with:
- Recognized text
- Parsed command and intent
- Extracted task data (if applicable)
- Confidence score
- Suggested action or clarification needed
