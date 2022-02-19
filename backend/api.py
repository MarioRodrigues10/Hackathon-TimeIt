import random
import json

from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Instantiate FastAPI
app = FastAPI()

# Whitelist
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.post('/api/v1/')
async def root(req: Request) -> list:
    data = await req.json()

    schedule = data['schedule']
    interests = data['interests']
    tags = interests['tags']

    to_remove = []
    colided = check_colide(schedule) # Returns a list of tuples containing events happening at the same time

    for event in colided:
        h1 = schedule[event[0]]
        h1_sum = 0
        h1_tags = 0

        h2 = schedule[event[1]]
        h2_sum = 0
        h2_tags = 0

        for tag in h1.get('tags', []):
            h1_tags += 1
            h1_sum += int(tags[tag])
            
        for tag in h2.get('tags', []):
            h2_tags += 1
            h2_sum += int(tags[tag])

        if h1_tags != 0:
            h1_sum = h1_sum / h1_tags
        
        if h2_tags != 0:
            h2_sum = h2_sum / h2_tags
        
        h1_len = len(h1.get('tags', []))
        h2_len = len(h2.get('tags', []))
        
        if (h1_sum > h2_sum) and (h2_len > 0):
            to_remove.append(h2)

        elif (h1_sum < h2_sum) and (h1_len > 0):
            to_remove.append(h1)
        
        elif (h1_sum == h2_sum) and (h1_len > 0) and (h2_len > 0):
            # Chooses a random schedule and remove it
            if (random.randint(0,1)) == 0:
                to_remove.append(h1)
            else:
                to_remove.append(h2)

    for elem in to_remove:
        if elem in schedule:
            schedule.remove(elem)

    return schedule
        
# Checks for coliding events inside the main schedule
def check_colide(schedule: list) -> list:
    colided = []
    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            if (check_colide_aux(schedule[i], schedule[j])):
                colided.append((i,j))
    return colided

def check_colide_aux(h1, h2) -> bool:
    start1 = h1['date_start']
    end1 = h1['date_end']
    start2 = h2['date_start']
    end2 = h2['date_end']

    if start1 == start2 and end1 == end2:
        return True
    
    if start1 < start2 and end1 > start2:
        return True

    if start1 > start2 and end1 < end2:
        return True 
    
    if start1 < start2 and end1 > start2:
        return True
    
    if start1 > start2 and end1 < end2:
        return True

    return False
