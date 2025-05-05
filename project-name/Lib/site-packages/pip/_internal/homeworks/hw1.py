# Use this file to write your queries. Submit this file to Gradescope after finishing your homework.

# Make sure to test that this script prints out the strings (your SQL queries) correctly.

# To verify your submission is in the correct format: `python3 hw1.py`

# Make sure the program prints out your SQL statements correctly. That means the autograder will read you SQL correctly. Running the Python file will not execute your SQL statements, it simply prints them.

instr = '''Instructions:
	Please put the queries under the corresponding functions below.
	Running this python file will check if the formatting is okay.
	Example:
		def query1():
			return """
				SELECT * FROM agent
			"""
'''

def query1():
	return """
	SELECT DISTINCT L.language
	FROM agent A, languagerel LR, language L
	WHERE A.city = 'Paris' AND A.agent_id = LR.agent_id AND LR.lang_id = L.lang_id;
	"""

def query2():
	return """
	SELECT AF.title, A.agent_id, A.first, A.last, A.city
    FROM agent A
	JOIN affiliationrel AFR
	ON A.agent_id = AFR.agent_id
	JOIN affiliation AF
	ON AFR.aff_id = AF.aff_id
	WHERE A.city = 'Seattle' AND AF.title = 'FBI';
	"""

def query3():
	return """
	SELECT AF.title, A.agent_id, A.first, A.last, L.language
	FROM agent A
	JOIN affiliationrel AFR
	ON A.agent_id = AFR.agent_id
	JOIN affiliation AF
	ON AFR.aff_id = AF.aff_id
	JOIN languagerel LR
	ON A.agent_id = LR.agent_id
	JOIN language L
	ON LR.lang_id = L.lang_id
	WHERE A.city = 'Seattle' AND AF.title = 'FBI';
	"""
	
def query4():
	return """
	SELECT M.name, T.name AS team_name, A.last AS agent_lastname, L.language, S.skill
	FROM agent A
	JOIN languagerel LR
	ON A.agent_id = LR.agent_id
	JOIN language L 
	ON LR.lang_id = L.lang_id
	JOIN skillrel SR
	ON SR.agent_id = A.agent_id
	JOIN skill S
	ON S.skill_id = SR.skill_id
	JOIN teamrel TR
	ON TR.agent_id = A.agent_id
	JOIN team T
	ON TR.team_id = T.team_id
	JOIN mission M
	ON M.Team_id = T.team_id
	WHERE L.language = 'English' AND S.skill = 'Kung Fu';
	"""

def query5():
	return """
	SELECT A.agent_id, A.first, A.last, AF.title
	FROM agent A
	OUTER LEFT JOIN affiliationrel AFR
	ON A.agent_id = AFR.agent_id
	OUTER LEFT JOIN affiliation AF
	ON AFR.aff_id = AF.aff_id
	WHERE A.country = 'Brazil';
	"""

def query6():
	return """
	SELECT A.agent_id, A.first, A.last, L.language, S.skill
	FROM agent A
	JOIN languagerel LR
	ON A.agent_id = LR.agent_id
	JOIN language L
	ON LR.lang_id = L.lang_id
	LEFT OUTER JOIN skillrel SR
	ON A.agent_id = SR.agent_id
	LEFT OUTER JOIN skill S
	ON SR.skill_id = S.skill_id
	WHERE A.agent_id <= 4
	ORDER BY A.agent_id;
	"""

def query7():
	return """
	SELECT A.agent_id, A.first, A.last, L.language, S.skill
	FROM agent A
	LEFT OUTER JOIN languagerel LR
	ON A.agent_id = LR.agent_id
	LEFT OUTER JOIN language L
	ON LR.lang_id = L.lang_id
	JOIN skillrel SR
	ON A.agent_id = SR.agent_id
	JOIN skill S
	ON SR.skill_id = S.skill_id
	WHERE A.agent_id <= 4
	ORDER BY A.agent_id;
	"""

def query8():
	return """
	SELECT A.agent_id, A.first, A.last, L.language, S.skill
	FROM agent A
	JOIN languagerel LR
	ON A.agent_id = LR.agent_id
	JOIN language L
	ON LR.lang_id = L.lang_id
	JOIN skillrel SR
	ON A.agent_id = SR.agent_id
	JOIN skill S
	ON SR.skill_id = S.skill_id
	WHERE A.agent_id <= 4
	ORDER BY A.agent_id;
	"""

def query9():
	return """
	SELECT COUNT (DISTINCT language) AS lan_count
	FROM language;
	"""

def query10():
	return """
	SELECT COUNT (DISTINCT team_id)  AS teams_count
	FROM team
	WHERE meeting_frequency = 'weekly';
	"""

def query11():
	return """
	SELECT clearance_id, ROUND(AVG(salary), 2) AS average_salary
	FROM agent
	WHERE city = 'Miami'
	GROUP BY clearance_id
	HAVING AVG(salary) > 200000;
	"""

def query12():
	return """
	SELECT S.skill, COUNT(DISTINCT A.agent_id) AS cnt
	FROM agent A
	JOIN skillrel SR
	ON A.agent_id = SR.agent_id
	JOIN skill S
	ON SR.skill_id = S.skill_id
	GROUP BY skill
	HAVING COUNT(DISTINCT A.agent_id) <= 20;
	"""

def query13():
	return """
	SELECT L.language AS 'skills and languages'
	FROM language L
	JOIN languagerel LR
	ON LR.lang_id = L.lang_id
	WHERE LR.agent_id = 1
	UNION ALL
	SELECT S.skill AS 'skills and languages'
	FROM skill S
	JOIN skillrel SR
	ON SR.skill_id = S.skill_id
	WHERE SR.agent_id = 1;
	"""

def query14():
	return """
	SELECT concat('affiliation: ', AF.title) AS aff_city
	FROM affiliation AF
	JOIN affiliationrel AFR
	ON AFR.aff_id = AF.aff_id
	JOIN teamrel TR
	ON AFR.agent_id = TR.agent_id
	JOIN mission M
	ON TR.team_id = M.Team_id
	WHERE M.name = 'Media Blanket'
	UNION
	SELECT concat('city: ', A.city) AS aff_city
	FROM agent A
	JOIN teamrel TR
	ON A.agent_id = TR.agent_id
	JOIN mission M
	ON TR.team_id = M.Team_id
	WHERE M.name = 'Media Blanket';
	"""

def query15():
	return """
	SELECT T.name AS team_name
	FROM team T
	JOIN teamrel TR
	ON T.team_id = TR.team_id
	JOIN skillrel SR
	ON SR.agent_id = TR.agent_id
	JOIN skill S
	ON SR.skill_id = S.skill_id
	WHERE S.skill = 'Kung Fu'
	INTERSECT
	SELECT T.name AS team_name
	FROM team T
	JOIN teamrel TR
	ON T.team_id = TR.team_id
	JOIN languagerel LR
	ON LR.agent_id = TR.agent_id
	JOIN language L
	ON LR.lang_id = L.lang_id
	WHERE L.language = 'English';
	"""

# Do not edit below

if __name__ == "__main__":
	try:
		if all(type(eval(f'print(t:=query{f+1}()),t')[1])==str for f in range(15)):
			print(f'Your submission is valid.')
		else:
			raise TypeError('Invalid Return Types.')
	except Exception as e:
		print(f'Your submission is invalid.\n{instr}\n{e}')
