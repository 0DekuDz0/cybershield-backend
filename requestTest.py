import requests

url = "http://127.0.0.1:8000/api/add_participant/"  # Replace with your actual endpoint

data = {
    "participant_name": "John Doe1",
    "participant_email": "joh@example.com",
    "participant_phone": "1234567891",
    "participant_dateOfBirth": "1995-06-15",
    "participant_skills": "Python, Django, Machine Learning",
    "participant_linkedin": "https://www.linkedin.com/in/johndoe",
    "participant_github": "https://github.com/johndoe",
    "participant_portfolio": "https://johndoe.com",
    "participant_haveParticipated": "True",
    "participant_previousExperience": "Worked on several ML projects",
    "new_team": "False",
    "team_name": "Team 1",
    # "participant_status": "Active",
    # "participant_team": "1"  # Replace with an actual team ID
}

response = requests.post(url, data=data)

print("Status Code:", response.status_code)
print("Response:", response.json())
