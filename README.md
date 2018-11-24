# Newsdata-Project

This repository contains a Report_Tool (code) that prints out a report in plain text from the `newsdata` in the `news` database.

## Steps to get started

  **Geting the environment ready:**
  1. Clone the Newsdata-Project repository
  2. Create a Virtual Machine (VM):
      a) Download Virtualbox [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
      b) Download Vagrant [here](https://www.vagrantup.com/downloads.html)
 
  **Important Note:** If you are using ``Windows`` operating system, before you continue to step 3), make sure you enable ``Intel Virtualization Technology`` hardware extantion by opening the system's BIOS menu.
  
  3. Asumming you already have Git installed, through the git terminal cd inside the vagrant subdirectory, than run the ``vagrant up`` command to get the VM started.
  4. When you get the shell prompt back, run the ``vagrant ssh`` command to log-in the VM.
  5. Once loged to the VM, run ``cd /vagrant``.
  6. To print out the report, run ``python query.py``.
  
  ## Report Example

"""
----------------------------------------------------------------

                        Newsdata Results

 --> The Top 3 Articles of All Times

        * 'Candidate is jerk, alleges rival':  338647 views

        * 'Bears love berries, alleges bear':  253801 views

        * 'Bad things gone, say good people':  170098 views

 --> Most Popular Authors of All Times

        * Ursula La Multa:  507594 views

        * Rudolf von Treppenwitz:  423457 views

        * Anonymous Contributor:  170098 views

        * Markoff Chaney:  84557 views

 --> Days with more than 1% percent of requests with error

        * Jul, 17 2016:  2.263 % error

---------------------------------------------------------------- 
"""
       
 ## VIEWS created to run the Query Codes:
 
````sql 
CREATE VIEW **Table1** AS
SELECT title,
    name
FROM Articles JOIN Authors ON articles.author = authors.id;


CREATE VIEW **Table2** AS
SELECT status,
    to_char(time, 'FMMon, DD YYYY') "date",
    substr(path, 10) "slug"
FROM log;


CREATE VIEW **Table3** AS
SELECT title,
    name,
    status,
    date
FROM Table2 JOIN Table1 ON Table2.slug = Table1.slug;


CREATE VIEW **Table4** AS
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
 
