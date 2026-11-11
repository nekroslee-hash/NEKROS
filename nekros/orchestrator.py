class AIOrchestrator:
    """Provider-neutral routing layer; no paid service is called by default."""
    def __init__(self):
        self.providers = {}

    def register(self, provider):
        self.providers[provider.name] = provider

    async def respond(self, prompt: str):
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        if not self.providers:
            return "هسته NEKROS فعال است؛ هنوز مدل هوش مصنوعی متصل نشده است."
        provider = next(iter(self.providers.values()))
        return await provider.generate(prompt)

orchestrator = AIOrchestrator()
