import os
os.system("pip install -U scratchattach")
os.system("pip install Pillow")

import scratchattach as scratch3

from PIL import Image
import requests
from io import BytesIO

session = scratch3.login("just_devs", os.getenv("JD_PASS"))
conn = session.connect_cloud("982808852") 

servv = "2.0"

client = scratch3.CloudRequests(conn)

def rgb_to_hex(rgb):
    r, g, b = rgb
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    
    hex_color = "{:02X}{:02X}{:02X}".format(r, g, b)
    
    return hex_color

def generatePfp(usertopfp,resolution):
    print(f"Generating pfp for user {usertopfp} with resolution {resolution}")
    userVar = scratch3.get_user(usertopfp)
    userVar.update()
    req = requests.get(userVar.icon_url).content
    req = BytesIO(req)
    Img = Image.open(req)
    Img = Img.rotate(90)
    Img = Img.convert("RGB")
    Img = Img.resize((int(resolution),int(resolution)))
    pixelList = []
    for pixelX in range(Img.width):
        for pixelY in range(Img.height):
            pixel = Img.getpixel((pixelX, pixelY))
            pixel = rgb_to_hex(pixel)
            pixelList.append(pixel)
    return pixelList

@client.request
def ping(): 
    print("Ping request received")
    return_data = []
    return_data.append("true")
    return_data.append(servv)
    return return_data

@client.request
def getinfo(argument1):
    print(f"Data requested for user {argument1}")
    user = scratch3.get_user(argument1)
    user.update()

    return_data = []
    return_data.append(f"Followers: {user.follower_count()}")
    return_data.append(f"About Me:\n{user.about_me}")
    return_data.append(f"Projects: {user.project_count()}")
    return_data.append(f"What Am I Working on:\n{user.wiwo}")
    return_data.append(user.message_count())

    return return_data

@client.request
def getpfp(argument1, argument2):
    print(f"PFP requested for user {argument1} and resolution {argument2}")
    
    return generatePfp(argument1, argument2)


@client.event
def on_ready():
    print("Request handler is running")

client.run()
