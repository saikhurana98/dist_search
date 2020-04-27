import sqlite3
from multiprocessing import pool
from nltk.corpus import stopwords
from string import punctuation



def execute_commands(cmds):
    # global
    local_list = []

    conn = sqlite3.connect('../src/Data/Movie.db')
    # create cursor to browese db
    c = conn.cursor()
    # generating unworthy words
    unworthy_words = {x: '' for x in set(stopwords.words('english'))}
    for item in cmds:
        final_tags = []
        title = item[0]
        first_list = [i for i in item[0].strip(punctuation).split(' ')]
        extracted_words = list(first_list)
        for word in extracted_words:
            try:
                test = unworthy_words[word]
            except KeyError:
                final_tags.append(word)
        final_tags = str(final_tags)
        # print('\n\tName: {}\n\tTags: {}\n'.format(item[0], final_tags))

        local_list.append((title, final_tags))
        return local_list


def func():

    global global_list

    conn = sqlite3.connect('../src/Data/Movie.db')

    # create cursor to browese db
    c = conn.cursor()

    # query db
    c.execute("SELECT title FROM Movie")

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
        title, final_tags = each
        print(f'\n Title: {title} \n Tags: {final_tags} \n')

        c.execute("""UPDATE Movie SET tag_list = :tag_list WHERE title = :title;""",
                  {'title': str(title), 'tag_list': final_tags})
    conn.commit()
    c.close()

if __name__ == "__main__":
    global_list = []
    func()

