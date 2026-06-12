from flask import Blueprint, jsonify, request, session
from models.Room import Room
from models.Application import Application, ApplicationStatus
from models import db
from models.Student import Student
from helper_functions import start_logging
import hashlib

import datetime

logger = start_logging("student_routes_", __name__)



student_bp = Blueprint("student", __name__)


@student_bp.route("/login", methods=["POST"])
def login():
    """This route is to receive login requests from the students. 
    The request should contain the student id and the password. 
    If the credentials are correct, the student id and the role of the user are stored in the session."""
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Missing credentials!"}), 403

        student_id_str = data.get("student_id")
        try_student_password = data.get("student_password")


        if student_id_str is None or try_student_password is None:
            return jsonify({"message": "Invalid credentials"}), 403

        if student_id_str is not None and try_student_password is not None:
            student_id = int(student_id_str)
            student = db.session.get(Student, student_id)

            if student is not None:
                student_password_hash = student.password_hash
                try_password_hash = hashlib.shake_256(
                    try_student_password.encode("utf-8")
                ).hexdigest(50)
                if try_password_hash == student_password_hash:
                    session["student_id"] = student_id
                    session["role"] = "student"
                    return jsonify({}), 200
        return jsonify({"message": "Invalid credentials"}), 403

    except Exception as e:
        logger.error(f"An error occured {e}")
        return jsonify({"message": f"An error occured  {e}"}), 400


@student_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({}), 200


@student_bp.before_request
def restrict_to_student():
    """This function is to restrict the access to the student routes only to the students."""

    if request.method == "OPTIONS":
        return None 
    
    if request.endpoint == "student.login":
        return None
    

    if session.get("role") != "student":
        return jsonify({"message": "Access denied. Student privileges required."}), 403
        


@student_bp.route("/rooms/available", methods=["GET"])
def get_all_free_rooms():
    """This route is to receive requests for getting which rooms are currently available.
    The request should contain the minimun budget and maximum budget for the room rent.
    If the minimum budget is not provided, it defaults to 0.
    If the maximum budget is not provided, it defaults to the biggest rent of an existing room.
    """
    min_budget = None
    max_budget = None
    try:
        min_budget = request.args.get("min_budget", type=int)
        max_budget = request.args.get("max_budget", type=int)

        rooms = None
        query = Room.query.filter(Room.available == True)
        if min_budget is not None:
            min_budget=max(0,min_budget)
            query = query.filter(Room.rent >= min_budget)
        if max_budget is not None:
            max_budget=max(0,max_budget)
            query = query.filter(Room.rent <= max_budget)
        rooms = query.all()
        return jsonify([r.room_Id for r in rooms]), 200
    except Exception as e:
        logger.error(f"An error occured {e}")
        return jsonify({"message": f"An error occured  {e}"}), 400


@student_bp.route("/rooms/description", methods=["GET"])
def check_free_room_description():
    """This route is to receive requests for getting the description (location, rent,...) of a room.
    The request should contain the room id. 
    This route is only for free rooms, if the room is occupied, an error message is returned."""
    try:
        room_id = request.args.get("room_id", type=int)
        if room_id is not None:
            room = db.session.get(Room, room_id)
            if room is not None and room.available == True:
                description = room.to_dict().get("description")
                return jsonify({"description": description}), 200

        return jsonify({"message": "Invalid room identifier"}), 422
    except Exception as e:
        logger.error(f"An error occured {e}")
        return jsonify({"message": f"An error occured  {e}"}), 400


