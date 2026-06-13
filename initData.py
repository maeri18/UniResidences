def initDatabase(db):
    random.seed(42)

    roomDescriptions = {
        1: "Type 1: Single room. Shared bathroom and kitchen, average size: 15 m2",
        2: "Type 2: Single room. Private bathroom, shared kitchen, average surface: 19 m2",
        3: "Type 3: Studio apartment. Private bathroom and kitchen. Single, average size, 24 m2",
        4: "Type 4: Studio apartment. Private bathroom and kitchen. Double (only for couples), average size, 35 m2",
        5: "Type 5: Two-room apartment. Private kitchen/living room, bathroom and one bedroom. (Only for couples): average size, 44 m2",
    }

    location = {
        1: "Esch-sur-Alzette",
        2: "Niederkorn",
        3: "Luxembourg City",
        4: "Kayl",
        5: "Dudelange",
        6: "Differdange",
        7: "Clervaux",
        8: "Ettelbruck",
        9: "Mersch",
    }

    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy", "Karl", "Leo", "Mallory", "Nina", "Oscar", "Peggy", "Quentin", "Rupert", "Trent", "Ingrid", "Ayat"]
    family_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Chekam","Hmideh"]

    for i in range(20):
        rent = random.randint(350, 950)
        room_id = generate_random_room_id()
        while db.session.get(Room, room_id) is not None:
            room_id = generate_random_room_id()

        room = Room(
            room_Id=room_id,
            available=True,
            rent=rent,
            description=roomDescriptions[random.randint(1, 5)]
            + ". Located at : "
            + location[random.randint(1, 9)] + f"\nRent: {rent}",
        )
        db.session.add(room)

    for i in range(20):
        student_name = family_names[random.randint(0, len(family_names)-1)]+" "+ names[random.randint(0, len(names)-1)]
        password = "".join(
            random.choices(
                string.ascii_letters + string.digits + string.punctuation,
                k=random.randint(6, 12),
            )
        )

        student_id = generate_random_student_id()
        while db.session.get(Student, student_id) is not None:
            student_id = generate_random_student_id()

        
        student = Student(
            student_Id=student_id,
            student_name=student_name,
            password_hash=hashlib.shake_256(password.encode("utf-8")).hexdigest(50),
        )

        db.session.add(student)

    for i in range(10):
        password = "".join(
            random.choices(
                string.ascii_letters + string.digits + string.punctuation,
                k=random.randint(12, 15),
            )
        )

        admin_id = generate_random_admin_id()
        while db.session.get(Admin, admin_id) is not None:
            admin_id = generate_random_admin_id()


        admin = Admin(
            admin_Id=admin_id,
            password_hash=hashlib.shake_256(password.encode("utf-8")).hexdigest(50),
        )

        db.session.add(admin)


