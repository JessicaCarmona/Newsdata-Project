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


# Code to execute a queries, openning and closing the connection
def query(query_code):
    """Executes PSQL Codes"""
    db = psycopg2.connect(database="news")
    c = db.cursor()
    c.execute(query_code)
    results = c.fetchall()
    db.close()
    return results


# Codes to print the report with each query results
def Heading():
    """Prints Report Heading""""
    Heading = "Newsdata Results"
    print("\n----------------------------------------------------------\n")
    print("\t\t\t" + Heading + "\n")


def Top_3_Articles():
    """Prints a list of the Top Three Articles and their total views"""
    Top_3_Articles = query(Q1)
    print("\n --> The Top 3 Articles of All Times\n")

    for title, views in Top_3_Articles:
        print("\t* {!r}:  {} views\n".format(title, views))


def Most_Popular_Authors():
    """Prints a list of the names of Popular Authors with their total views"""
    Most_Popular_Authros = query(Q2)
    print("\n --> Most Popular Authors of All Times\n")

    for name, views in Most_Popular_Authros:
        print("\t* {}:  {} views\n".format(name, views))


def Prc_Error():
    """Prints date and percent of requests with error when greater than 1%"""
    Prc_Error = query(Q3)
    print("\n --> Days with more than 1% percent of requests with error\n")

    for date, prc_error in Prc_Error:
        print("\t* {}:  {} % error\n\n".format(date, prc_error))
        print("----------------------------------------------------------\n")


if __name__ == '__main__':
    Heading()
    Top_3_Articles()
    Most_Popular_Authors()
    Prc_Error()
