import psycopg2


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
cursor.execute("create view article_views as select articles.title, \
               articles.author, count(articles.slug) as views\
               from articles join log on log.path \
               like concat('%', articles.slug) \
               group by articles.title, articles.author \
               order by views desc;")
cursor.execute('select title, views from article_views limit 3;')
print "The top 3 most viewed articles:\n"
printRows(cursor.fetchall(), "views")
cursor.execute('select authors.name, sum(article_views.views) as views \
               from article_views \
               join authors on article_views.author = authors.id \
               group by authors.name \
               order by views desc')
print "\nHere are the authors ranked in terms of greatest number of viewers:"
printRows(cursor.fetchall(), "views")
cursor.execute("select time::date as date, \
               round( count ( case when status like '%404%' then 1 end ) \
               * 100::numeric / count(*) , 2 ) as percent_fail \
               from log \
               group by date \
               having (count(case when status like '%404%' then 1 end) \
               * 100)::numeric / count(*) > 1.0;")
print "\nThese are the dates where >1% of users could not load an article:"
printRows(cursor.fetchall(), "precentage failure")
db.close()
