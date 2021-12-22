## 20-books
Group 57<br/>
members: sqguo
<br/>
<br/>

### Loading Data
Download all CSV files to the following path:
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
Open PowerShell and install all dependencies:<br/>
```sh
pip install -r ./requirements.txt
```
Start the application using python3:
```sh
python ./application.py
```
Read the instructions located at:
```sh
./MANUAL.md
```

### Data Mining