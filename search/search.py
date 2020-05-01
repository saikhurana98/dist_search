import sqlite3
import json

with open ('../src/Data/index.json') as f:
    index = json.load(f)

def main():
    filepath = os.path.join('../src/Data/Movie.db')
    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    c.execute("SELECT id FROM Movie;")
    data = c.fetchall()

def lookup_tags(output):
    output = output.split()
    # year = []
    if output == -1:
        print("Error, no input")

    else:
        for i in range (len(output)):
            # for j in range (2020):
                # print(output[i])
                print (index[output[i]])  
            
        return



output = input("Enter: ")
lookup_tags(output)
