# Newsdata-Project

This repository contains a Report_Tool (code) that prints out a report in plain text from the data (`newsdata`) in the `news` database.

## Steps to get started

  **Geting the environment ready:**
  1. Clone the Newsdata-Project repository and unzip the *News-Project* folder.
  2. Create a Virtual Machine (VM):
      a) Download Virtualbox [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
      b) Download Vagrant [here](https://www.vagrantup.com/downloads.html)
 
  **Important Note:** If you are using ``Windows`` operating system, before you continue to step 3), make sure you enable ``Intel Virtualization Technology`` hardware extantion by opening the system's BIOS menu.
  
  3. Asumming you already have Git installed, through the git terminal, get inside the News-Project directory and cd inside the vagrant subdirectory, than run the ``vagrant up`` command to get the VM started.
  4. When you get the shell prompt back, run the ``vagrant ssh`` command to log-in the VM.
  5. Once loged to the VM, run ``cd /vagrant``.
  6. To print out the report, run ``python query.py``.
         
 ## VIEWS created to run the Query Codes:
 
````sql 
CREATE VIEW Table1 AS
SELECT title,
    name
FROM Articles JOIN Authors ON articles.author = authors.id;


CREATE VIEW Table2 AS
SELECT status,
    to_char(time, 'FMMon, DD YYYY') "date",
    substr(path, 10) "slug"
FROM log;


CREATE VIEW Table3 AS
SELECT title,
    name,
    status,
    date
FROM Table2 JOIN Table1 ON Table2.slug = Table1.slug;


CREATE VIEW Table4 AS
WITH total_status AS (
        SELECT date,
            count(*) AS total
            FROM Table2
            GROUP BY date),
    error_status AS (
        SELECT date,
            count(*) AS errors
        FROM Table2
        WHERE status !='200 OK'
        GROUP BY date)
SELECT total_status.date,
    total,
    errors
FROM total_status JOIN error_status ON total_status.date = error_status.date
ORDER BY date;
 
