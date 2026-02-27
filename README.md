# Open Ocean Collective

## Project Overview
Surfing in the UK is often perceived as:

Exclusive

Limited to coastal areas

Lacking ethnic and socioeconomic diversity

Open Ocean Collective aims to challenge this perception by promoting surfing among underrepresented communities in the UK.

The platform allows a diverse group of surfers to tell their personal stories about how they got into surfing and organisises monthly surf trips open to all!


## UX Design Process (LO1.1 & LO1.5)

Flow Chart: [Flow chart of initial user navigation through website]   (https://res.cloudinary.com/dwe00uiuy/image/upload/v1772198092/Screenshot_2026-02-27_at_13.01.18_qxvjc5.png)

A flow chart was created to visualise how users navigate the Open Ocean Collective website. It outlines the journey from landing on the homepage to interacting with the core features:

Visiting the homepage

Browsing shared stories

Clicking on a story to read in full

Commenting on stories

Exploring meet-up events

Navigating back to the homepage or other sections

This flow chart helped ensure a logical, intuitive navigation, reducing confusion for users and improving overall usability. I didn't end up implimenting user profiles as it became overcomplicated and wasn't nessesary for the MVP. 

Wireframes: 

Wireframes were designed for the main pages of the application to plan layout, structure, and user interactions:

Homepage: Highlights featured stories and upcoming meet-ups

[Screenshot of homepage wireframe] (https://res.cloudinary.com/dwe00uiuy/image/upload/v1772203565/Screenshot_2026-02-27_at_14.44.20_vievaf.png)

Story Page: Displays full story text, allows users to comment, edit and delete thier comments
 
[Screenshot of story page wirframe] (https://res.cloudinary.com/dwe00uiuy/image/upload/v1772203573/Screenshot_2026-02-27_at_14.44.59_fpwgyk.png)

Surf Trips Page: Users can sign on for a surf trip which gets sent to the admin page. 

[Screenshot of surf trip page wireframe] (https://res.cloudinary.com/dwe00uiuy/image/upload/v1772203571/Screenshot_2026-02-27_at_14.44.49_l4xtvv.png)

Log in

[Screenshot of log in page wireframe] (https://res.cloudinary.com/dwe00uiuy/image/upload/v1772203566/Screenshot_2026-02-27_at_14.44.32_sxf4ke.png)

Sign Up

[Screenshot of sign up page wireframe] (https://res.cloudinary.com/dwe00uiuy/image/upload/v1772203566/Screenshot_2026-02-27_at_14.44.39_o2rcpp.png)

Story creation

[Screenshot of upload story page wirefame] (https://res.cloudinary.com/dwe00uiuy/image/upload/v1772203565/Screenshot_2026-02-27_at_14.45.36_ylqrqq.png)


## Agile Methodology (LO1.3)
Agile methodology was used to guide the development of Open Ocean Collective, ensuring that features were built incrementally and aligned with the project’s core objective of promoting diverse surfing experiences. Project planning and task tracking were managed using GitHub Projects, where user stories were organised using a Kanban-style board.

Key User Story

One of the central user stories for the project was:

As a user, I can view stories from other users, so that I can learn about diverse surfing experiences and stay engaged with the community.

This story directly supports the project’s mission of increasing visibility and representation within UK surfing culture.

Acceptance Criteria

The following acceptance criteria were defined before development began:

Users can view a feed of stories from all users.

Stories display the title, author, and timestamp.

Clicking a story opens the full content.

Users cannot edit or delete stories that are not their own.

Stories display correctly on desktop and mobile devices (responsive design).

Task Breakdown

This user story was broken down into smaller, manageable development tasks:

Create a custom Story model using Django’s ORM

Implement a view to retrieve and display all stories

Design a responsive template to render the story feed

Create a detail view for full story content

Implement access control to restrict editing and deletion

Test responsiveness across different screen sizes

Each task was moved across the project board from To Do → In Progress → Testing → Done, ensuring structured progress and continuous validation against the acceptance criteria.

Iterative Development

The feature was developed iteratively:

Database model created and migrated

Basic story list view implemented

Detail page functionality added

Access restrictions implemented

Responsive styling refined

Testing carried out to verify all acceptance criteria were met

This Agile approach ensured the final implementation fully satisfied the original user story while maintaining alignment with the overall project goals.



## Database Design & Development (LO1.2, LO2.1, LO7.1)
🗄️ Database Design & Application Logic

(LO1.2, LO2.1, LO7.1)

The Open Ocean Collective application is built using the Django framework and its built-in ORM to manage data securely and efficiently.

The database was designed to support:

Story creation and sharing

Commenting functionality

Meetup listings

User authentication and access control

Custom Data Models
1️⃣ Story Model

The Story model stores community-submitted surfing experiences.

Each story includes:

title

content

image_url (optional)

author_user (ForeignKey to Django User)

Timestamp fields (for ordering and tracking updates)

A one-to-many relationship exists between users and stories:

One user → Many stories

Each story → One author

This relationship is enforced using Django’s ForeignKey field to ensure data integrity.

2️⃣ Comment Model

The Comment model allows users to engage with stories.

Each comment includes:

story (ForeignKey to Story)

user (ForeignKey to User)

content

Timestamp field

This creates:

One story → Many comments

One user → Many comments

If a story is deleted, its related comments are also removed using cascading delete behaviour.

3️⃣ Meetup Model

The Meetup model supports surf trip listings, allowing users to view available surf meetups. Although sign-ups are currently handled via form submission and messaging feedback, the structure allows for database-backed storage via MeetupSignup.

Database Operations Using Django ORM

All database interactions are handled through Django’s ORM, including:

Retrieving all stories (Story.objects.all())

Fetching individual stories by ID

Creating new stories

Creating comments linked to a specific story

Updating story and comment content

Deleting stories and comments

Handling exceptions using try/except blocks

Using the ORM ensures:

Protection against SQL injection

Clean, readable queries

Secure data handling

Maintainable application logic

🔁 CRUD Functionality

(LO2.2)

The application implements full CRUD functionality for both Stories and Comments.

Story CRUD
Create

Authenticated users can create a story via the create_story view.
The system validates required fields before saving the story to the database.

Read

All users can view the story feed via the stories view.
Each story displays:

Title

Author

Content preview

Associated comments

Clicking into a story reveals full content.

Update

Authenticated users can edit their own stories using the edit_story view.
The system checks:

if story.author_user != request.user:

This prevents users from editing stories that are not theirs.

Delete

Users can delete their own stories via the delete_story view.
A confirmation page is displayed before permanent deletion.

Comment CRUD
Create

Authenticated users can post comments on stories.
If a user is not logged in, they are redirected to the login page.

Update

Users may edit only their own comments via the edit_comment view.

Delete

Users may delete only their own comments via the delete_comment view.

Permission checks ensure users cannot modify other users’ content.

🔐 Authentication & Access Control

(LO3)

Authentication is implemented using Django’s built-in authentication system and Django Allauth for registration.

Features Implemented:

User registration via signup form

Secure login using authenticate()

Custom logout functionality

Login-required decorators for protected views

Role-based content restriction (users can only edit/delete their own content)

The @login_required decorator is applied to:

Story creation

Story editing

Story deletion

Comment editing

Comment deletion

Unauthenticated users attempting restricted actions are redirected and shown clear feedback messages.

💬 User Notifications

(LO2.3)

The application uses Django’s messages framework to provide real-time feedback, including:

Successful login/logout messages

Story creation confirmation

Comment posting confirmation

Error messages for invalid input

Permission denial notifications

This improves usability and ensures users are always informed of the outcome of their actions.

🧠 Custom Python Logic & Code Quality

(LO1.4)

The project includes custom Python logic demonstrating:

Conditional statements (if/else)

Authentication checks

Permission validation

Exception handling (try/except)

Input validation using .strip() to prevent empty submissions

File naming follows consistent lowercase conventions without spaces to ensure cross-platform compatibility.

Code readability was prioritised through:

Clear function naming

Logical view separation

Structured indentation

Descriptive variable names

The project follows the guidelines set out in PEP 8 for Python code style.


## Features & CRUD Functionality (LO2.2)
Open Ocean Collective implements full CRUD (Create, Read, Update, Delete) functionality for both Stories and Comments, allowing users to actively participate in the community.

Story Features

Create
Logged-in users can create and publish their own surfing stories using a submission form.

Read
All users can view a feed of stories shared by the community. Each story displays the title, author, timestamp, and full content.

Update
Users can edit their own stories. The system checks that the logged-in user is the original author before allowing changes.

Delete
Users can delete their own stories. A confirmation page is shown before deletion to prevent accidental removal.

Comment Features

Create
Logged-in users can post comments on stories to engage with other members.

Read
Comments are displayed beneath each story, allowing users to view discussions.

Update
Users can edit their own comments.

Delete
Users can delete their own comments, ensuring they maintain control over their contributions.

Access control ensures that users cannot edit or delete content created by others, maintaining security and data integrity across the platform.


## Forms & Validation (LO2.4)

## User Notifications (LO2.3)

## Authentication, Authorisation & Access Control (LO3)

## Code Quality & Custom Logic (LO1.4)

## Testing (LO4)

## Version Control & GitHub (LO5)

## Deployment (LO6)

## AI Tools Reflection (LO8)

## Technologies Used

## Credits
