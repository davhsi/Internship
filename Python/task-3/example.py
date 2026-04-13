import db
from model import Model
from fields import CharField, IntegerField, ForeignKey

# Setup connection
connect = db.connect
close = db.close
conn = connect("example.db") 


# Define models
class User(Model):
    name = CharField(max_length=100)                     
    email = CharField(max_length=255, unique=True)
    age = IntegerField(nullable=True)


class Post(Model):
    title = CharField(max_length=200)
    author = ForeignKey(User, related_name="posts")


# Create tables
User.create_table()
Post.create_table()


# Create users
alice = User(name="Alice", email="alice@example.com", age=30)
alice.save()

bob = User(name="Bob", email="bob@example.com", age=25)
bob.save()


# Create posts
post1 = Post(title="Hello World", author=alice)
post1.save()

post2 = Post(title="Another Post", author=bob)
post2.save()


# Database queries
all_users = User.all()

users = User.filter(age_gte=25).order_by("name").all()

user = User.get(name="Alice")
print(f"Found: {user}")

posts = alice.posts.all()


# Update data
bob.name = "Bobby"
bob.save()

# Close connection
close()