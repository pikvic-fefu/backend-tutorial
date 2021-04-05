class Post:
    def __init__(self, id, title, author, date, text, tags):
        self.title = title
        self.author = author
        self.date = date
        self.text = text
        self.tags = tags
        self.id = id

    def save_post(self, file):
        with open(file, 'wt', encoding='utf-8') as f:
            f.write(self.id)
            f.write(self.title)
            f.write(self.author)
            f.write(self.date)
            f.write(self.text)
            f.write(self.tags)
    
    def __str__(self):
        return f"{self.title} : {self.tags}"

    def __repr__(self):
        return f"{self.title} : {self.tags}"

def read_posts_from_file(file):
    posts = []
    with open(file, 'rt', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
        n = len(lines) // 6
        for i in range(n):
            id, title, author, date, text, tags = lines[i*6:(i+1)*6]
            tags = [tag.strip() for tag in tags.split(',')]
            post = Post(int(id), title, author, date, text, tags)
            posts.append(post)
    return posts