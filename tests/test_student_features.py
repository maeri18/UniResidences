import pytest
import hashlib
import datetime
from flask import jsonify
from models.Student import Student
from models.Application import Application, ApplicationStatus
from models.Room import Room


def test_for_test_database_correctness(new_db):
    # students data correctness
    # Testing stored student ids existence
    student1 = new_db.get(Student, 811)
    student2 = new_db.get(Student, 1269)
    student3 = new_db.get(Student, 7617)
    
    assert student1 is not None
    assert student2 is not None
    assert student3 is not None

    # Testing student password correctness
    student1_test_password_hash = hashlib.shake_256(b"Au*jJHGy").hexdigest(50)
    student2_test_password_hash = hashlib.shake_256(b"vBhvjA7IItz").hexdigest(50)
    student3_test_password_hash = hashlib.shake_256(b"+vdDzt_?D9L\\").hexdigest(50)

    assert student1.password_hash == student1_test_password_hash
    assert student2.password_hash == student2_test_password_hash
    assert student3.password_hash == student3_test_password_hash


    # rooms data correctness
    # Testing stored room ids existence
    room1 = new_db.get(Room, 1924)
    room2 = new_db.get(Room, 3757)   
    room3 = new_db.get(Room, 9035)   
    room4 = new_db.get(Room, 588)
    room5 = new_db.get(Room, 8379)

    assert room1 is not None
    assert room2 is not None        
    assert room3 is not None
    assert room4 is not None    
    assert room5 is not None

    # Testing that all rooms are initially available
    assert room1.available == True  
    assert room2.available == True  
    assert room3.available == True  
    assert room4.available == True  
    assert room5.available == True  

    # Testing that initially all rooms have no applications
    assert room1.isLinkedTo == []
    assert room2.isLinkedTo == []
    assert room3.isLinkedTo == []
    assert room4.isLinkedTo == []
    assert room5.isLinkedTo == []


@pytest.fixture(scope="session")
def student_login_data():
    """ This fixture provides a list of valid student login credentials for testing purposes."""
    login_data = [(811, "Au*jJHGy"), (1269, "vBhvjA7IItz"), (7617, "+vdDzt_?D9L\\")]
       
    return login_data

@pytest.fixture(scope="session")
def all_room_ids():
    room_ids = [1924, 3757,  9035,  588, 8379]

    return room_ids

@pytest.fixture(scope="session")
def all_rooms():

    rooms = [{'id': 1924, 'available': True, 'rent': 677, 'description': 'Type 1: Single room. Shared bathroom and kitchen, average size: 15 m2. Located at : Dudelange\nRent: 677'},
{'id': 3757, 'available': True, 'rent': 475, 'description': 'Type 2: Single room. Private bathroom, shared kitchen, average surface: 19 m2. Located at : Niederkorn\nRent: 475'},
{'id': 9035, 'available': True, 'rent': 696, 'description': 'Type 1: Single room. Shared bathroom and kitchen, average size: 15 m2. Located at : Clervaux\nRent: 696'},
{'id': 588, 'available': True, 'rent': 366, 'description': 'Type 1: Single room. Shared bathroom and kitchen, average size: 15 m2. Located at : Kayl\nRent: 366'},
{'id': 8379, 'available': True, 'rent': 469, 'description': 'Type 5: Two-room apartment. Private kitchen/living room, bathroom and one bedroom. (Only for couples): average size, 44 m2. Located at : Esch-sur-Alzette\nRent: 469'}
    ]

    return rooms
    

def test_student_login(student_login_data, new_client):
    """ This test function verifies the student login functionality by testing both valid and invalid login attempts."""
   
    test_wrong_student_password = "wrongPassword"

    for test_student_id, test_student_password in student_login_data:
        credentials = {"student_id":test_student_id, "student_password":test_student_password}
        wrong_credentials_1 = {"student_id":test_student_id, "student_password":test_wrong_student_password} # wrong password
        wrong_credentials_2 = {"student_id":0, "student_password":test_student_password} # wrong student id, and existing password
        wrong_credentials_3 = {"student_id":-1, "student_password":test_student_password} # wrong student id, and existing password
        missing_credentials_1 = {"student_password":test_wrong_student_password} # missing student id
        missing_credentials_2 = {"student_id":test_student_id} # missing student password
     
        response = new_client.post("/student/login", json=credentials)
        assert response.status_code == 200

        response = new_client.post("/student/login", json=wrong_credentials_1)
        assert response.status_code == 403

        response = new_client.post("/student/login", json=wrong_credentials_2)
        assert response.status_code == 403

        response = new_client.post("/student/login", json=wrong_credentials_3)
        assert response.status_code == 403

        response = new_client.post("/student/login", json=missing_credentials_1)
        assert response.status_code == 403

        response = new_client.post("/student/login", json=missing_credentials_2)
        assert response.status_code == 403


