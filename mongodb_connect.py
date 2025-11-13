# 1. Make sure you import this function
from urllib.parse import quote_plus
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# 2. Store your credentials in separate variables
#    This is much cleaner and safer.
raw_username = "VenkatRam"
raw_password = "Venkat@2004"  # The password with the special '@' character
cluster_address = "cluster0.ly8admn.mongodb.net"

# 3. Escape the password (and username, for good practice)
username = quote_plus(raw_username)
password = quote_plus(raw_password)

# 4. Build the final URI using an f-string with the ESCAPED credentials
#    Note: It's standard to include retryWrites and w=majority
uri = f"mongodb+srv://{username}:{password}@{cluster_address}/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)