@student_bp.route("/rooms/apply", methods=["POST"])
def apply_for_a_room():
    """This route is to receive requests for applying for a room.
    The request should contain the room id, the student id and an application message.
    If the room is not yet occupied, the application is successful, the status of the application is set to pending
    If the application is successful, the student can not apply for another room until the status of the application is changed to rejected.
   """
    try:

        room_id = request.args.get("room_id", type=int)
        student_id = request.args.get("student_id", type=int)
        request_data = request.get_json()

        application_message = None
        if request_data is not None:
            application_message = request_data.get("application_message")

        if (
            room_id is not None
            and student_id is not None
            and application_message is not None
        ):
            if student_id != session.get("student_id"):
                return jsonify({"message":"You are not allowed to do this"}), 403
            
            room = db.session.get(Room, room_id)

            if room is None:
                return jsonify({"message": "Invalid room identifier"}), 422

            student_active_applications = Application.query.filter(
                Application.student_Id == student_id,
                db.or_(
                    Application.status == ApplicationStatus.PENDING,
                    Application.status == ApplicationStatus.ACCEPTED,
                ),
            ).all()

            if room.available == True and student_active_applications == []:
                new_application = Application(
                    status=ApplicationStatus.PENDING,
                    application_message=application_message,
                    submission_date=datetime.datetime.now(),
                    student_Id=student_id,
                    room_Id=room_id,
                )
                db.session.add(new_application)
                db.session.commit()
                return jsonify({"message": "Successfully created the application"}), 201
            elif room.available == False:
                return (
                    jsonify({"message": "Can't submit application for occupied room."}),
                    422,
                )
            else:
                return (
                    jsonify(
                        {
                            "message": "Can not submit a new application at the moment. Reason is, there is already a pending/accepted application for this student."
                        }
                    ),
                    422,
                )

        else:
            return (
                jsonify(
                    {
                        "message": "One of the required to submit the application parameters is missing "
                    }
                ),
                400,
            )
    except Exception as e:
        db.session.rollback() # rollback in case of an error to avoid having the database in an inconsistent state
        logger.error(f"An error occured {e}")
        return jsonify({"message": f"An error occured  {e}"}), 400


@student_bp.route("/applications/all", methods=["GET"])
def get_all_applications():
    """This route is to receive requests for getting all the applications details (application id, submission date, room description, rent) submitted by a student.
    The result is sorted by submission date, the most recent application is the first in the list.
    """
    try:
        student_id = request.args.get("student_id", type=int)

        if student_id is not None:
            if student_id != session.get("student_id"):
                return jsonify({"message":"You are not allowed to do this"}), 403

            student_applications = None
            student = db.session.get(Student, student_id)
            if student is not None:
                student_applications = student.submitted
            else:
                return jsonify({"message": "Unexisting student"}), 422

            details = [
                application_details
                for application_details in sorted(
                    [
                        (
                            app.submission_date,
                            app.application_Id,
                            app.linksTo.description,
                            app.linksTo.rent,
                        )
                        for app in student_applications
                    ]
                )
            ]
            details.reverse() # to have the most recent application first in the list

            return jsonify({"applicationDetails": details, }), 200
        else:
            return (
                jsonify(
                    {
                        "message": "One of the required to submit the application parameters is missing "
                    }
                ),
                400,
            )

    except Exception as e:
        logger.error(f"An error occured {e}")
        return jsonify({"message": f"An error occured  {e}"}), 400


@student_bp.route("/application/status", methods=["GET"])
def check_application_status():
    """This route is to receive requests for getting the status of an application.
    The request should contain the application id and the student id."""
    try:
        student_id = request.args.get("student_id", type=int)
        application_id = request.args.get("application_id", type=int)

        if student_id is not None and application_id is not None:
            if student_id != session.get("student_id"):
                return jsonify({"message":"You are not allowed to do this"}), 403
            application_status = None
            application = Application.query.filter(
                Application.application_Id == application_id,
                Application.student_Id == student_id,
            ).first()

            if application is not None:
                application_status = application.to_dict().get("status")
                return jsonify({"status": application_status}), 200
            else:
                return jsonify({"message": "Unexisting application identifier"}), 422

        else:
            return (
                jsonify(
                    {
                        "message": "One of the required to submit the application parameters is missing "
                    }
                ),
                400,
            )

    except Exception as e:
        logger.error(f"An error occured {e}")
        return jsonify({"message": f"An error occured  {e}"}), 400
