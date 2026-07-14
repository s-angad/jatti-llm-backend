class ContextManager:
    def __init__(self):
        self.history = []
        
    def add_interaction(self, user_prompt: str, generated_code: str):
        self.history.append({"user": user_prompt, "assistant": generated_code})
        if len(self.history) > 3:
            self.history.pop(0) # keep last 3 interactions to save tokens
            
    def get_context_string(self) -> str:
        if not self.history:
            return ""
        context = "Previous conversation:\n"
        for interaction in self.history:
            context += f"User: {interaction['user']}\n"
            context += f"Jatti: {interaction['assistant']}\n"
        return context

context_manager = ContextManager()
