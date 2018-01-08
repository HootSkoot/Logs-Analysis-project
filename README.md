# Logs-Analysis-project
Creates a report analysing articles on a database.

To use this tool with the specific database you'll need a virtual machine and vagrant installed.  Newsdata.sql, the database file, needs to be in the vagrant folder alongside the newspaper.py file.  

This is an internal reporting tool for use on a databse.  It will connect, run queries, and printout answers automatically.  The user only needs to be logged into  vagrant and run the tool with the command "python newspaper.py"

The first question answered is the total views per article in descending order, the authors with the most views in descending order, and the days on which more than 1% of users had errors accessing articles.

Only one view is created, article_views.  This table contains the article titles, authors of each of those articles, and view counts for said articles.  This table is used to answer the first two questions.  The third question does not use this table.

create view article_views as select articles.title, articles.author, count(articles.slug) as views 
    from articles join log on log.path like concat('%', articles.slug) 
    group by articles.title, articles.author 
    order by views desc;
