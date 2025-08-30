"""
Livewell UTI Agent - CLI Entry Point
"""
import sys
import signal
from core.conversation import ConversationManager
from utils.logger import EvaluationLogger


class PatientInterface:
    def __init__(self):
        self.conversation_manager = ConversationManager()
        self.logger = EvaluationLogger()
        self.running = True
        
        # Handle graceful exit
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        self.conversation_manager.display_goodbye()
        self.running = False
        sys.exit(0)
    
    def manage_conversation_flow(self):
        self.conversation_manager.display_welcome()
        
        while self.running:
            user_input = self.conversation_manager.get_user_input()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                self.conversation_manager.display_goodbye()
                break
            
            if not user_input:
                continue
                
            response = self.conversation_manager.process_input(user_input)
            self.conversation_manager.display_agent_response(response)
            
            # Check if conversation is complete
            if self.conversation_manager.is_complete():
                self.conversation_manager.display_goodbye()
                break


def main():
    try:
        interface = PatientInterface()
        interface.manage_conversation_flow()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()