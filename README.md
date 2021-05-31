# Python-Django chat application
This application allow several users to talk in a chatroom and also to get stock quotes
from an API using a specific command.

### Recomendations
  - Redis >= 5
  - Python 3
  - Tested in Linux

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
- 6: Basic registred user username: admin and password: 123

## Considerations
### Completed Mandatory Features
:heavy_check_mark: Allow registered users to log in and talk with other users in a chatroom. \
:heavy_check_mark: Allow users to post messages as commands into the chatroom with the following format
/stock=stock_code \
:heavy_check_mark: Create a decoupled bot that will call an API using the stock_code as a parameter
(https://stooq.com/q/l/?s=aapl.us&f=sd2t2ohlcv&h&e=csv, here aapl.us is the
stock_code) \
:heavy_check_mark: The bot should parse the received CSV file and then it should send a message back into
the chatroom using a message broker like RabbitMQ. The message will be a stock quote
using the following format: “APPL.US quote is $93.42 per share”. The post owner will be
the bot. \
:heavy_check_mark: Have the chat messages ordered by their timestamps and show only the last 50
messages. \
:heavy_check_mark: Unit test the functionality you prefer. \

### Completed Bonus (Optional) Features
:heavy_check_mark: Have more than one chatroom. \
:heavy_check_mark: Handle messages that are not understood or any exceptions raised within the bot. \

### My Personal Bonus Features
+ Also i created a crud that is possible to register a new user in the page [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/).
+ I used websocket services to create async system !
+ A loged user can create a new chat room in the page [http://127.0.0.1:8000/room/](http://127.0.0.1:8000/room/).
+ All routes are protected and just only loged users post comments and create a new chat room.


