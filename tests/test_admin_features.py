import pytest

from models.Student import Student
from models.Application import Application, ApplicationStatus
from models.Room import Room
import datetime

@pytest.fixture(scope="session")
def admin_login_credentials():
    """Provides test credentials for the university housing administrators."""
    return {"admin_id": 2721, "admin_password": "yx0y2[Lu~Viek"}


def test_admin_login_and_logout(new_client, admin_login_credentials):
    """Verifies that an administrator can securely login and logout of the system."""
    # Test valid login
    response = new_client.post("/admin/login", json=admin_login_credentials)
    assert response.status_code == 200

    # Test invalid login credentials
    bad_credentials = {"admin_id": admin_login_credentials["admin_id"], "admin_password": "wrongPassword"}
    response = new_client.post("/admin/login", json=bad_credentials)
    assert response.status_code == 403

    # Test logout functionality
    response = new_client.post("/admin/logout")
    assert response.status_code == 200


def test_get_all_rooms(new_client, admin_login_credentials, new_db):
    """Verifies that admins can search and filter room identifiers based on availability."""
    # Authenticate admin session
    new_client.post("/admin/login", json=admin_login_credentials)

    # 1. Test searching for free rooms
    response = new_client.get("/admin/rooms/all", query_string={"availability": "True"})
    assert response.status_code == 200
    free_room_ids = response.json
    assert isinstance(free_room_ids, list)

    # Verify that all returned IDs are actually marked as available in the DB
    for r_id in free_room_ids:
        room = new_db.get(Room, r_id)
        assert room.available is True

    # 2. Test searching for occupied rooms
    response = new_client.get("/admin/rooms/all", query_string={"availability": "False"})
    assert response.status_code == 200
    occupied_room_ids = response.json
    assert isinstance(occupied_room_ids, list)



def test_handle_application_approval_flow(new_client, admin_login_credentials, new_db):
    """Verifies the complete lifecycle of approving a pending student room application."""
    new_client.post("/admin/login", json=admin_login_credentials)

    # 1. Setup a fresh pending application in the DB safely linked to a free room
    test_room = new_db.query(Room).filter_by(available=True).first()
    test_student = new_db.query(Student).first()
    
    pending_app = Application(
        status=ApplicationStatus.PENDING,
        application_message="Requesting a place to study.",
        submission_date=datetime.datetime.now(),
        student_Id=test_student.student_Id,
        room_Id=test_room.room_Id
    )
    new_db.add(pending_app)
    new_db.commit()

    # 2. Test reading all pending application identifiers
    response = new_client.get("/admin/applications/pending")
    assert response.status_code == 200
    assert pending_app.application_Id in response.json

    # 3. Test reading the specific details of this target application
    response = new_client.get("/admin/applications/details", query_string={"application_id": pending_app.application_Id})
    assert response.status_code == 200
    assert response.json["room_id"] == test_room.room_Id
    assert response.json["status"] == ApplicationStatus.PENDING.value

    # 4. Approve the application
    response = new_client.put(f"/admin/applications/accept", query_string={"application_id": pending_app.application_Id, "admin_id":admin_login_credentials['admin_id']})
    assert response.status_code == 200

    # 5. Assert the status has successfully transformed to ACCEPTED
    new_db.refresh(pending_app)
    assert pending_app.status == ApplicationStatus.ACCEPTED

    # 6. CRITICAL SPECIFICATION CHECK: Status can never be changed once accepted/rejected
    # Attempting to reject an already accepted application must fail
    bad_rejection_payload = {"reason": "Changing our mind."}
    response = new_client.put(
        "/admin/applications/reject", 
        json=bad_rejection_payload, 
        query_string={"application_id": pending_app.application_Id, "admin_id":admin_login_credentials['admin_id']}
    )
    assert response.status_code == 422  # Status cannot be modified further


def test_handle_application_rejection_validation(new_client, admin_login_credentials, new_db):
    """Ensures rejections mandate a textual reason and update state securely."""
    new_client.post("/admin/login", json=admin_login_credentials)

    test_room = new_db.query(Room).first()
    test_student = new_db.query(Student).first()
    
    pending_app = Application(
        status=ApplicationStatus.PENDING,
        application_message="Hoping for an allocation.",
        student_Id=test_student.student_Id,
        submission_date=datetime.datetime.now(),
        room_Id=test_room.room_Id
    )
    new_db.add(pending_app)
    new_db.commit()

    # 1. Attempt to reject WITHOUT providing a text reason (Should fail validation)
    empty_payload = {"reason_for_refusal": ""}
    response = new_client.put(
        f"/admin/applications/reject", 
        json=empty_payload, 
        query_string={"application_id": pending_app.application_Id, "admin_id":admin_login_credentials['admin_id']}
    )
    assert response.status_code == 422 # Bad request due to missing reason parameter
    assert response.json['message'] == "Missing reason for refusal"

    # 2. Reject WITH a formal valid text explanation
    valid_payload = {"reason_for_refusal": "The dormitory facility is undergoing scheduled maintenance. So no more rooms can be assigned for 2 months. Please re-submit the application once you've received an email saying that the maintenance is done."}
    response = new_client.put(
        "/admin/applications/reject", 
        json=valid_payload, 
        query_string={"application_id": pending_app.application_Id,"admin_id":admin_login_credentials['admin_id']}
    )
    assert response.status_code == 200

    # 3. Confirm database updates match the expected outcome
    new_db.refresh(pending_app)
    assert pending_app.status == ApplicationStatus.REJECTED