
## Team Project Planner

A backend application to manage a base of users with functionality for team creation and a project board for task assignment. Uses Django as the primary framework, connected to a postgreSQL database.

### Database

Postgresql is used as the database management system. This provides a few advantages over using a file system to persist db data.

* Faster retrieval of data

* Allows usage of django's inbuilt ORM methods for search and filter queries

* Cleaner code and scalable application

#### Connecting to Database
Create database with name, giving access to user with password and make the respective changes within the 'project_planner/settings.py' file in the 'DATABASES' variable as follows:

	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.postgresql_psycopg2',
	        'NAME': 'project_planner',
	        'USER': 'project_planner_user',
	        'PASSWORD': 'project_planner_pass',
	        'HOST': 'localhost',
	        'PORT': '5432',
	    }
	}

Host and port values may differ based on your local machine.
Once completed you are ready to run model migrations. Cd over to the root directory and run:

	python3 manage.py migrate 
This should create the necessary tables and relations between our models according to the specified schema , Finally to get the server up, run :

	python3 manage.py runserver
Now you can start using the APIs.

### APIs
The application's default port is 8000 and every route should be preceded by "http://localhost:8000/"
#### 1. User
All API calls to the user model must be of the format:

	http://localhost:8000/users/	
**List Users**
The above mentioned route by itself when run on a browser or when run through postman's GET request function renders a json list of all users:

	[{
		"name": <user_name>,
		"diplay_name": <display_name>,
		"description": <description>,
		"created_at": <created_at>
	}]	
**Create User**
Path to be used:

	http://localhost:8000/users/create/
Post request using Postman, the body of which must be in the format:

	{
		"name": "Issac Newton",
		"display_name": "Issac",
		"description": "claims to have discovered gravity."
	}	
*name* and *display_name* are required parameters. *Name* must be unique.
Response consists of user id when record is successfully created.

	{
		"id": 1
	}
**Describe User**
Path : 

	http://localhost:8000/users/describe/
Request body (POST) structure:

	{
		"id":  1
	}
Response format: 

	{
		"name": <user_name>,
		"diplay_name": <display_name>,
		"description": <description>,
		"created_at": <created_at>
	}
**Update User**
Path: 

	http://localhost:8000/users/update/
Request body: 

	{
		"id":  1,
		"user":  {
					"display_name": "Newton",
					"description": "I got hit by an apple." 
				 }
	}
Response format:

	{
		"name": <name>,
		"display_name": <display_name>,
		"description": <description>,
		"created_at": <date-time value>,
		"updated_at": <date-time value>
	}
**Get Teams**
Path:

	http://localhost:8000/users/get_teams/
Request Body:

	{
		"id":  1
	}
Response Format (json list):

	[{
		"name": <team_name>,
		"description": <team_description>,
		"created_at": <date-time value>
	}]
#### 2. Team
All API calls to the Team model must be of the format:

	http://localhost:8000/teams/
**List Teams**
Get request to the base teams' url would render a json list of all teams as follows:

	[{
		"name": <team_name>,
		"description": <team_description>,
		"admin": <team_admin_id>,
		"users": [<user_id_1>, <user_id_2>],
		"created_at": <date-time value>
	}]

**Create Team**
Path:

	http://localhost:8000/teams/create/
POST request body:

	{
		"name": <team_name>,
		"admin": <team_admin_id>,
		"description": <team_description>,
		"users": [<user_id_1>, <user_id_2>]
	}
Response format:

	{
		"id": <team_id>
	}
*name* and *admin_id* fields are mandatory. *name* must be unique.
**Describe Team**
Path:

	http://localhost:8000/teams/describe/
Request body:

	{
		"id":  1
	}
Response format:

	{
		"name": <team_name>,
		"description": <team_description>,
		"admin": <team_admin_id>,
		"created_at": <date-time value>
	}
**Update Team**
Path: 

	http://localhost:8000/teams/update/
