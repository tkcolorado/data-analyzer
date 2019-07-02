# data-analyzer
Data visualization of consumption rate for tariff, area and user_id etc.

## Description
Import csv files by django custom command, and then, I visualize the data by table and chart by categories.

## Requirement
- chartjs==1.2
- Django==2.2.2
- numpy==1.16.4
- pandas==0.24.2
- python-dateutil==2.8.0
- pytz==2019.1
- six==1.12.0
- sqlparse==0.3.0

## Usage
`git clone git@github.com:takahirosawamura/data-analyzer.git`  

1. `cd data-analyzer`  

2. `python -m venv django`  

3. Deactivate your VM if you are running  

4. activate venv(`source django/bin/activate`)  

5. `pip install -r requirements.txt`  

6. `python path/to/manage.py migrate`  

7. data import: import csv files to DB: `python path/to/manage.py import`  

8. data-dashboard :`python path/to/manage.py runserver`  

## reference
- custom command
https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/

you can check the data analyzation, summary page and detail page.  

### summary page:   
you can check the db, tables and chart.  
![Summary](https://user-images.githubusercontent.com/18510885/60484357-49670980-9cd4-11e9-9043-3469a51cc9c0.png)

### details page:   
you can chack the db more than summary page. id, date, tariff, consumption etc.
![Detail](https://user-images.githubusercontent.com/18510885/60484356-49670980-9cd4-11e9-8cdd-e246d1a25581.png)

## Todo
Now, this app's performance is not good, so I want to tune performance, efficient query, code splitting etc.

## Author
[tkcolorado](https://github.com/tkcolorado)
