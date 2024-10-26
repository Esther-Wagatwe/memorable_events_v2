import random
import string
import lorem
from app import create_app, db
from models.user import User
from models.vendor import Vendor
from models.review import Review
from werkzeug.security import generate_password_hash


# Generate a weighted random rating
def weighted_starts_rating() -> int:
    return random.choices([1, 2, 3, 4, 5], weights=[0.5, 0.5, 1.5, 2.5, 5])[0]


# generate random password
def generate_random_password(length=10):
    """Generate a random password with letters and digits."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# generate data
def create_data():
    # Create a list of users with hashed passwords
    users_data = [
        {'username': 'John', 'email': "john.doe@example.com"},
        {'username': 'Emily', 'email': "emily.smith@example.com"},
        {'username': 'Michael', 'email': "michael.johnson@example.com"},
        {'username': 'Sarah', 'email': "sarah.williams@example.com"},
        {'username': 'David', 'email': "david.brown@example.com"},
        {'username': 'Jessica', 'email': "jessica.davis@example.com"},
    ]

    # create a list of users
    for user_data in users_data:
        # generate random password
        password = generate_random_password()
        # create new user
        new_user = User(
            username=user_data['username'],
            email=user_data['email'],
        )
        # set the hashed password
        new_user.password = generate_password_hash(password)
        # add user to the database
        db.session.add(new_user)
        # commit the changes
        db.session.commit()
        print(f"Created user: {new_user.username} with password: {password}")

    # Create a list of vendors
    vendors_data = [
        {'name': 'Acme Inc.', 'description': 'A wedding cake baking company.', 'image_path': 'https://images.unsplash.com/photo-1604702433171-33756f3f3825', 'phone_number': '0722653964', 'email': 'info@acmeltd.co.ke', 'service_fee': 26000},
        {'name': 'Floral Studio', 'description': 'A floral design studio.', 'image_path': 'https://images.unsplash.com/reserve/xd45Y326SvKzSR3Nanc8_MRJ_8125-1.jpg', 'phone_number': '0722653964', 'email': 'hello@floralstudio.com', 'service_fee': 452000},
        {'name': 'Cake Studio', 'description': 'A cake design studio.', 'image_path': 'https://images.unsplash.com/photo-1627580358573-ea0c4a2cb199', 'phone_number': '0722653964', 'email': 'joan@cakestudio.net', 'service_fee': 10000},
        {'name': 'Bakery Studio', 'description': 'A bakery design studio.', 'image_path': 'https://images.unsplash.com/photo-1585779885249-e55411459cf7', 'phone_number': '0722653964', 'email': 'bake69@gmail.com', 'service_fee': 65000},
        {'name': 'Wedding Studio', 'description': 'A wedding design studio.', 'image_path': 'https://images.unsplash.com/photo-1519741497674-611481863552', 'phone_number': '0722653964', 'email': 'contact@email.co.ze', 'service_fee': 15000},
        {'name': 'Event Studio', 'description': 'An event design studio.', 'image_path': 'https://images.unsplash.com/photo-1501281668745-f7f57925c3b4', 'phone_number': '0722653964', 'email': 'all@email.com', 'service_fee': 25000},
    ]

    for vendor_data in vendors_data:
        print(f"Creating new vendor: {vendor_data['name']}")
        
        new_vendor = Vendor(**vendor_data)
        db.session.add(new_vendor)
        db.session.commit()
        
        # Create random reviews
        for _ in range(random.randint(1, 5)):
            random_user = random.choice(User.query.all())
            print(f"Creating new review for {vendor_data['name']} from {random_user.username}")
            
            review = Review(
                rating=weighted_starts_rating(),
                comment=lorem.sentence(),
                user=random_user,
                vendor=new_vendor
            )
            db.session.add(review)

        db.session.commit()  # Commit after adding all reviews for a vendor

    db.session.close()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        create_data()

# Created user: John with password: n1fAiGXE5g
# Created user: Emily with password: Z1GdQggkpp
# Created user: Michael with password: Hd5l3A9Q84
# Created user: Sarah with password: S8yQSSH9En
# Created user: David with password: N6WLYvcaCg
# Created user: Jessica with password: YSCs3eCkzj
