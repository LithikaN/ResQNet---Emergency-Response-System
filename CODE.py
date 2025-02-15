# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 23:51:40 2025

@author: lithi
"""

# ResQNet -  Emergency Response System

users_db = {
    "volunteers": [],
    "emergencies": []
}


def register_user(name, location, is_volunteer=False, skills=None):
    user_id = f"user_{len(users_db['volunteers']) + 1}"
    user = {
        "user_id": user_id,
        "name": name,
        "location": location,  # Tuple (latitude, longitude)
        "is_volunteer": is_volunteer,
        "skills": skills if skills else []
    }
    if is_volunteer:
        users_db["volunteers"].append(user)
    return user


def trigger_emergency(user_id, location, emergency_type):
    emergency_id = f"emergency_{len(users_db['emergencies']) + 1}"
    emergency = {
        "emergency_id": emergency_id,
        "user_id": user_id,
        "location": location,
        "emergency_type": emergency_type,
        "status": "Pending"  # Pending, Accepted, Resolved
    }
    users_db["emergencies"].append(emergency)
    return emergency


def find_nearby_volunteers(emergency_location, max_distance_km=5):
    nearby_volunteers = []
    for volunteer in users_db["volunteers"]:
        distance = ((volunteer["location"][0] - emergency_location[0])**2 + 
                   (volunteer["location"][1] - emergency_location[1])*2)*0.5
        if distance <= max_distance_km:
            nearby_volunteers.append(volunteer)
    return nearby_volunteers


def match_volunteers_to_emergency(emergency):
    nearby_volunteers = find_nearby_volunteers(emergency["location"])
    if nearby_volunteers:
        matched_volunteer = nearby_volunteers[0]  # Pick the first volunteer for simplicity
        emergency["status"] = "Accepted"
        return matched_volunteer
    else:
        return None


def resolve_emergency(emergency):
    emergency["status"] = "Resolved"
    print(f"Emergency {emergency['emergency_id']} has been resolved.")


def main():
    
    volunteer1 = register_user("John Doe", (37.7749, -122.4194), is_volunteer=True, skills=["CPR", "First Aid"])
    volunteer2 = register_user("Jane Smith", (37.7849, -122.4294), is_volunteer=True, skills=["EMT"])

    
    user = register_user("Alice Johnson", (37.7750, -122.4180))

    
    emergency = trigger_emergency(user["user_id"], user["location"], "Medical Emergency")
    print(f"Emergency {emergency['emergency_id']} triggered by {user['name']} at {emergency['location']}.")

    
    matched_volunteer = match_volunteers_to_emergency(emergency)
    if matched_volunteer:
        print(f"Alert sent to {matched_volunteer['name']} (ID: {matched_volunteer['user_id']}) for emergency {emergency['emergency_id']}.")
        resolve_emergency(emergency)
    else:
        print("No nearby volunteers available.")

    
    print("\nDatabase State:")
    print("Volunteers:", users_db["volunteers"])
    print("Emergencies:", users_db["emergencies"])

if __name__ == "_main_":
    main()