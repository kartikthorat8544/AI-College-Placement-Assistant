INTENTS = {
    "greeting": {
        "priority": 1,
        "patterns": [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ],
        "response": (
            "Hello! I am your AI College and Placement Assistant. "
            "How can I help you today?"
        )
    },

    "resume": {
        "priority": 1,
        "patterns": [
            "resume",
            "cv",
            "create resume",
            "resume format",
            "improve my resume",
            "resume preparation",
            "resume tips"
        ],
        "response": (
            "For a strong placement resume, include your skills, education, "
            "projects, internships and achievements. Keep it clear and concise."
        )
    },

    "interview": {
        "priority": 1,
        "patterns": [
            "interview",
            "interview preparation",
            "technical interview",
            "hr interview",
            "interview questions",
            "prepare for interview"
        ],
        "response": (
            "Interview preparation should include technical concepts, coding "
            "practice, project explanation and common HR questions."
        )
    },

    "python_interview": {
        "priority": 2,
        "patterns": [
            "python interview",
            "python interview questions",
            "prepare python interview",
            "python placement questions"
        ],
        "response": (
            "For a Python interview, prepare data types, functions, OOP, "
            "exception handling, modules, file handling and coding problems."
        )
    },

    "aptitude": {
        "priority": 1,
        "patterns": [
            "aptitude",
            "reasoning",
            "quantitative aptitude",
            "logical reasoning",
            "aptitude questions",
            "aptitude preparation"
        ],
        "response": (
            "For aptitude preparation, practise quantitative aptitude, logical "
            "reasoning and verbal ability regularly with timed tests."
        )
    },

    "placement": {
        "priority": 1,
        "patterns": [
            "placement",
            "placement preparation",
            "campus placement",
            "prepare for placement",
            "placement guidance"
        ],
        "response": (
            "Placement preparation should include aptitude, technical skills, "
            "projects, resume preparation, communication and mock interviews."
        )
    },

    "skills": {
        "priority": 1,
        "patterns": [
            "skills",
            "technical skills",
            "placement skills",
            "skills for placement",
            "what skills should i learn"
        ],
        "response": (
            "For software placements, focus on Python, SQL, DSA, Git, APIs, "
            "databases, basic web development and practical projects."
        )
    },

    "goodbye": {
        "priority": 1,
        "patterns": [
            "bye",
            "goodbye",
            "see you",
            "thank you",
            "thanks"
        ],
        "response": (
            "You're welcome! Keep preparing consistently. "
            "Good luck with your placements!"
        )
    }
}