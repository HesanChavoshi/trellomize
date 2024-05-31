import unittest
from datetime import datetime, timedelta
from project import Project
from Task import Priority
from Task import Status
from Task import Task
import User

class TestProject(unittest.TestCase):
    
    def setUp(self):
        self.project = Project(id=1, title="Test Project", leader="John Doe", members=["Alice", "Bob"], tasks=[])
        self.task = Task(title="Task 1", description="Description for Task 1", assignees=[], history=[], comments=[], project=self.project.id, start=datetime.now(), end=datetime.now() + timedelta(days=1))

    def test_initialization(self):
        self.assertEqual(self.project.id, 1)
        self.assertEqual(self.project.title, "Test Project")
        self.assertEqual(self.project.leader, "John Doe")
        self.assertEqual(self.project.members, ["Alice", "Bob"])
        self.assertEqual(self.project.tasks, [])

    def test_add_member(self):
        self.project.add_member("Charlie")
        self.assertIn("Charlie", self.project.members)
        
    def test_add_existing_member(self):
        self.project.add_member("Alice")
        self.assertEqual(self.project.members.count("Alice"), 1)

    def test_remove_member(self):
        self.project.remove_member("Alice")
        self.assertNotIn("Alice", self.project.members)
        
    def test_remove_nonexistent_member(self):
        self.project.remove_member("Charlie")
        self.assertNotIn("Charlie", self.project.members)

    def test_add_task(self):
        self.project.add_task(self.task)
        self.assertIn(self.task, self.project.tasks)

    def test_add_existing_task(self):
        self.project.add_task(self.task)
        self.project.add_task(self.task)
        self.assertEqual(self.project.tasks.count(self.task), 1)

    def test_remove_task(self):
        self.project.add_task(self.task)
        self.project.remove_task(self.task)
        self.assertNotIn(self.task, self.project.tasks)

    def test_remove_nonexistent_task(self):
        self.project.remove_task(self.task)
        self.assertNotIn(self.task, self.project.tasks)
        
    def test_assign_task(self):
        self.project.tasks.append(self.task)
        self.project.assign_task(self.task.id, "Alice")
        self.assertIn("Alice", self.task.assignees)

    def test_assign_task_to_non_member(self):
        self.project.tasks.append(self.task)
        with self.assertLogs() as cm:
            self.project.assign_task(self.task.id, "Charlie")
        self.assertIn("Member Charlie is not part of the project.", cm.output[0])

class TestTask(unittest.TestCase):

    def setUp(self):
        self.task = Task(title="Task 1", description="Description for Task 1", assignees=[], history=[], comments=[], project=1, start=datetime.now(), end=datetime.now() + timedelta(days=1))

    def test_initialization(self):
        self.assertEqual(self.task.title, "Task 1")
        self.assertEqual(self.task.description, "Description for Task 1")
        self.assertEqual(self.task.assignees, [])
        self.assertEqual(self.task.priority, Priority.LOW)
        self.assertEqual(self.task.status, Status.BACKLOG)
        self.assertEqual(self.task.history, [])
        self.assertEqual(self.task.comments, [])
        self.assertEqual(self.task.project, 1)

    def test_add_assignee(self):
        self.task.add_assignee("Alice")
        self.assertIn("Alice", self.task.assignees)

    def test_remove_assignee(self):
        self.task.add_assignee("Alice")
        self.task.remove_assignee("Alice")
        self.assertNotIn("Alice", self.task.assignees)

    def test_change_priority(self):
        self.task.change_priority(Priority.HIGH)
        self.assertEqual(self.task.priority, Priority.HIGH)

    def test_change_status(self):
        self.task.change_status(Status.DOING)
        self.assertEqual(self.task.status, Status.DOING)

    def test_add_comment(self):
        self.task.add_comment("Alice", "Great job!")
        self.assertIn("Alice: Great job!", self.task.comments)

    def test_add_history(self):
        self.task.add_history("Task created.")
        self.assertIn("Task created.", self.task.history)

    def test_change_start(self):
        new_start = datetime.now() + timedelta(days=2)
        self.task.change_start(new_start)
        self.assertEqual(self.task.start, new_start)

    def test_change_end(self):
        new_end = datetime.now() + timedelta(days=5)
        self.task.change_end(new_end)
        self.assertEqual(self.task.end, new_end)


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User(username="john_doe", age=30, password="securepassword", email="john@example.com", tasks=[], projects=[])

    def test_initialization(self):
        self.assertEqual(self.user.username, "john_doe")
        self.assertEqual(self.user.age, 30)
        self.assertEqual(self.user.password, "securepassword")
        self.assertEqual(self.user.email, "john@example.com")
        self.assertEqual(self.user.status, "on")
        self.assertEqual(self.user.tasks, [])
        self.assertEqual(self.user.projects, [])

    def test_set_get_name(self):
        self.user.set_name("jane_doe")
        self.assertEqual(self.user.get_name(), "jane_doe")

    def test_set_get_age(self):
        self.user.set_age(25)
        self.assertEqual(self.user.get_age(), 25)

    def test_set_get_password(self):
        self.user.set_password("newpassword")
        self.assertEqual(self.user.get_password(), "newpassword")

    def test_set_get_email(self):
        self.user.set_email("jane@example.com")
        self.assertEqual(self.user.get_email(), "jane@example.com")

    def test_add_task(self):
        task = "Task 1"
        self.user.add_task(task)
        self.assertIn(task, self.user.tasks)

    def test_remove_task(self):
        task = "Task 1"
        self.user.add_task(task)
        self.user.remove_task(task)
        self.assertNotIn(task, self.user.tasks)

    def test_add_project(self):
        project = "Project 1"
        self.user.add_project(project)
        self.assertIn(project, self.user.projects)

    def test_remove_project(self):
        project = "Project 1"
        self.user.add_project(project)
        self.user.remove_project(project)
        self.assertNotIn(project, self.user.projects)

    def test_change_status(self):
        self.user.change_status()
        self.assertEqual(self.user.status, "off")
        self.user.change_status()
        self.assertEqual(self.user.status, "on")

if __name__ == '__main__':
    unittest.main()
