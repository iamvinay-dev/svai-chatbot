import json
import os

def get_context():
    # Path to the JSON file
    json_path = os.path.join(os.path.dirname(__file__), 'college_data.json')
    
    # Base summary context
    context = """
    SVAI BOT - COMPACT KNOWLEDGE BASE: S.V. ARTS COLLEGE (AUTONOMOUS)
    
    COLLEGE INFO:
    - Managed by: TTD (Tirumala Tirupati Devasthanams)
    - Principal: Prof. N. Venugopal Reddy (9000489182)
    - Accreditation: NAAC A+ Grade (3.28 CGPA)
    - Location: Tirupati, Andhra Pradesh.
    - Timings: 09:30 AM to 04:15 PM
    """

    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 1. Extract Management
            mgt = data.get('management', {}).get('officials', [])
            context += "\nMANAGEMENT:\n" + "\n".join([f"- {o['name']} ({o['designation']})" for o in mgt[:5]])

            # 2. Extract Academic Schedule Key Dates
            sch = data.get('academic_schedule_2025_2026', {}).get('odd_semesters_I_III_V', {})
            if sch:
                context += f"\n\nODD SEMESTER: Classes from {sch.get('commencement_of_classes')}, Exams from {sch.get('sem_end_exams_theory')}."

            # 3. Extract Scholarships (Shortened)
            scholarships = data.get('scholarships', {}).get('list', [])
            context += "\n\nSCHOLARSHIPS:\n" + ", ".join([s['name'] for s in scholarships[:8]])

            # 4. Extract Departments & HODs
            context += "\n\nDEPARTMENTS & HODs:\n"
            depts = data.get('faculty_members', {}).get('departments', {})
            for dept_name, members in depts.items():
                hod = "N/A"
                if isinstance(members, list) and len(members) > 0:
                    hod = members[0].get('name', 'N/A')
                elif isinstance(members, dict):
                    # Handle nested structure like Physics/Chemistry
                    faculty = members.get('faculty', [])
                    if faculty: hod = faculty[0].get('name', 'N/A')
                context += f"- {dept_name}: {hod}\n"

            # 5. Extract Rules Summary
            context += "\nRULES: 75% attendance req. Condonation fee Rs. 500. Ragging is a crime. Uniform: Blue/Navy."
            
            return context
        except Exception as e:
            print(f"Error reading JSON: {e}")
            return context
    
    return context
