import json
from processpiper import ProcessMap, EventType, ActivityType, GatewayType

class ProcessMapper:
    def __init__(self):
        self.data = {"core": {}, "steps": [], "connections": []}
        self.pm = None
        
    def ask_core_questions(self):
        """Video's six questions."""
        print("\n## CORE QUESTIONS")
        self.data["core"] = {
            "name": input("Process name (e.g., 'HR Onboarding'): "),
            "why": input("Purpose/goal: "),
            "roles": input("Roles (comma-separated): ")
        }
    
    def collect_steps(self):
        """Interactive step collection."""
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
                "type": input("Type (task/decision/start/end): ").lower(),
                "lane": input("Lane/Pool (e.g., 'HR/Recruiter'): ").strip()
            }
            steps.append(step)
            step_id += 1
        
        self.data["steps"] = steps
    
    def build_process_map(self):
        """Generate BPMN using reference API."""
        process_name = self.data["core"]["name"]
        
        with ProcessMap(process_name, colour_theme="BLUEMOUNTAIN") as pm:
            self.pm = pm
            
            # Parse lanes/pools from steps
            pools = {}
            lanes = {}
            
            for step in self.data["steps"]:
                pool_name, lane_name = step["lane"].split("/", 1) if "/" in step["lane"] else (process_name, step["lane"])
                
                # Create pool if new
                if pool_name not in pools:
                    pools[pool_name] = pm.add_pool(pool_name)
                
                # Create lane if new
                if lane_name not in lanes or lanes[lane_name] != pools[pool_name]:
                    lane_obj = pools[pool_name].add_lane(lane_name)
                    lanes[lane_name] = pools[pool_name]
                
                # Add element based on type
                lane = pools[pool_name].add_lane(lane_name)
                if step["type"] == "start":
                    elem = lane.add_element(step["name"], EventType.START)
                elif step["type"] == "end":
                    elem = lane.add_element(step["name"], EventType.END)
                elif step["type"] == "decision":
                    elem = lane.add_element(step["name"], GatewayType.EXCLUSIVE)
                else:  # task
                    elem = lane.add_element(step["name"], ActivityType.TASK)
                
                step["element"] = elem
            
            # Auto-connect sequential (extend for manual connections)
            prev_elem = None
            for step in self.data["steps"]:
                if prev_elem:
                    prev_elem.connect(step["element"], step["name"])
                prev_elem = step["element"]
            
            pm.set_footer(f"Automated from {self.data['core']['why'][:60]}...")
            pm.draw()
    
    def save_all(self):
        """Save PNG + JSON."""
        filename = self.data["core"]["name"].lower().replace(" ", "_")
        self.pm.save(f"{filename}.png")
        
        with open(f"{filename}.json", "w") as f:
            json.dump(self.data, f, indent=2)
        
        print(f"\n✅ Generated: {filename}.png | {filename}.json")

# RUN
if __name__ == "__main__":
    mapper = ProcessMapper()
    mapper.ask_core_questions()
    mapper.collect_steps()
    mapper.build_process_map()
    mapper.save_all()
    print("\n🎬 Video-exact BPMN ready! Perfect for ClickUp/SOPs.")
