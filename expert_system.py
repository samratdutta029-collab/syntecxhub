class RuleBasedExpertSystem:
    def __init__(self):
        # A set to keep track of known facts/symptoms
        self.facts = set()
        # List of rules. Each rule is a dictionary containing:
        # 'if': list of conditions that must all be true
        # 'then': the conclusion that becomes a new fact if conditions are met
        self.rules = []

    def add_rule(self, conditions, conclusion):
        """Adds an if-then rule to the engine."""
        self.rules.append({
            'if': conditions,
            'then': conclusion
        })

    def add_facts(self, initial_facts):
        """Accepts initial user facts."""
        for fact in initial_facts:
            self.facts.add(fact.strip().lower())

    def forward_chaining(self):
        """
        Executes forward chaining inference.
        Loops through rules, infers new facts, and logs the reasoning path.
        """
        print("\n--- Starting Inference Engine (Forward Chaining) ---")
        print(f"Initial Facts Base: {list(self.facts)}")
        
        # Keep track of which rules have already been triggered to avoid infinite loops
        triggered_rules = []
        new_fact_inferred = True

        # Continue looping as long as we keep discovering new facts
        while new_fact_inferred:
            new_fact_inferred = False

            for index, rule in enumerate(self.rules):
                # Skip if this rule was already fired
                if index in triggered_rules:
                    continue

                # Check if ALL 'if' conditions of the rule are present in our facts base
                if all(condition in self.facts for condition in rule['if']):
                    conclusion = rule['then']
                    
                    # If the conclusion is not already a known fact, add it!
                    if conclusion not in self.facts:
                        self.facts.add(conclusion)
                        triggered_rules.append(index)
                        new_fact_inferred = True
                        
                        # LOG INFERENCE STEP (Reasoning Path)
                        print(f"[LOG] Rule Triggered: IF {rule['if']} -> THEN Inferred: '{conclusion.upper()}'")
                        print(f"Current Facts Base: {list(self.facts)}\n")
                        
                        # Break out of the rule loop to restart checking with the newly updated facts base
                        break 

        print("--- Inference Complete ---")
        print(f"Final Derived Facts Base: {list(self.facts)}\n")


# ==========================================
# TESTING THE SYSTEM (Multi-Step Inference)
# ==========================================
if __name__ == "__main__":
    # 1. Initialize the Expert System
    expert_system = RuleBasedExpertSystem()

    # 2. Define the Knowledge Base (Rules)
    # This demonstrates chaining: 
    # Fever + Cough -> Flu. Flu + Dehydration -> Severe Flu.
    expert_system.add_rule(['fever', 'cough'], 'flu')
    expert_system.add_rule(['flu', 'dehydration'], 'severe flu')
    expert_system.add_rule(['rash', 'fever'], 'measles')
    expert_system.add_rule(['severe flu', 'breathing difficulty'], 'hospitalization recommended')

    # 3. Accept User Symptoms (Initial Facts)
    print("Welcome to the AI Expert System Engine.")
    print("Enter symptoms separated by commas (e.g., fever, cough, dehydration, breathing difficulty):")
    
    # Static fallback if running headless, or active prompt:
    user_input = input("Enter symptoms: ")
    if not user_input.strip():
        # Default fallback test case to demonstrate full chaining
        user_input = "fever, cough, dehydration, breathing difficulty"
        print(f"Using default test symptoms: {user_input}")

    # Process and add user symptoms
    user_symptoms = user_input.split(",")
    expert_system.add_facts(user_symptoms)

    # 4. Run the engine to infer conclusions and view reasoning logs
    expert_system.forward_chaining()