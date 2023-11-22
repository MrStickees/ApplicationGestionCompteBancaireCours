import json
import os
import bcrypt
import uuid

class Data:
    SEL_FILE = "key.txt"

    def __init__(self, name, key="test"):
        self.name = name
        self.key = key
        self.data = {}

    @staticmethod
    def get_fixed_salt():
        if not os.path.exists(Data.SEL_FILE):
            fixed_salt = bcrypt.gensalt()
            with open(Data.SEL_FILE, 'wb') as f:
                f.write(fixed_salt)
        else:
            with open(Data.SEL_FILE, 'rb') as f:
                fixed_salt = f.read()
        return fixed_salt

    def loadData(self):
        if not self.name in os.listdir():
            self.saveData()
            return
        with open(self.name, 'r') as f:
            self.data = json.load(f)

    def saveData(self):
        with open(self.name, 'w') as f:
            json.dump(self.data, f, indent=4)

    def addUser(self, username, password):
        password = self.hashPassword(password)
        id = str(uuid.uuid4())
        self.data[id] = {
            "username": username,
            "password": password,
            "solde": 20,
            "history": []
        }
        self.saveData()

    def removeUser(self, id):
        del self.data[id]
        self.saveData()

    def hashPassword(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), Data.get_fixed_salt()).decode('utf-8')


if __name__ == "__main__":
    data = Data("data.json")
    data.loadData()
    data.addUser("test", "test")