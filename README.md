# Social Media API
A simple backend social media API.

### Features
- CRUD-based, with implementations for creating, reading, updating and deleting users and posts.
- Users also have the ability to vote for/like posts.
- Authentication enforced with user passwords and JSON Web Tokens.
- Authorisation alse ensured e.g. one user cannot delete another user's posts.

### Implementation
- Written in Python using the FastAPI web framework.
- Database-driven with a PostgreSQL database.
- Password hashing using Bcrypt for secure storage in the database.
- API-endpoint testing done with Postman.
- Unit-testing for all endpoints set up using the third-party PyTest Python testing library.
- Containerisation set up with Docker using Docker Images and Docker Compose for the app and the database.
- CI/CD pipeline set up with Github Actions.
- Deployed to an Ubuntu Server set up on a Raspberry Pi 4.
