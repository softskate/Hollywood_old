import sqlite3
con=sqlite3.connect('db.sqlite')
curs=con.cursor()

con2=sqlite3.connect('db.sqlite3')
curs2=con2.cursor()

curs.execute("SELECT * FROM actors")
mlog=curs.fetchall()
for i in mlog:
    curs2.execute("INSERT INTO hollywood_actor (actor_id,name) VALUES (?,?)", (i[0],i[1]))
    con2.commit()
    print(i[0])
    
curs.execute("SELECT * FROM writers")
mlog=curs.fetchall()
for i in mlog:
    curs2.execute("INSERT INTO hollywood_writer (writer_id,name) VALUES (?,?)", (i[0],i[1]))
    con2.commit()
    print(i[0])

mid=1
curs.execute("SELECT * FROM movies")
mlog=curs.fetchall()
for i in mlog:
    writers_names=''
    writer=''
    if i[3]:
        curs.execute("SELECT name FROM writers WHERE id=?",(i[3],))
        writer=curs.fetchone()[0]
        curs2.execute("SELECT id FROM hollywood_writer WHERE writer_id=?",(i[3],))
        wid=curs2.fetchone()[0]
        curs2.execute("INSERT OR IGNORE INTO hollywood_movie_writers (movie_id,writer_id) VALUES (?,?)", (mid,wid))
        con2.commit()
    else:
        for x in eval(i[8]):
            print(x)
            curs2.execute("SELECT id FROM hollywood_writer WHERE writer_id=?",(x['id'],))
            wid=curs2.fetchone()[0]
            curs2.execute("INSERT OR IGNORE INTO hollywood_movie_writers (movie_id,writer_id) VALUES (?,?)", (mid,wid))
            con2.commit()
            curs.execute("SELECT name FROM writers WHERE id=?",(x['id'],))
            writers_name=curs.fetchone()[0]
            if writers_names:
                writers_names=writers_names+', '+writers_name
            else:
                writers_names=writers_name
                
    actors_names=''
    curs.execute("SELECT actor_id FROM movie_actors WHERE movie_id=?",(i[0],))
    actors_ids=curs.fetchall()
    for x in actors_ids:
        curs2.execute("INSERT OR IGNORE INTO hollywood_movie_actors (movie_id,actor_id) VALUES (?,?)", (mid,x[0]))
        con2.commit()
        curs.execute("SELECT name FROM actors WHERE id=?",(x[0],))
        actors_name=curs.fetchone()[0]
        if actors_names:
            actors_names=actors_names+', '+actors_name
        else:
            actors_names=actors_name
                
    curs2.execute("INSERT INTO hollywood_movie (movie_id,title,imdb_rating,genre,description,writers_names,director,actors_names,writer) VALUES (?,?,?,?,?,?,?,?,?)", (i[0],i[4],i[7],i[1],i[5],writers_names,i[2],actors_names,writer))
    con2.commit()
    mid+=1
    print(i[0])
