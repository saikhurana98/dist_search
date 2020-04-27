import nltk
nltk.download('stopwords')

import sqlite3
from multiprocessing import pool
from nltk.corpus import stopwords
from string import punctuation


def execute_commands(cmds):

    local_list = []
    # generating unworthy words
    unworthy_words = {x: '' for x in set(stopwords.words('english'))}
    for item in cmds:
        final_tags = []
        title = item[1]
        first_list = [i for i in title.strip(punctuation).split(' ')]
        extracted_words = list(first_list)
        for word in extracted_words:
            try:
                test = unworthy_words[word]
            except KeyError:
                final_tags.append(word)
        final_tags = ','.join(final_tags)
        # print('\n\tName: {}\n\tTags: {}\n'.format(item[0], final_tags))

        local_list.append((item[0],title, final_tags))
    return local_list


def func():

    conn = sqlite3.connect('../src/Data/Movie.db')

    # create cursor to browese db
    c = conn.cursor()

    # query db
    c.execute("SELECT id,title FROM Movie;")

    # function to chunk the entire data
    def chunks(l, n):
        lst = []
        for i in range(0, len(l), n):
            lst.append(l[i: i + n])
        return lst

    # generating the entire data
    commands = c.fetchall()

    # print(commands)
    print('Data Fetch Complete!')
    print(len(commands))

    # creating the Pool. Vary the number based on your cores
    p = pool.Pool(16)
    # chunking the commands into segments to use parallel processing
    cmd_chunks = chunks(commands, 250)
    # starting the processes
    total = p.map(execute_commands, cmd_chunks)
    total = [each for sublist in total for each in sublist]
    p.terminate()
    
    # print(total)

    for each in total:
        pid, title, final_tags = each
        # print(f'\n Title: {title} \n Tags: {final_tags} \n')

        sql_update_query = '''Update Movie set tag_list = "{}" where id = {};'''.format(final_tags, pid)
        # print(sql_update_query)
        c.execute(sql_update_query)

        # c.execute("""UPDATE Movie SET tag_list = :tag_list WHERE title = :title;""",
        #           {'title': str(title), 'tag_list': final_tags})
    conn.commit()
    c.close()

if __name__ == "__main__":
    func()

