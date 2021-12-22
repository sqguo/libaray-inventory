## 20-books Client Instruction Manual
This user manual provides a basic understanding of the client application's capabilities.<br/>
See README.md for instructions on setting up the client application. 
<br/>
<br/>

### Homepage
After starting the application, user will arrive at the homepage. <br/>
A user will be presented with the following options:
```sh
lookup a book                  f
checkout a book                b
publish a book                 p
review a book                  r
exit                           q
```
The user may select any option by typing in their respective character key, then press enter.<br/>
If the user failed to select a valid option, the application will prompt the user to try again.<br/>
_note: At any point in time, the user may quit the application by pressing CTRL C_

<br/>

### Looking Up A Book
One of the most common use case of the client application is looking up a book in our database.

```sh
./data/my_data_files.csv
```

Install all dependencies:
```sh
pip install -r ./requirements.txt
```

Run the loading scripts using python3:
```sh
python ./load_ILS.py
python ./load_goodreads.py
python ./load_reviews.py
python ./load_inventory.py
python ./load_checkouts.py
```
_Important:_ the scripts must be run in the same order as specified above. <br/>
_This takes about 60 minutes to run on an unloaded server.<br/>
Do not wait till the marking deadline to create your version of the dataset._
<br/>
<br/>

### Running the Client APP
Start the application using python3:
```sh
python ./application.py
```
Read the instructions located at:
```sh
./MANUAL.md
```

### Data Mining