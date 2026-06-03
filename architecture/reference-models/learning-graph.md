# Reference Model: Learning Graph

The learning graph connects learning artifacts and outcomes.

```text
LearningPath -> contains -> Course
Course -> contains -> Module
Course -> teaches -> Skill
Assessment -> validates -> Skill
Course -> awards -> Badge
Badge -> contributesTo -> Certification
Credential -> backedBy -> Evidence
```

The learning graph is the backbone for search, recommendations, credentials, analytics, and agentic learning workflows.
