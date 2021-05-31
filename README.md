# Python-Django chat application
This application allow several users to talk in a chatroom and also to get stock quotes
from an API using a specific command.

### Recomendations
  - Redis >= 5
  - Python 3
  - System has been tested for linux 

### Installation and Deploy using Docker
- 1: Check if redis is running, case is running stop your current redis server using the command below, just to avoid conflicts:
		
		sudo /etc/init.d/redis-server stop
- 2: Using the terminal enter in repository chat folder and run the command to build docker:
		
		sudo docker-compose build
- 3: Using the terminal enter in repository chat folder and run the command to start server:
		
		sudo docker-compose up -d 
- 4: Check docker containers starts successfully:
	   	
		sudo docker ps
- 5: Then check the web app in [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
