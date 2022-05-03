from pymongo import MongoClient
import os
import logging

"""
Environment Variables
"""
TOKEN = os.getenv("TOKEN")
RANDOMMER_API = os.getenv("RANDOMMER_API")
MONGODB = os.getenv("MONGODB")

"""
Logging setup.
"""
logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='nextcord.log', encoding='utf-8', mode='w'
)

handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
)
logger.addHandler(handler)



"""
MongoDB 
"""
Client = MongoClient(MONGODB)

def warn_count(idict: dict, id: int):
    try:
        count = 0
        print(idict)
        for i in idict[id]:
            count += 1
        return(count)
    except KeyError:
        return(0)


def main():
    pass

if __name__ == "__main__":
    main()