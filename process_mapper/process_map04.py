import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
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
                "type": input("Type (task/decision/subprocess): ").lower(),
                "role": input("Role/Lane: ").strip(),
                "duration": input("Duration (optional): ").strip()
            }
            steps.append(step)
            step_id += 1
        self.data["steps"] = steps
    
    def generate_flowchart(self):
        """Pure matplotlib flowchart matching video shapes."""
        process_name = self.data["core"]["what"]
        filename = process_name.lower().replace(" ", "_")
        
        # Group by roles for swimlanes
        roles = defaultdict(list)
        for step in self.data["steps"]:
            roles[step["role"]].append(step)
        
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 12)
        ax.axis('off')
        
        # Swimlane backgrounds
        y_base = 10
        lane_height = 1.5
        role_y_positions = {}
        
        for i, (role, steps_in_role) in enumerate(roles.items()):
            y_start = y_base - (i * lane_height * 1.2)
            role_y_positions[role] = y_start + 0.2
            
            # Lane background
            lane_rect = patches.Rectangle((0.5, y_start), 11, lane_height, 
                                        facecolor='lightblue', alpha=0.3, 
                                        edgecolor='gray', linewidth=2)
            ax.add_patch(lane_rect)
            
            # Role label
            ax.text(0.3, y_start + lane_height/2, role, fontsize=12, 
                   fontweight='bold', va='center')
        
        # Draw steps (video shapes: rect=task, diamond=decision)
        step_positions = {}
        y_pos = 11
        
        for step in self.data["steps"]:
            role_y = role_y_positions[step["role"]]
            x_pos = 2 + (self.data["steps"].index(step) * 1.5) % 8
            
            label = f"{step['name']}\n{step.get('duration', '')}"
            
            if step["type"] == "decision":
                # Diamond (video style)
                diamond = FancyBboxPatch((x_pos-0.6, role_y-0.6), 1.2, 1.2,
                                       boxstyle="rounddiamond,pad=0.1",
                                       facecolor="yellow", edgecolor="black")
                ax.add_patch(diamond)
                ax.text(x_pos, role_y, label, ha='center', va='center', 
                       fontsize=9, wrap=True)
            else:
                # Rectangle (task)
                rect = patches.FancyBboxPatch((x_pos-0.8, role_y-0.6), 1.6, 1.2,
                                            boxstyle="round,pad=0.1",
                                            facecolor="white", edgecolor="black")
                ax.add_patch(rect)
                ax.text(x_pos, role_y, label, ha='center', va='center', 
                       fontsize=9, wrap=True)
            
            step_positions[step["id"]] = (x_pos, role_y)
        
        # Arrows (flow)
        for i in range(len(self.data["steps"])-1):
            x1, y1 = step_positions[self.data["steps"][i]["id"]]
            x2, y2 = step_positions[self.data["steps"][i+1]["id"]]
            ax.annotate('', xy=(x2-0.8, y2), xytext=(x1+0.8, y1),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        # Start/End
        ax.add_patch(patches.Circle((1, 10.5), 0.4, facecolor='green'))
        ax.text(1, 10.5, "START", ha='center', va='center', fontweight='bold')
        
        ax.add_patch(patches.Circle((10, 1), 0.4, facecolor='red'))
        ax.text(10, 1, "END", ha='center', va='center', fontweight='bold')
        
        # Title
        fig.suptitle(f'{process_name}\n{self.data["core"]["why"][:80]}...', 
                    fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f"{filename}.png", dpi=300, bbox_inches='tight')
        plt.savefig(f"{filename}.svg", bbox_inches='tight')
        plt.close()
        
        print(f"\n✅ Generated: {filename}.png | {filename}.svg")
        return filename
    
    def save_data(self, filename):
        with open(f"{filename}.json", "w") as f:
            json.dump(self.data, f, indent=2)
        print(f"✅ Saved: {filename}.json")

# RUN - Works everywhere!
if __name__ == "__main__":
    mapper = ProcessMapper()
    mapper.ask_core_questions()
    mapper.collect_steps()
    filename = mapper.generate_flowchart()
    mapper.save_data(filename)
    print("\n🎬 Video-style flowchart ready! Blender: Parse JSON → 3D.")
