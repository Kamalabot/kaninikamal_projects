import json
from diagrams import Diagram, Cluster, Edge
from diagrams.generic.blank import Blank
from diagrams.generic.device import Mobile
from diagrams.generic.chart import FlowChart
from collections import defaultdict

class ProcessMapper:
    def __init__(self):
        self.data = {"core": {}, "selection": {}, "steps": []}
        
    def ask_core_questions(self):
        questions = {
            "what": "Process name (e.g., 'HR Onboarding')?",
            "why": "Purpose/goal?",
            "who": "Roles (comma-separated)?",
            "when": "Trigger event?",
            "how": "Tools used?",
            "where": "Tracking system?"
        }
        print("\n## CORE QUESTIONS")
        for key, q in questions.items():
            self.data["core"][key] = input(f"{q}: ").strip()
    
    def collect_steps(self):
        print("\n## STEPS (type 'done' to finish)")
        steps = []
        step_id = 1
        while True:
            print(f"\nStep {step_id}:")
            name = input("Name: ").strip()
            if name.lower() == 'done': break
            
            step = {
                "id": f"S{step_id}",
                "name": name,
                "type": input("Type (task/decision): ").lower(),
                "role": input("Role/Lane: ").strip()
            }
            steps.append(step)
            step_id += 1
        self.data["steps"] = steps
    
    def generate_diagram(self):
        """Generate PNG using diagrams library."""
        process_name = self.data["core"]["what"]
        filename = process_name.lower().replace(" ", "_")
        
        # Group by roles (clusters = swimlanes)
        roles = defaultdict(list)
        for step in self.data["steps"]:
            roles[step["role"]].append(step)
        
        with Diagram(process_name, show=False, filename=filename):
            # Start/End
            start = Blank("START")
            end = Blank("END")
            
            # Create clusters (swimlanes)
            clusters = {}
            prev_nodes = {}
            
            for role, steps in roles.items():
                with Cluster(role):
                    cluster_nodes = []
                    for step in steps:
                        if step["type"] == "decision":
                            node = FlowChart("diamond")
                            node.label = step["name"]
                        else:
                            node = FlowChart("box")
                            node.label = step["name"]
                        cluster_nodes.append(node)
                    
                    # Connect within cluster
                    for i in range(len(cluster_nodes)-1):
                        cluster_nodes[i] >> cluster_nodes[i+1]
                    
                    clusters[role] = cluster_nodes[0]
                    prev_nodes[role] = cluster_nodes[-1]
            
            # Linear flow through first step of each role (simplified)
            first_steps = [clusters[role] for role in roles]
            for i in range(len(first_steps)-1):
                first_steps[i] >> first_steps[i+1]
            
            start >> first_steps[0]
            first_steps[-1] >> end
        
        print(f"\n✅ Generated: {filename}.png")
        return filename
    
    def save_data(self, filename):
        with open(f"{filename}.json", "w") as f:
            json.dump(self.data, f, indent=2)
        print(f"✅ Saved: {filename}.json")

# RUN
if __name__ == "__main__":
    mapper = ProcessMapper()
    mapper.ask_core_questions()
    mapper.collect_steps()
    filename = mapper.generate_diagram()
    mapper.save_data(filename)
    print("\n🎬 Use PNG in docs/ClickUp. Blender: Parse JSON → 3D flowchart.")
