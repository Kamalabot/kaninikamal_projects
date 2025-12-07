import json
import os
from processpiper import ProcessMap, EventType, ActivityType, GatewayType

class FileProcessMapper:
    def __init__(self, filename="process.txt"):
        self.filename = filename
        self.data = {"core": {}, "steps": []}
        self.elements = {}
        
    def load_from_file(self):
        """Parse process.txt format."""
        if not os.path.exists(self.filename):
            print(f"❌ {self.filename} not found. Creating example...")
            self.create_example_file()
            return False
        
        print(f"📖 Loading {self.filename}...")
        with open(self.filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Parse format: ProcessName | Purpose | Role1,Role2
        # Step1|task|Pool1/Lane1
        # Step2|decision|Pool1/Lane2
        self.data["core"]["name"] = lines[0].split('|')[0].strip()
        self.data["core"]["why"] = lines[1].split('|')[0].strip()
        
        # Parse steps (line 3+)
        for i, line in enumerate(lines[2:], 1):
            if '|' in line:
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    step = {
                        "id": f"S{i}",
                        "name": parts[0].strip(),
                        "type": parts[1].strip() if len(parts) > 1 else "task",
                        "pool_lane": parts[2].strip()
                    }
                    self.data["steps"].append(step)
        
        print(f"✅ Loaded: {self.data['core']['name']} ({len(self.data['steps'])} steps)")
        return True
    
    def create_example_file(self):
        """Create process.txt with 5-step HR example."""
        example = '''HR Onboarding|Streamline new hire process|HR,Recruiter,Manager
Purpose: Reduce time-to-hire by 30%
Job Req Received|start|HR/HR
Post Job Ad|task|HR/Recruiter
Screen Resumes?|decision|HR/Recruiter
Conduct Interview|task|HR/Manager
Send Offer & Onboard|end|HR/HR'''
        
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(example)
        print(f"✅ Created example {self.filename}")
    
    def build_process_map(self):
        """Generate BPMN from parsed data."""
        process_name = self.data["core"]["name"]
        
        with ProcessMap(process_name, colour_theme="BLUEMOUNTAIN") as pm:
            self.pm = pm
            
            # Ensure minimum steps
            if not self.data["steps"]:
                self.data["steps"] = [{
                    "id": "S1", "name": "Default Task", "type": "task", 
                    "pool_lane": f"{process_name}/Team"
                }]
            
            pool_dict = {}
            lane_dict = {}
            
            for step in self.data["steps"]:
                # Parse pool/lane: Pool1/Lane1 or just Lane1
                if '/' in step["pool_lane"]:
                    pool_name, lane_name = step["pool_lane"].split('/', 1)
                else:
                    pool_name = process_name
                    lane_name = step["pool_lane"]
                
                # Create pool
                if pool_name not in pool_dict:
                    pool_obj = pm.add_pool(pool_name)
                    pool_dict[pool_name] = pool_obj
                
                # Create lane
                lane_key = f"{pool_name}/{lane_name}"
                if lane_key not in lane_dict:
                    lane_obj = pool_dict[pool_name].add_lane(lane_name)
                    lane_dict[lane_key] = lane_obj
                
                lane = lane_dict[lane_key]
                
                # Add element
                elem_type = {
                    "start": EventType.START,
                    "end": EventType.END,
                    "decision": GatewayType.EXCLUSIVE
                }.get(step["type"], ActivityType.TASK)
                
                elem = lane.add_element(step["name"], elem_type)
                self.elements[step["id"]] = elem
            
            # Sequential connections
            step_ids = sorted(self.elements.keys(), key=lambda x: int(x[1:]))
            for i in range(len(step_ids)-1):
                self.elements[step_ids[i]].connect(self.elements[step_ids[i+1]])
            
            pm.set_footer(f"File: {self.filename} | {self.data['core']['why'][:50]}...")
            pm.draw()
    
    def save_all(self):
        """Save PNG + JSON."""
        filename = self.data["core"]["name"].lower().replace(" ", "_")
        self.pm.save(f"{filename}.png")
        
        with open(f"{filename}.json", "w") as f:
            json.dump(self.data, f, indent=2)
        
        print(f"\n🎉 SUCCESS: {filename}.png | {filename}.json")

# RUN
if __name__ == "__main__":
    mapper = FileProcessMapper("process.txt")
    if mapper.load_from_file():
        mapper.build_process_map()
        mapper.save_all()
    print("\n📝 Edit process.txt → rerun for new BPMN!")
