import os
import sqlite3
import json

def main():
    filepath = os.path.join(os.getcwd(),'src', 'Data', 'Movie.db')
    print(filepath)
    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    c.execute("SELECT id, title, year, tag_list, year FROM Movie;")
    data = c.fetchall()

    index = {}

    for entry in data:
        # print(f' Id: {entry[0]} \n Movie: {entry[1]} \n Tags: {entry[2]} \n')
        year = entry[2]
        tag_list = entry[3].split(',')
        movie_id = entry[0]
        for tag in tag_list:
            
            leaf_list = []
            try:
                sub_dict = index[str(tag.lower())]
            except KeyError:
                sub_dict = {}

            leaf_list.append(movie_id)
            
            if year in sub_dict:
                leaf_list.extend(sub_dict[year]) 
            else:
                pass

            sub_dict[year] = leaf_list
            
            index[str(tag.lower())] = sub_dict
    # print(index)
    with open(os.path.join(os.getcwd(),'src', 'Data', 'index.json'),'w+') as fp:
        fp.write(json.dumps(index))

if __name__ == "__main__":
    main()
