# OLD LEAGUE PROJECT
This was an old project to help players on the game league of legends, [VIDEO EXAMPLE](https://www.youtube.com/watch?v=NKT2Pmt82Hg
).
It used real time comunication and the Google Speech API.

## HOW TO REPLICATE
### 0 Your api key
---
You have to set the variable API_KEY from disrupt_flash/setting.py to yout key !

### 1 Installing things
---
##### 1.1 Create a virtualenv and install requirements 
```
if ( you dont have pip and virtualenv installed ) {
	https://pip.pypa.io/en/stable/installing/
	$ [sudo] pip install virtualenv
}
// Create virtualenv
$ cd disrupt_flash_project
$ virtualenv ../disrupt_env
$ source ../disrupt_env/bin/activate
$ pip install -r requirements.txt	

```


##### 1.2 Django stuff
$ cd disrupt_flash

Database:
$ ./manage.py migrate

Geting champions and summoner spells to database:
$ ./manage.py get_champions
$ ./manage.py get_spells

And Regions:
$ ./manage.py create_regions


```
if ( you want to acces the admin panel ) {
	$ ./manage.py createsuperuser
	http://127.0.0.1:8000/admin
}
```


##### 1.3 NODE STUFF

```
if ( you dont have node installed ){
	https://nodejs.org/en/download/package-manager/
}
```

Install packages whitin the root directory (disrupt_flash_project):
$ npm install


### 2 RUNING THE SERVERS
---

##### 2.1 RUNING DJANGO SERVER

 !! B4 anything go to the static/img/ folder and:
 $ mkdir qr

$ ./manage.py runserver
( only you can access )

or

$ ./manage.py runserver 0.0.0.0:8000
( so other computers on network can access via "yourip":8000 )
( you will have to change the url in templates/room.html {% if '8000' in request.META.HTTP_HOST %} <script src=...> from 127.0.0.1 to your private ip )


##### 2.2 RUNING THE NODE SERVER

$ node socket_server/index.js


### 3 CRON TO DELETE ROOMS
---
Create a cron every hour for the next commnad
$ ./manage.py delete_rooms  ( must be with the virtualenv and disrupt_flash/ folder )


### 4 RUN WITH HTTPS
---
If you want to upload everything to a domain name you need https or the voice recognition will ask the user for permision every 2 minutes or so.

Django will work fine with nginx configured the right way, but the socket_server/index.js will need the following code:
```
var fs = require('fs');
var options = {
   key  : fs.readFileSync('privkey.pem'),
   cert : fs.readFileSync('cert.pem')
};
// replace http with https in the require('http')
var http = require('https').Server(options, app);
```
Also you need to modify the http to https in the files in disrupt_flash/templates/room.html

# EXTRAS:
---
- RUN IN CHROME !

- IF YOU ARE NOT USING LOCALHOST, YOU NEED HTTPS OR THE BROWSER WILL ASK FOR PERMISION
ALL THE TIME FOR THE VOICE RECOGNITION. AND YOU WILL NEED TO CHANGE all from http to https including
the node js server at :3000

- IM USING https://github.com/foreverjs/forever TO RUN EVERYTHING ON SERVER

- YOU MAY NEED TO MODYFY THE DB FILE AND STATIC FOLDER OWNER AND PERMISIONS,
THE APP HAS TO HAE ACCESS TO ( db.sqlite[or your db], all the files on static/, the files in disrupt_flash/ )

- ADJUNST MIC VOLUME LVL, IT CAN HELP IF IT DOESNT DETECT YOUR BREATH
OR OTHER THINGS, BUT IS SOMEHOW ACCURATE

- IF YOU USE IT ON A MOVILE PHONE IT WILL WORK, BUT IF YOU LOCK THE SCREEN THE JS STOPS
WORKING AND SO DOES THE APP, BUT YOU CAN USE IT ON A WEB BROSER (on pc or laptop) AND MINIMIZE
THE SCREEN

- NOT CONFIGURED FOR URF, HEXAKILL, OR OTHER GAMEMODES THAN 5v5, 3v3 ( for now )

- DONT TRY TO RUN WHEN PLAYING AGAINST BOTS, IF YOU
NEED REAL GAMES WATCH HERE:
http://www.lolnexus.com/recent-games?filter-region=2&filter-sort=2

- INSTALL SASS ( if you want to edit the css )
http://sass-lang.com/install
$ sh allsass.sh


