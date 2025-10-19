# Team info function for Developer, DevOps, and Security teams
def get_team_info() -> dict:
	"""
	Returns information about Developer, DevOps, and Security teams,
	including members, skills, and contact information.
	"""
	return {
		"Developer": {
			"contact": "dev-team@example.com",
			"members": [
				{"name": "Alice Smith", "skills": ["Python", "React", "APIs"]},
				{"name": "Bob Lee", "skills": ["Java", "Spring Boot", "SQL"]},
				{"name": "Carol Jones", "skills": ["C#", ".NET", "Azure"]},
			]
		},
		"DevOps": {
			"contact": "devops-team@example.com",
			"members": [
				{"name": "David Kim", "skills": ["Azure DevOps", "Docker", "Kubernetes"]},
				{"name": "Eva Brown", "skills": ["Terraform", "CI/CD", "Linux"]},
			]
		},
		"Security": {
			"contact": "security-team@example.com",
			"members": [
				{"name": "Frank Green", "skills": ["Penetration Testing", "SIEM", "Incident Response"]},
				{"name": "Grace White", "skills": ["IAM", "Network Security", "Compliance"]},
			]
		}
	}
