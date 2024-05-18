# Project.py

class Project:
    def __init__(self, ID, Title):
        self.ID = ID
        self.Title = Title
        self.members = []
        self.tasks = []

    def get_id(self):
        return self.ID
    
    def get_title(self):
        return self.Title
    
    
    def add_member(self, name):
        if name not in self.members:
            self.members.append(name)

    
    def __del__(self):
        print("Project deleted")