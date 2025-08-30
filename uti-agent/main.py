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
        print("\n\nThank you for using the UTI Care Agent. Goodbye!")
        self.running = False
        sys.exit(0)
    
    def display_welcome(self):
        print("=" * 50)
        print("UTI Care Agent")
        print("=" * 50)
        print("I'm here to help assess your urinary symptoms and provide guidance.")
        print("Type 'quit' or 'exit' to end the session at any time.")
        print("Press Ctrl+C to exit gracefully.\n")
    
    def handle_user_input(self) -> str:
        try:
            return input("You: ").strip()
        except EOFError:
            return "quit"
    
    def display_response(self, response: str):
        print(f"\nAgent: {response}\n")
    
    def manage_conversation_flow(self):
        self.display_welcome()
        
        while self.running:
            user_input = self.handle_user_input()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Thank you for using the UTI Care Agent. Take care!")
                break
            
            if not user_input:
                continue
                
            response = self.conversation_manager.process_input(user_input)
            self.display_response(response)
            
            # Check if conversation is complete
            if self.conversation_manager.is_complete():
                print("Session complete. Thank you for using the UTI Care Agent!")
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