#!/usr/bin/env python3

import psycopg2


# PSQL Queries (Q):
"""
    * Q1: Returns Top 3 articles
    * Q2: Returns Most popular authors
    * Q3: Returns Days with more than 1% of requests with errors
"""

Q1 = """SELECT title,
            count(*) AS views
        FROM Table3
        WHERE status = '200 OK'
        GROUP BY title
        ORDER BY views
        DESC LIMIT 3;"""

Q2 = """SELECT name,
            count(*) AS views
        FROM Table3
        WHERE status = '200 OK'
        GROUP BY name
        ORDER BY views DESC;"""

Q3 = """WITH percent AS (
            SELECT date,
                ROUND((SUM(errors)/SUM(total))*100.0,3) AS prc_error
            FROM Table4
            GROUP BY date)
       SELECT date, prc_error FROM percent WHERE prc_error>1;"""


# Code to xecute a queries, openning and closing the connection
def query(query_code):
    db = psycopg2.connect(database="news")
    c = db.cursor()
    c.execute(query_code)
    results = c.fetchall()
    db.close()
    return results


# Codes to print the report with each query results
def Heading():
    Heading = "Newsdata Results"
    print("\n----------------------------------------------------------------\n")    
    print("\t\t\t" + Heading + "\n")


def Top_3_Articles():
    Top_3_Articles = query(Q1)
    print("\n --> The Top 3 Articles of All Times\n")

    for title, views in Top_3_Articles:
        print("\t* {!r}:  {} views\n".format(title, views))


def Most_Popular_Authors():
    Most_Popular_Authros = query(Q2)
    print("\n --> Most Popular Authors of All Times\n")

    for name, views in Most_Popular_Authros:
        print("\t* {}:  {} views\n".format(name, views))


def Prc_Error():
    Prc_Error = query(Q3)
    print("\n --> Days with more than 1% percent of requests with error\n")

    for date, prc_error in Prc_Error:
        print("\t* {}:  {} % error\n\n".format(date, prc_error))
        print("----------------------------------------------------------------\n")


if __name__ == '__main__':
    Heading()
    Top_3_Articles()
    Most_Popular_Authors()
    Prc_Error()


# VIEW TABLES:

"""
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
"""
