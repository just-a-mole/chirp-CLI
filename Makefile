all: start

start:
	python3 app.py

reset: 
	sqlite3 app.db < nuke.txt
	sqlite3 app.db < create.txt
	python3 app.py < populate.txt

populate:
	python3 app.py < populate.txt

nuke:
	sqlite3 app.db < nuke.txt

create:
	sqlite3 app.db < create.txt

posts:
	python3 app.py < createPosts.txt

test:
	sqlite3 app.db < test.txt
