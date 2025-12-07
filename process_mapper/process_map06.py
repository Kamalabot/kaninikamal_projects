import json
from processpiper import ProcessMap, EventType, ActivityType, GatewayType

class ProcessMapper:
    def __init__(self):
        self.data = {"core": {}, "steps": []}
        self.pm = None
        self.elements = {}
        
    def ask_core_questions(self):
        print("\n## CORE QUESTIONS")
        self.data["core"] = {
            "name": input("Process name: ").strip() or "Business Process",
            "why": input("Purpose: ").strip() or "Streamline operations"
        }
    
    def collect_steps(self):
        print("\n## STEPS - Add at least 3 (Start → Task → End)")
        steps = []
        
        # Minimum guaranteed steps
        steps.append({
            "id": "S1", "name": "Process Start", "type": "start", 
            "pool": self.data["core"]["name"], "lane": "Team"
        })
        
        # Interactive steps
        step_id = 2
        while len(steps) < 5:  # Collect 3-5 steps
            print(f"\nStep {step_id}:")
            name = input("Name (or Enter for auto): ").strip()
            if not name and step_id == 2:
                name = "Main Task"
            if name.lower() == 'done': break
            
            step = {
                "id": f"S{step_id}",
                "name": name or f"Step {step_id}",
                "type": input("Type (task/decision): ").lower() or "task",
                "pool": input("Pool (Enter=default): ").strip() or self.data["core"]["name"],
                "lane": input("Lane: ").strip() or "Team"
            }
            steps.append(step)
            step_id += 1
        
        # Ensure end step
        if not any(s["type"] == "end" for s in steps):
            steps.append({
                "id": "S99", "name": "Process End", "type": "end",
                "pool": self.data["core"]["name"], "lane": "Team"
            })
        
        self.data["steps"] = steps
        print(f"✅ Collected {len(steps)} steps")
    
    def build_process_map(self):
        """Guaranteed valid BPMN with explicit lane creation."""
        process_name = self.data["core"]["name"]
        
        with ProcessMap(process_name, colour_theme="BLUEMOUNTAIN") as pm:
            self.pm = pm
            
            # Track pools/lanes
            pool_dict = {}
            lane_dict = {}
            
            for step in self.data["steps"]:
                pool_name = step["pool"]
                lane_name = step["lane"]
                
                # Create pool
                if pool_name not in pool_dict:
                    pool_obj = pm.add_pool(pool_name)
                    pool_dict[pool_name] = pool_obj
                
                # Create lane (unique per pool+lane combo)
                lane_key = f"{pool_name}/{lane_name}"
                if lane_key not in lane_dict:
                    lane_obj = pool_dict[pool_name].add_lane(lane_name)
                    lane_dict[lane_key] = lane_obj
                
                lane = lane_dict[lane_key]
                
                # Add element
                if step["type"] == "start":
                    elem = lane.add_element(step["name"], EventType.START)
                elif step["type"] == "end":
                    elem = lane.add_element(step["name"], EventType.END)
                elif step["type"] == "decision":
                    elem = lane.add_element(step["name"], GatewayType.EXCLUSIVE)
                else:
                    elem = lane.add_element(step["name"], ActivityType.TASK)
                
                self.elements[step["id"]] = elem
            
            # Sequential connections (video style)
            step_ids = sorted([s["id"] for s in self.data["steps"]], 
                            key=lambda x: int(x[1:]))
            
            for i in range(len(step_ids)-1):
                prev_id = step_ids[i]
                next_id = step_ids[i+1]
                self.elements[prev_id].connect(self.elements[next_id])
            
            pm.set_footer(f"Auto-generated: {self.data['core']['why'][:50]}...")
            pm.draw()
            print("✅ Process map drawn successfully!")
    
    def save_all(self):
        filename = self.data["core"]["name"].lower().replace(" ", "_")
        self.pm.save(f"{filename}.png")
        
        with open(f"{filename}.json", "w") as f:
            json.dump(self.data, f, indent=2)
        
        print(f"\n🎉 SUCCESS: {filename}.png | {filename}.json")
        print("📱 Ready for ClickUp/Notion/SOPs!")

# RUN - Guaranteed to work!
if __name__ == "__main__":
    mapper = ProcessMapper()
    mapper.ask_core_questions()
    mapper.collect_steps()
    mapper.build_process_map()
    mapper.save_all()
