import json
import os

def get_context():
    # Path to the JSON file
    json_path = os.path.join(os.path.dirname(__file__), 'college_data.json')
    
    # Base context (always included)
    base_context = """
    SVAI BOT - COMPLETE DIGITAL HANDBOOK: S.V. ARTS COLLEGE (AUTONOMOUS)
    
    COLLEGE CONTACTS:
    - Office: 0877-2264602 | JEO: 2264392 | DEO: 2264522
    - Principal: Prof. N. Venugopal Reddy (1st Feb 2024 - Present)
    - Superintendent: Smt. S. Lalitha (9490370445)

    COLLEGE TIMINGS: 09:30 AM to 04:15 PM
    RULES OF DISCIPLINE:
    - Uniform: Mandatory Sky Blue Shirt & Navy Blue Pant (Boys), Blue Salwar Kameez (Girls).
    - Ragging: Strictly prohibited and punishable.
    - Attendance: 75% minimum required.
    """

    # Check if JSON file exists and load it
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert the entire JSON to a string context
                # (You can customize this to only include relevant parts)
                json_context = json.dumps(data, indent=2)
                return f"{base_context}\n\n--- ADDITIONAL COLLEGE DATA ---\n{json_context}"
        except Exception as e:
            print(f"Error reading JSON: {e}")
            return base_context
    else:
        # Fallback to the original hardcoded directory if JSON doesn't exist yet
        return base_context + """
        VISION & MISSION:
        - Vision: To transform mediocre students into socially responsible citizens through education, ethics, and spirituality.
        - Mission: To build competent, committed professionals and inculcate spiritual/moral values.

        FEES (Approx.): 
        - BA Honours (Rs. 5400), B.Com Gen (Rs. 5400), B.Com CA (Rs. 10845), B.Sc (Rs. 5600 - Rs. 11045).

        COMPUTER SCIENCE DEPARTMENT:
        - Head: Prof. K. Kameswara Rao (9550559568)
        - Faculty: Sri Chakravarthy (9505123979), Dr. Jyotsna (9704835308), Sri V. Kamalanadhan (9701602609), Sri D. Suresh Babu (9666748464).
        - Latest Courses: B.Sc Honours (Data Science, AI, Computer Science), BCA Honours, and Quantum Technologies.
        """
