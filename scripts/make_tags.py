import sqlite3
from string import punctuation
from nltk.corpus import stopwords

# connect to db
conn = sqlite3.connect('../src/Data/Movie.db')

# create cursor to browese db
c = conn.cursor()

# query db

c.execute("SELECT title FROM Movie")

# defining stopwords
unworthy_words = set(stopwords.words('english'))

# how many results to return
data = list(c.fetchmany(10))

for item in data:
    final_tags = []

    title = item[0]
    # tagline = item[1]

    first_list = [i for i in item[0].strip(punctuation).split(' ')]

    # second_list = [j for j in item[1].strip(punctuation).split(' ')]

    # extracted_words = list(set(first_list) | set(second_list))

    extracted_words = list(first_list)

    for word in extracted_words:
        if word not in unworthy_words:
            final_tags.append(word)
    final_tags = str(final_tags)

    print(f'\n Name: {item[0]} \n  Tags: {final_tags} \n')

    c.execute("""UPDATE Movie SET tag_list = :tag_list WHERE title = :title""",
                {'title': str(title), 'tag_list': final_tags})

# commit the transaction
conn.commit()

# close the db
conn.close()
