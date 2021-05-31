# Browser-Based chat application using Python with Django
This application allow several users to talk in a chatroom and also to get stock quotes
from an API using a specific command.

### Recomendations
  - Redis >= 5
  - Python 3

### Installation and Deploy using Docker
- 1: Check if redis is running, case is running stop your current redis server using the command (just to avoid conflicts):
		sudo /etc/init.d/redis-server stop
- 2: Using the terminal enter in repository chat folder and run the command:
		sudo docker-compose -build up -d 
- 3: Check docker containers starts successfully:
	    sudo docker ps
- 4: Then check the web app in [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
