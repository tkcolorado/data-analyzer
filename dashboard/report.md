# messageboard
- graph
  - chart.js/d3.js
    it's better performance to create simple chart than d3.js.
  - set django-rest-framework(api) and ajax

- pandas
    At first, I coded raw queryset in django, however, considering the performance, the speed of import multiple csvs, I selected pandas to import csv and they store the db

- logging
- testcode
  - django test(unittest or pytest)
- refactoring

### import
- import sets the logging

### view
I set the table and chart. I use the pandas on chart and chart.js on chart.
However, I find out bad performance by requesting table and chart at once. so I want to change the table, create django-rest-framework, api and ajax.

### template
- table
I request the part of tbody by ajax. however, I request all the part of pagination, so I have to tune the performance of rendering pages.
