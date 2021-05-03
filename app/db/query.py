

CREATE_QUERY_POSTS = """CREATE TABLE IF NOT EXISTS posts
                  (id integer primary key, title text, text text,
                   author text, date text);"""
CREATE_QUERY_TAGS = """CREATE TABLE IF NOT EXISTS tags
                  (id integer primary key, title text);"""
CREATE_QUERY_POSTS_TAGS = """CREATE TABLE IF NOT EXISTS posts_tags
                (id integer primary key, post_id integer, tag_id integer);
               """

TAGS_FOR_POST = """SELECT tags.id, tags.title FROM posts_tags, tags WHERE posts_tags.post_id = ? AND tags.id = posts_tags.tag_id"""
POSTS_QUERY = """SELECT *  FROM posts"""
POST_QUERY = """SELECT * FROM posts WHERE id = ?"""
INSERT_QUERY = """INSERT INTO posts (title, text, author, date)
                VALUES ('Hello', 'World 123', 'Vasya', '2002-01-02')
                """
INSERT_POST_QUERY = """INSERT INTO posts (title, text, author, date)
                VALUES (?, ?, ?, ?)
                """
INSERT_TAG_QUERY = """INSERT INTO tags (title)
                VALUES (?)
                """
INSERT_POST_TAG_QUERY = """INSERT INTO posts_tags (post_id, tag_id)
                    VALUES (?, ?)
                    """                

