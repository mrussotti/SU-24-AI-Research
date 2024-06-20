import pymongo
from pymongo import MongoClient
import networkx as nx
import matplotlib.pyplot as plt

uri = "mongodb+srv://mrussotti20:YVqToG5aNIbouX31@cluster0.3d6b0da.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

#creates database + collections
db = client['financialNetwork']
users_collection = db['users']
transactions_collection = db['transactions']
relationships_collection = db['relationships']

#clears existing data to avoid duplicate entries 
users_collection.delete_many({})
transactions_collection.delete_many({})
relationships_collection.delete_many({})

#  sample users
users = [
    {"_id": 1, "name": "Alice", "email": "alice@example.com"},
    {"_id": 2, "name": "Bob", "email": "bob@example.com"},
    {"_id": 3, "name": "Charlie", "email": "charlie@example.com"},
    {"_id": 4, "name": "David", "email": "david@example.com"},
    {"_id": 5, "name": "Eve", "email": "eve@example.com"},
    {"_id": 6, "name": "Frank", "email": "frank@example.com"},
    {"_id": 7, "name": "Grace", "email": "grace@example.com"},
    {"_id": 8, "name": "Hank", "email": "hank@example.com"},
    {"_id": 9, "name": "Ivy", "email": "ivy@example.com"},
    {"_id": 10, "name": "Jack", "email": "jack@example.com"},
]

users_collection.insert_many(users)

#sample transactions
transactions = [
    {"_id": 101, "amount": 5000, "date": "2024-01-01"},
    {"_id": 102, "amount": 20000, "date": "2024-01-02"},
    {"_id": 103, "amount": 15000, "date": "2024-01-03"},
    {"_id": 104, "amount": 25000, "date": "2024-01-04"},
    {"_id": 105, "amount": 30000, "date": "2024-01-05"},
    {"_id": 106, "amount": 45000, "date": "2024-01-06"},
    {"_id": 107, "amount": 35000, "date": "2024-01-07"},
    {"_id": 108, "amount": 10000, "date": "2024-01-08"},
    {"_id": 109, "amount": 50000, "date": "2024-01-09"},
    {"_id": 110, "amount": 55000, "date": "2024-01-10"},
]

transactions_collection.insert_many(transactions)

# relationships (aka user makes a transaction)
relationships = [
    {"user_id": 1, "transaction_id": 101},
    {"user_id": 2, "transaction_id": 102},
    {"user_id": 3, "transaction_id": 103},
    {"user_id": 1, "transaction_id": 104},
    {"user_id": 4, "transaction_id": 105},
    {"user_id": 5, "transaction_id": 106},
    {"user_id": 6, "transaction_id": 107},
    {"user_id": 7, "transaction_id": 108},
    {"user_id": 8, "transaction_id": 109},
    {"user_id": 9, "transaction_id": 110},
    {"user_id": 10, "transaction_id": 101},  # a suspicious transaction, shared with another user
    {"user_id": 1, "transaction_id": 105},   # a suspicious transaction, shared with another user
    {"user_id": 2, "transaction_id": 105},   # a suspicious transaction, shared with another user
]

relationships_collection.insert_many(relationships)

#gets data from Mongo
users = list(users_collection.find())
transactions = list(transactions_collection.find())
relationships = list(relationships_collection.find())

#identify suspicious transactions (shared by multiple users)
transaction_counts = {}
for relationship in relationships:
    t_id = relationship["transaction_id"]
    if t_id in transaction_counts:
        transaction_counts[t_id] += 1
    else:
        transaction_counts[t_id] = 1

suspicious_transactions = [t_id for t_id, count in transaction_counts.items() if count > 1]

# makes  graph
G = nx.Graph()

# Adds stuff to graph
for user in users:
    G.add_node(user["_id"], label=user["name"], type='user')

for transaction in transactions:
    G.add_node(transaction["_id"], label=f"Transaction {transaction['_id']}", type='transaction')

for relationship in relationships:
    G.add_edge(relationship["user_id"], relationship["transaction_id"], relationship='made')

# draws the graph
# plt.figure(figsize=(12, 8))
# pos = nx.spring_layout(G, k=0.5)  
# labels = nx.get_node_attributes(G, 'label')
# node_colors = ['red' if node in suspicious_transactions else ('skyblue' if G.nodes[node]['type'] == 'user' else 'lightgreen') for node in G.nodes]

# nx.draw(G, pos, with_labels=True, node_size=700, node_color=node_colors, font_size=10, font_color='black')
# nx.draw_networkx_labels(G, pos, labels, font_size=12, font_color='black', verticalalignment='top')

# plt.show()

# CRUD Operations :) create, read, update, delete

#create: Add a new user and a transaction, then create a relationship
new_user = {"_id": 11, "name": "Kara", "email": "kara@example.com"}
users_collection.insert_one(new_user)
new_transaction = {"_id": 111, "amount": 60000, "date": "2024-01-11"}
transactions_collection.insert_one(new_transaction)
new_relationship = {"user_id": 11, "transaction_id": 111}
relationships_collection.insert_one(new_relationship)
print(f"Inserted new user: {new_user}")
print(f"Inserted new transaction: {new_transaction}")
print(f"Inserted new relationship: {new_relationship}")

#read: Get all users and transactions
all_users = list(users_collection.find())
all_transactions = list(transactions_collection.find())
print("All users:")
for user in all_users:
    print(user)
print("All transactions:")
for transaction in all_transactions:
    print(transaction)

# update: Change a transaction amount
transactions_collection.update_one({"_id": 102}, {"$set": {"amount": 25000}})
updated_transaction = transactions_collection.find_one({"_id": 102})
print(f"Updated transaction: {updated_transaction}")

# delete: Remove a user and their transactions
users_collection.delete_one({"_id": 3})
relationships_collection.delete_many({"user_id": 3})
print("Deleted user with _id 3")
remaining_users = list(users_collection.find())
print("Remaining users after deletion:")
for user in remaining_users:
    print(user)

#checks for any friendships involving the deleted user and remove them
relationships_collection.delete_many({"$or": [{"from": 3}, {"to": 3}]})

#gets updated data
users = list(users_collection.find())
transactions = list(transactions_collection.find())
relationships = list(relationships_collection.find())

#recreate / redraw the graph with updated data
G.clear()

#add nodes to the graph
for user in users:
    G.add_node(user["_id"], label=user["name"], type='user')
for transaction in transactions:
    G.add_node(transaction["_id"], label=f"Transaction {transaction['_id']}", type='transaction')

#adds edges to the graph
for relationship in relationships:
    G.add_edge(relationship["user_id"], relationship["transaction_id"], relationship='made')

#identify suspicious transactions (shared by multiple users)
transaction_counts = {}
for relationship in relationships:
    t_id = relationship["transaction_id"]
    if t_id in transaction_counts:
        transaction_counts[t_id] += 1
    else:
        transaction_counts[t_id] = 1

suspicious_transactions = [t_id for t_id, count in transaction_counts.items() if count > 1]

# draw the  new graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.5)
labels = nx.get_node_attributes(G, 'label')
node_colors = ['red' if node in suspicious_transactions else ('skyblue' if G.nodes[node]['type'] == 'user' else 'lightgreen') for node in G.nodes]

nx.draw(G, pos, with_labels=True, node_size=700, node_color=node_colors, font_size=10, font_color='black')
nx.draw_networkx_labels(G, pos, labels, font_size=12, font_color='black', verticalalignment='top')

plt.show()