def test_get_all_free_rooms(student_login_data, new_client, all_rooms, all_room_ids, new_db):
    """ This test function verifies the functionality of retrieving available rooms based on different budget criteria.
      It tests the response for various combinations of minimum and maximum budget parameters, as well as the behavior when a room's availability status is changed."""
    
    # fake student login
    student_id, student_password = student_login_data[0]
    credentials = {"student_id":student_id, "student_password":student_password}
    new_client.post("/student/login", json=credentials)
    
    # Testing with empty query
    query={}
    response = new_client.get("/student/rooms/available", query_string=query)
    assert response.json==all_room_ids
    assert response.status_code == 200

    # Testing with different budget ranges
    min_budgets = [0,450,1900,-1]
    max_budgets = [0,500,-40]

    for min_budget in min_budgets:
        for max_budget in max_budgets:
            query={"min_budget":min_budget, "max_budget":max_budget}
            response = new_client.get("/student/rooms/available", query_string=query)

            expected_room_ids = [room.get('id') for room in all_rooms if room.get('rent')<=max_budget and room.get('rent')>=min_budget]

            assert response.json==expected_room_ids
            assert response.status_code == 200

            query={"max_budget":max_budget}
            response = new_client.get("/student/rooms/available", query_string=query)

            expected_room_ids = [room.get('id') for room in all_rooms if room.get('rent')<=max_budget ]

            assert response.json==expected_room_ids
            assert response.status_code == 200

            query={"min_budget":min_budget}
            response = new_client.get("/student/rooms/available", query_string=query)

            expected_room_ids = [room.get('id') for room in all_rooms if room.get('rent')>=min_budget]

            assert response.json==expected_room_ids
            assert response.status_code == 200


    # Changing a room of id 1924 and of rent 677 to unavailable
    room = new_db.get(Room, all_room_ids[0])
    room.available = False

    new_db.commit()

    # Fetching rooms from rent range [670 , 680]. Only room of id 1924 is in that range, so the application should respond with an empty list
    query={"min_budget":670, "max_budget":680}
    response = new_client.get("/student/rooms/available", query_string=query)
    assert response.json == []
    assert response.status_code == 200



def test_check_free_room_description(student_login_data, new_client, all_rooms,new_db):
    """ This test function verifies the functionality of retrieving the description of a specific room based on its identifier.
      It tests the response for valid room identifiers, as well as the behavior when invalid room identifiers are provided."""

    # Fake student login
    student_id, student_password = student_login_data[0]
    credentials = {"student_id":student_id, "student_password":student_password}
    new_client.post("/student/login", json=credentials)

    # Testing with real room identifiers
    for i in range(len(all_rooms)):
        room_id = all_rooms[i]["id"]
        query = {"room_id":room_id}
        response = new_client.get("/student/rooms/description", query_string=query)

        assert response.status_code == 200
        assert response.json["description"] == all_rooms[i]["description"]

    # testing with fake room identifiers
    wrong_room_ids = [0,-1,1000]
    for wrong_room_id in wrong_room_ids:
        query = {"room_id":wrong_room_id}
        response = new_client.get("/student/rooms/description", query_string=query)

        assert response.status_code == 422
        assert response.json["message"] == "Invalid room identifier"

def test_apply_for_a_room(student_login_data, new_client, all_room_ids, new_db):
    """ This test function verifies the functionality of applying for a room by a student.
      It tests the response for valid application scenarios, as well as the behavior when attempting
        to apply for an occupied room or when there is already a pending application for the student."""

    # fake student login to be able to use student roles
    student_id, student_password = student_login_data[0]
    credentials = {"student_id":student_id, "student_password":student_password}
    new_client.post("/student/login", json=credentials)


    # Application when the room is occupied
    # Making a room unavailable
    room_id = all_room_ids[0]
    room_to_be_occupied = new_db.get(Room, room_id)
    room_to_be_occupied.available = False

    new_db.commit()

    application_message = {"application_message" : "Can I have this room?"}
    query = {"room_id":room_id, "student_id":student_id}

    response = new_client.post("/student/rooms/apply", json=application_message, query_string=query)
    assert response.status_code==422
    assert response.json["message"]=="Can't submit application for occupied room."


    # Making the room available again for next test
    room_to_be_occupied.available = True
    new_db.commit()
    

    # Valid application
    room_id = all_room_ids[2]
    application_message = {"application_message" : "Can I have this room?"}
    query = {"room_id":room_id, "student_id":student_id}

    # in the database, initially there is no application
    assert len(new_db.query(Application).all())==0
    response = new_client.post("/student/rooms/apply", json=application_message, query_string=query)

    assert response.status_code == 201 # 201 because we created a ressource

    # we now have exactly one application in the database
    applications_list = new_db.query(Application).all()
    assert len(applications_list) == 1


    # Ensuring the application has the correct values (student id, room id ...)
    assert applications_list[0].status == ApplicationStatus.PENDING
    assert applications_list[0].student_Id == student_id
    assert applications_list[0].room_Id == room_id
    assert applications_list[0].application_message == application_message["application_message"]



    # Application when there is already a pending application
    old_application_id = applications_list[0].application_Id 
    room_id = all_room_ids[1]
    application_message = {"application_message" : "Please, can I have this room too?"}
    query = {"room_id":room_id, "student_id":student_id}

    response = new_client.post("/student/rooms/apply", json=application_message, query_string=query)

    assert response.status_code ==  422
    assert response.json["message"] == "Can not submit a new application at the moment. Reason is, there is already a pending/accepted application for this student."


    # Checking that the new application was not created
    applications_list = new_db.query(Application).all()
    assert len(applications_list) == 1
    assert applications_list[0].application_Id == old_application_id


   
