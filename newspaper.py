import psycopg2
#!/usr/bin/env python


def printRows(list, viewType):
    """this function takes in the table and the data point for comparision, and
    prints out each row"""
    i = 1
    for row in list:
        print "%s: %s    %s: %s" % (i, row[0], viewType, row[1])
        i += 1
    return


db = psycopg2.connect(database='news')
cursor = db.cursor()
"""this view creates a table with the article titles, authors,
and view counts used for the next two steps"""
cursor.execute("CREATE OR REPLACE VIEW article_views AS SELECT articles.title, \
               articles.author, COUNT(articles.slug) AS views\
               FROM articles JOIN log ON log.path \
               LIKE CONCAT('%', articles.slug) \
               GROUP BY articles.title, articles.author \
               ORDER BY views DESC;")
cursor.execute('SELECT title, views FROM article_views LIMIT 3;')
print "The top 3 most viewed articles:\n"
printRows(cursor.fetchall(), "views")
cursor.execute('SELECT authors.name, SUM(article_views.views) AS views \
               FROM article_views \
               JOIN authors ON article_views.author = authors.id \
               GROUP BY authors.name \
               ORDER BY views DESC')
print "\nHere are the authors ranked in terms of greatest number of viewers:"
printRows(cursor.fetchall(), "views")
cursor.execute("SELECT time::date AS date, \
               ROUND( COUNT ( CASE WHEN status LIKE '%404%' THEN 1 END ) \
               * 100::numeric / COUNT(*) , 2 ) AS percent_fail \
               FROM log \
               GROUP BY date \
               HAVING (COUNT(CASE WHEN status LIKE '%404%' THEN 1 END) \
               * 100)::numeric / COUNT(*) > 1.0;")
print "\nThese are the dates where >1% of users could not load an article:"
printRows(cursor.fetchall(), "precentage failure")
db.close()