Request body: 

	{
		"id":  1,
		"team":  {
					"name":  <new_team_name>,
					"description":  <new_team_description>,
					"admin": <new_team_admin> 
				 }
	}
Response format:

	{
		"name": <name>,
		"admin": <team_admin_id>,
		"description": <description>,
		"created_at": <date-time value>,
		"updated_at": <date-time value>
	}
**Add Users**
Path:

	http://localhost:8000/teams/add_users/
Request Body:

	{
		"id": 2,
		"users": [5, 6, 4]
	}
Response Format:

	{
        "name": <team_name>,
        "admin": <team_admin_id>,
        "description": <team_description>,
        "users": <team_users>,
        "created_at": <date-time value>,
        "updated_at": <date-time value>
    }
Will only add users that exist within database and are not already part of the team
**Remove Users**
Path:

	http://localhost:8000/teams/remove_users/
Request Body:

	{
		"id": <team_id>,
		"users": [4]
	}
Response Format:

	{
        "name": <team_name>,
        "admin": <team_admin_id>,
        "description": <team_description>,
        "users": <team_users>,
        "created_at": <date-time value>,
        "updated_at": <date-time value>
    }
**List Users**
Path:

	http://localhost:8000/teams/list_users/
Request Body:

	{
    "id": <team_id>
	}
Response Format:
JSON list of all users belonging to team.

	[
		{
			"id": <user_id>, 
			"name": <user_name>,
			"display_name": <user_display_name>,
			"admin": <true/false value>
		}
	]
#### 3. Board
**Create Board**
Path:

	http://localhost:8000/boards/create/
POST request body:

	{
		"name": <board_name>,
		"description": <board_description>,
		"team_id": <team_id>
	}
Response format:

	{
		"id": <board_id>
	}
*name* and *team_id* fields are mandatory. *name* must be unique for a team i.e. combination of *name* and *team_id* should be unique. If board already exists and is closed, it will be re-opened.

**Close Board**
Path:

	http://localhost:8000/boards/close/
Request Body:

	{
		"id": <board_id>
	}
Response format:

	{
		"status": <new_board_status>
	}
Closes board only when all tasks belonging to the board have a status of "COMPLETE".

**Add Task**
add new task to a board
Path:

	http://localhost:8000/boards/add_task/
Request Body:

	{
		"title": <task_title>,
		"board_id": <board_id>,
		"description": <task_description>,
		"user_id": <task_user_id>
	}
Response format:

	{
		"id": <task_id>
	}
*title*, *board_id* and *user_id* are mandatory fields.  A task can be added only to an open board and if user_id is part of team that manages the board.

**Update Task Status**
Path:

	http://localhost:8000/boards/update_task/
Request Body:

	{
    	"id": <task_id>,
    	"status": "COMPLETE"
	}
Response Format:

	{"Success"/"Error": <new_status>/<error_message>}
Task status is "OPEN" by default. It can take values "IN_PROGRESS", "COMPLETE". Anything else would trigger error response.

**List Boards**
list all boards that are managed by a team
Path:

	http://localhost:8000/boards/list_boards/
Request Body:

	{
		"id": <team_id>
	}
Response Format:
JSON list of board details

	[
		{
			"id": board.id, 
			"name": board.name, 
		}
	]

**List Tasks**
list all tasks that are managed by a team
Path:

	http://localhost:8000/boards/list_tasks/
Request Body:

	{
		"id": <team_id>
	}
Response Format:
JSON list of task details

	[
		{
			"Board Name": board.name, 
			"Task": [
                            {
                                "Title": task.title,
                                "Status": task.status
                            }
                        ]
		}
	]

**Export Board**
Create a text file with board details named "<board_name>_<board_id>.txt". 
Id board name is "Content Service" with an id=1 it will be saved within the "out" directory as "Content_Service_1.txt".

Path:

	http://localhost:8000/boards/export/
Request Body:

	{
    	"id": <board_id>
	}
Response Format:

	{
		"filepath": <path/to/text/file/filename.txt>
	}
The filepath to the txt file is rendered as response
