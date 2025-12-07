import json
from processpiper import ProcessMap, Pool, Lane, ActivityType, GatewayType, EventType

class ProcessMapper:
    def __init__(self):
        self.data = {
            "core": {}, "selection": {}, "scope": {}, 
            "layers": {}, "validation": {}, "steps": []
        }
        self.pm = None
        
    def ask_core_questions(self):
        """Six foundational questions from video."""
        questions = {
            "why": "Why do we perform this process (purpose/goal)?",
            "what": "What is the overall process name (e.g., 'HR Onboarding')?",
            "who": "Main roles involved (comma-separated)?",
            "when": "When does it trigger (e.g., 'New job req received')?",
            "how": "Main tools used (comma-separated)?",
            "where": "Where tracked (e.g., 'ClickUp, Google Sheets')?"
        }
        print("\n## 1. CORE QUESTIONS")
        for key, q in questions.items():
            self.data["core"][key] = input(f"{q}: ").strip()
    
    def ask_selection_questions(self):
        """Target high-impact areas."""
        print("\n## 2. PROCESS SELECTION")
        self.data["selection"] = {
            "pain": input("Biggest frustration/bottleneck: "),
            "impact": input("How it drives revenue/cost savings: "),
            "frequency": input("Frequency (daily/weekly/monthly): "),
            "errors": input("Current error rate/cycle time: ")
        }
    
    def collect_steps(self):
        """Interactive step collection with decisions."""
        print("\n## 3. SCOPE & STEPS (type 'done' to finish)")
        steps = []
        step_id = 1
        
        while True:
            print(f"\nStep {step_id}:")
            step = {
                "id": step_id,
                "name": input("Step name: "),
                "type": input("Type (task/decision/subprocess): ").lower(),
                "lane": input("Lane/role: "),
                "duration": input("Duration (minutes): "),
                "tool": input("Tool: ")
            }
            if step["name"].lower() == 'done': break
            steps.append(step)
            step_id += 1
            
        self.data["steps"] = steps
        
        # Connect steps
        print("\nConnections (e.g., '1->2,2->3|2->4' for decision):")
        self.data["connections"] = input().strip()
    
    def ask_layers(self):
        """Swimlanes and metrics."""
        print("\n## 4. LAYERS")
        self.data["layers"] = {
            "people": input("Swimlanes needed (y/n): "),
            "emotions": input("Emotion peaks (e.g., 'Scheduling frustration'): ")
        }
    
    def generate_map(self):
        """Create BPMN diagram from collected data."""
        process_name = self.data["core"]["what"]
        self.pm = ProcessMap(process_name)
        pool = Pool(process_name)
        
        # Create lanes from unique roles
        lanes = {}
        for step in self.data["steps"]:
            if step["lane"] not in lanes:
                lanes[step["lane"]] = Lane(step["lane"], pool=pool)
        
        # Add elements
        elements = {}
        for step in self.data["steps"]:
            lane = lanes[step["lane"]]
            if step["type"] == "task":
                el = lane.add_element(step["name"], ActivityType.TASK)
            elif step["type"] == "decision":
                el = lane.add_element(step["name"], GatewayType.EXCLUSIVE)
            else:  # subprocess
                el = lane.add_element(step["name"], ActivityType.TASK)
            elements[step["id"]] = el
        
        # Connect (simple linear for demo, extend for branches)
        prev = None
        for step_id in range(1, len(self.data["steps"])+1):
            if prev:
                prev.connect(elements[step_id])
            prev = elements[step_id]
        
        self.pm.set_footer(f"Automated from {self.data['core']['why'][:50]}...")
        self.pm.draw()
    
    def save_and_export(self):
        """Save data and export diagram."""
        filename = self.data["core"]["what"].lower().replace(" ", "_")
        
        # Save JSON
        with open(f"{filename}.json", "w") as f:
            json.dump(self.data, f, indent=2)
        
        # Export PNG/SVG
        self.pm.save(f"{filename}.png")
        print(f"\n✅ Saved: {filename}.json | {filename}.png")
        print("Use in ClickUp/SOPs or Blender for 3D explainer.")

# Run automation
mapper = ProcessMapper()
mapper.ask_core_questions()
mapper.ask_selection_questions()
mapper.collect_steps()
mapper.ask_layers()
mapper.generate_map()
mapper.save_and_export()