import streamlit as st
import heapq

class Candidate:
    def __init__(self, name, qualification, skills):
        self.name = name
        self.qualification = qualification
        self.skills = skills
        self.wait_time = 0
        self.priority = 0

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.wait_time < other.wait_time
        return self.priority < other.priority

def filter_candidates(applicants, qualification_criteria):
    filtered = [c for c in applicants if c.qualification in qualification_criteria]
    return filtered

def calculate_priority(candidate):
    if candidate.skills[0] == "C++":
        candidate.priority = 1
    elif candidate.skills[0] == "HTML":
        candidate.priority = 2
    else:
        candidate.priority = 3

def display_selected_candidates(candidates):
    st.write("\nSelected Candidates for Interview:")
    for c in candidates:
        st.write(f"Name: {c.name}, Qualification: {c.qualification}")

def apply_priority_aging(pq):
    temp = []
    while pq:
        c = heapq.heappop(pq)
        c.wait_time += 1
        c.priority += c.wait_time
        temp.append(c)
    for c in temp:
        heapq.heappush(pq, c)

def schedule_interviews(pq):
    st.write("\nInterview Schedule (based on priority):")
    if not pq:
        st.write("No candidates available for interviews.")
        return
    slot = 1
    while pq:
        c = heapq.heappop(pq)
        st.write(f"Slot {slot}: {c.name} (Priority: {c.priority}, Wait Time: {c.wait_time})")
        slot += 1

def main():
    st.title("Candidate Interview Scheduler")
    st.write("Enter the number of candidates:")
    n = st.number_input("Number of candidates", value=1, step=1)

    applicants = []
    for i in range(n):
        st.write(f"Enter details for candidate {i + 1}:")
        name = st.text_input(f"Name", key=f"candidate_{i}_name")
        common_qualifications = ["BCA", "MCA", "BSCCS","MSCCS", "Other"]
        selected_qualification = st.selectbox(f"Qualification", common_qualifications, key=f"candidate_{i}_qualification")
        if selected_qualification == "Other":
            qualification = st.text_input(f"Please specify qualification:", key=f"candidate_{i}_other_qualification")
        else:
            qualification = selected_qualification
        skills = []
        for j in range(3):
            skills.append(st.text_input(f"Skill {j + 1}", key=f"candidate_{i}_skill_{j}"))
        candidate = Candidate(name, qualification, skills)
        calculate_priority(candidate)
        applicants.append(candidate)

    st.write("Filtering candidates by qualification...")
    qualification_criteria = ["BCA", "MCA", "BSCCS","MSCCS"]
    filtered_candidates = filter_candidates(applicants, qualification_criteria)

    if not filtered_candidates:
        st.write("No candidates meet the qualification criteria.")
        return

    display_selected_candidates(filtered_candidates)

    st.write("Scheduling interviews...")
    pq = []
    for c in filtered_candidates:
        heapq.heappush(pq, c)

    apply_priority_aging(pq)
    schedule_interviews(pq)

if st.checkbox("Run"):
    main()
