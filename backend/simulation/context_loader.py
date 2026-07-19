from backend.ai_brain.context_builder import ContextBuilder

class ContextLoader:
    """Retrieves current StadiumState before simulation execution."""
    def __init__(self):
        self.builder = ContextBuilder()

    def load_context(self) -> dict:
        """Loads and structures the live operational snapshot."""
        return self.builder.build_context()

context_loader = ContextLoader()
