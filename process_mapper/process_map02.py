import json
import graphviz
from collections import defaultdict

class ProcessMapper:
    def __init__(self):
        self.data = {
            "core": {}, "selection": {}, "scope": {}, 
            "layers": {}, "validation": {}, "steps": []
        }
        self.dot = None
        
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
        print("\n## 2. PROCESS SELECTION")
        self.data["selection"] = {
            "pain": input("Biggest frustration/bottleneck: "),
            "impact": input("How it drives revenue/cost savings: "),
            "frequency": input("Frequency (daily/weekly/monthly): "),
            "errors": input("Current error rate/cycle time: ")
        }
    
    def collect_steps(self):
        """Interactive step collection."""
        print("\n## 3. SCOPE & STEPS (type 'done' when finished)")
        steps = []
        step_id = 1
        
        while True:
            print(f"\nStep {step_id}:")
            name = input("Step name: ").strip()
            if name.lower() == 'done': break
                
            step = {
                "id": f"S{step_id}",
                "name": name,
                "type": input("Type (task/decision/subprocess): ").lower(),
                "lane": input("Lane/role (e.g., Client, Team): "),
                "duration": input("Duration (minutes, optional): "),
                "tool": input("Tool (optional): ")
            }
            steps.append(step)
            step_id += 1
        
        self.data["steps"] = steps
        
        # Connections
        print("\nConnections (e.g., 'S1->S2,S2->S3|S2->S4' for decision branch):")
        self.data["connections"] = input("Or press Enter for linear flow: ").strip()
    
    def ask_layers(self):
        print("\n## 4. LAYERS")
        self.data["layers"] = {
            "swimlanes": input("Show swimlanes (y/n): ").lower() == 'y',
            "emotions": input("Emotion notes (optional): ")
        }
    
    def generate_map(self):
        """Generate DOT flowchart."""
        process_name = self.data["core"]["what"]
        self.dot = graphviz.Digraph(process_name, format='png')
        self.dot.attr(rankdir='LR', size='12,8')  # Left-to-right flow
        
        # Video shapes: rectangle=task, diamond=decision
        shapes = {'task': 'box', 'decision': 'diamond', 'subprocess': 'folder'}
        
        # Group by lanes (subgraphs)
        lanes = defaultdict(list)
        for step in self.data["steps"]:
            lanes[step["lane"]].append(step)
        
        with self.dot.subgraph() as s:
            s.attr(rank='same')
            for lane_name, steps_in_lane in lanes.items():
                with s.subgraph(name=f'cluster_{lane_name.replace(" ", "_")}') as lane:
                    lane.attr(label=lane_name, style='filled', color='lightblue')
                    for step in steps_in_lane:
                        shape = shapes.get(step["type"], 'box')
                        label = f"{step['name']}\\n{step.get('duration', '')}min\\n{step.get('tool', '')}"
                        self.dot.node(step["id"], label, shape=shape)
        
        # Connections (linear if empty)
        if not self.data["connections"]:
            for i in range(len(self.data["steps"])-1):
                self.dot.edge(self.data["steps"][i]["id"], self.data["steps"][i+1]["id"])
        else:
            for conn in self.data["connections"].split(','):
                self.dot.edge(*conn.strip().split('->'))
        
        self.dot.node('start', 'START', shape='ellipse')
        self.dot.node('end', 'END', shape='ellipse')
        self.dot.edge('start', self.data["steps"][0]["id"])
        self.dot.edge(self.data["steps"][-1]["id"], 'end')
        
        self.dot.attr(label=f'{process_name}\\n{self.data["core"]["why"][:60]}...')
    
    def save_and_export(self):
        """Export diagram."""
        filename = self.data["core"]["what"].lower().replace(" ", "_")
        
        # Save JSON data
        with open(f"{filename}.json", "w") as f:
            json.dump(self.data, f, indent=2)
        
        # Export PNG + DOT source
        self.dot.render(f"{filename}", view=False, cleanup=True)
        print(f"\n✅ Generated: {filename}.png | {filename}.json | {filename}.dot")
        print("📱 Open PNG in browser/docs. Edit DOT for tweaks.")
        print("🎬 Blender: Import DOT→3D flowchart via Python extrusions.")

# Run
if __name__ == "__main__":
    mapper = ProcessMapper()
    mapper.ask_core_questions()
    mapper.ask_selection_questions()
    mapper.collect_steps()
    mapper.ask_layers()
    mapper.generate_map()
    mapper.save_and_export()
