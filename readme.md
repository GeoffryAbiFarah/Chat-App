### To run the application:
* Clone the repository using:
    git clone https://github.com/GeoffryAbiFarah/Chat-App.git

* Install the dependancies using the following commands:
    - on windows: pip install -r requirements.txt
    - on linux: pip3 install -r requirements.txt

* Create a MongoDB Cluster & Database

* Create a ".env" file and add to it the Cluster connection string, your ".env" file should look like this:

    DB_URL=[YOUR CONNECTION STRING]
    SECRET_KEY=[YOUR SECRET KEY FOR FLASK LOGIN]

* Run the app using the following command:
    - on windows: python app.py
    - on linux: python3 app.py

