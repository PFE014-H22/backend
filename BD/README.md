# Database
## Add new technology from StackOverflow
### Step 1: Download dump from DataExplorer
To add new technologies to the app you must first download a data dump relating to this technology from the StackExchange DataExplorer. Go to [Compose new query](https://data.stackexchange.com/stackoverflow/query/new) and run this mySQL query:
```sql
select p.Id, p.AcceptedAnswerId, p.CreationDate, p.Title, p.Body, p.Tags, a.Body as 'Answer Body'
from Posts as p join Posts as a on p.AcceptedAnswerId = a.Id
where p.Tags like '%<your technology>%' and p.AcceptedAnswerId is not null
order by CreationDate asc
```
Here we select all questions with an accpted answer and with your desired technology as the tag.

You can then download the csv.

The order is ascending so that we only have to add at the end when we update the file.

### Step 2: Generate parameters text file
Use the [fetch_cassandra_parameters](/src/config_parameters/cassandra/fetch_cassandra_parameters.py) script to create a new script that will fetch and generate a text file that will contain all the config parameters from your desired techology. 

### Step 3: Filter your CSV file
Use the [filter_dump](/src/SO/filter_dump.py) script to filter the CSV downloaded from Step 1 with text file generated from Step 2. This will remove all questions for which the answer doesn't include a config parameter. It will also add a new column with the found parameter for each question.

### Step 4: Update your CSV file
Use the [update_dump](/src/SO/update_dump.py) script to update your DB. You'll also want to setup a flask scheduler in [main](/main.py) to automate the update. You should only need to change to file names in order to setup your new technology.

## Add new Data source
This is in case you already have data for a certain technology from StackOverflow and you want to add more from another source. For example, Jira or Github.
### Step 1: Extract the necessary info
Extract the necessary information from the new data source and add it as new rows to the existing CSV. 

Add the new data source to the [datasource](/datasource/datasource.py) file.

### Step 2: Create an update script
Create a script to update from this new data source. Once that's done, use the flask scheduler in [main.py](../main.py) to run the update.

### Step 3: Train the model
Train the model with the new data.