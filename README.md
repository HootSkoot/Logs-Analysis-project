# Logs-Analysis-project
Creates a report analysing articles on a database

This is an internal reporting tool for use on a databse.  It will connect, run queries, and printout answers.

Only one view is created, article_views.  This table contains the article titles, authors of each of those articles, and view counts for said articles.  This table is used to answer the first two questions.  The third question does not use this table.

create view article_views as select articles.title, articles.author, count(articles.slug) as views 
    from articles join log on log.path like concat('%', articles.slug) 
    group by articles.title, articles.author 
    order by views desc;
