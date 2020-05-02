import os
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import sqlite3
from multiprocessing import pool
from nltk.corpus import stopwords
from string import punctuation


def execute_commands(cmds):
    local_list = []
    # generating unworthy words
    unworthy_words = {x: '' for x in set(stopwords.words('english'))}
    unworthy_words.update({x: '' for x in punctuation})
    for item in cmds:
        pid = item[0]
        title = item[1]
        final_tags = []
        first_list = list(nltk.word_tokenize(title))
        for word in first_list:
            try:
                test = unworthy_words[word.lower()]
            except KeyError:
                final_tags.append(word)
        final_tags = ','.join(final_tags)
        local_list.append((pid, title, final_tags))
    return local_list


def func():

    filepath = os.path.join('../src/Data/Movie.db')
    print(filepath)
    conn = sqlite3.connect(filepath)
    # create cursor to browese db
    c = conn.cursor()
    # query db
    c.execute("SELECT id, title FROM Movie;")
    # function to chunk the entire data
    def chunks(l, n):
        lst = []
        for i in range(0, len(l), n):
            lst.append(l[i: i + n])
        return lst
    # generating the entire data
    commands = c.fetchall()
    print('Fetching data completed!')
    print(len(commands))
    # creating the Pool. Vary the number based on your cores
    p = pool.Pool(2)
    # chunking the commands into segments to use parallel processing
    cmd_chunks = chunks(commands, 250)
    # starting the processes
    total = p.map(execute_commands, cmd_chunks)
    total = [each for sublist in total for each in sublist]
    p.terminate()
    print("Generating queries completed!")
    params = []
    for checkpoint in range(len(total)):
        pid, title, tags = total[checkpoint]
        params.append((tags, pid))
        if ((checkpoint + 1) % 7500 == 0 or (checkpoint + 1) == len(total)):
            print("Starting update: {} done".format(checkpoint + 1))
            q = """Update Movie set tag_list = ? where id = ?"""
            c.executemany(q, params)
            conn.commit()
            params = []
            print("{} entries updated!".format(checkpoint + 1))
    c.close()


if __name__ == "__main__":
    func()