def test_get_all_applications(student_login_data, new_client, all_room_ids, new_db):
    """ This test function verifies the functionality of retrieving all applications submitted by a student.
      It tests the behavior when there are no applications or when an application exist for the student."""
    # fake student login to be able to use student roles
    student_id, student_password = student_login_data[2]
    credentials = {"student_id":student_id, "student_password":student_password}
    new_client.post("/student/login", json=credentials)

    # No application yet, so the application should return an empty list
    query={"student_id":student_id}
    response=new_client.get("/student/applications/all", query_string=query)

    assert response.status_code==200
    assert response.json["applicationDetails"]==[]

    # Submitting a valid application for room of id 1924
    room_id = all_room_ids[0]
    application_message = {"application_message" : "I need this room because soon my parents will kick me out!"}
    query = {"room_id":room_id, "student_id":student_id}
    response = new_client.post("/student/rooms/apply", json=application_message, query_string=query)

    # checking that the application was sucessfull
    assert response.status_code == 201 # 201 because we created a ressource

    # getting the newly created application from the database
    application = new_db.query(Application).all()[0]

    # Checking again the list of application for this student
    query={"student_id":student_id}
    response=new_client.get("/student/applications/all", query_string=query)
    fetched_applications = response.json["applicationDetails"]

    assert response.status_code==200
    assert len(fetched_applications)==1
    
    # checking that the fetched application is the correct one
    _ , fetched_application_id,_,_  = fetched_applications[0]
    assert fetched_application_id == application.application_Id


def test_check_application_status(student_login_data, new_client, all_room_ids, new_db):
    """ This test function verifies the functionality of checking the status of a specific application submitted by a student.
      It tests the behavior when an invalid application identifier is provided, as well as the response for valid application identifiers with different application statuses."""
    # fake student login to be able to use student roles
    student_id, student_password = student_login_data[1]
    credentials = {"student_id":student_id, "student_password":student_password}
    new_client.post("/student/login", json=credentials)

    # Trying to check the status of a non-existing application
    wrong_application_id = 1000
    query={"student_id":student_id, "application_id":wrong_application_id}
    response=new_client.get("/student/application/status", query_string=query)

    assert response.status_code==422
    assert response.json['message']=="Unexisting application identifier"


    # adding a new applications:
    # to another student
    other_student_id, _ = student_login_data[0]
    new_application_1 = Application(application_Id=1,
                    status=ApplicationStatus.PENDING,
                    application_message="",
                    submission_date=datetime.datetime.now(),
                    student_Id=other_student_id,
                    room_Id=all_room_ids[1],
                )
    
    # To the real student
    new_application_2 = Application(application_Id=2,
                    status=ApplicationStatus.ACCEPTED,
                    application_message="",
                    submission_date=datetime.datetime.now(),
                    student_Id=student_id,
                    room_Id=all_room_ids[2],
                )


    new_db.add(new_application_1)
    new_db.add(new_application_2)
    new_db.commit()

    # Trying to check the status of an accepted application 
    query={"student_id":student_id, "application_id":2}
    response=new_client.get("/student/application/status", query_string=query)
    assert response.status_code==200
    assert response.json["status"]==ApplicationStatus.ACCEPTED.value

    # Trying to check the status of a pending application a wrong student id that is not the one of the student who submitted the application
    query={"student_id":student_id, "application_id":1}
    response=new_client.get("/student/application/status", query_string=query)
    assert response.status_code==422
    assert response.json["message"]=="Unexisting application identifier"

    
