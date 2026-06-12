from flask import Blueprint, jsonify, request, session
from models.Room import Room
from models.Application import Application, ApplicationStatus
from models import db
from models.Admin import Admin
from helper_functions import start_logging, parse_bool_arg
import hashlib

logger = start_logging("admin_routes_", __name__)


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/login", methods=["POST"])
def login():
    """Admin login route. Expects JSON with 'admin_id' and 'admin_password' fields. Validates credentials and starts a session if successful."""
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Missing credentials!"}), 403

        admin_id_str = data.get("admin_id")
        try_admin_password = data.get("admin_password")

        print("*******Tried to login with ",admin_id_str," and ", try_admin_password)

        if admin_id_str is None or try_admin_password is None:
            return jsonify({"message": "Missing credentials"}), 403

        if admin_id_str is not None and try_admin_password is not None:
            admin_id = int(admin_id_str)
            admin = db.session.get(Admin, admin_id)

            if admin is not None:
                admin_password_hash = admin.password_hash
                try_password_hash = hashlib.shake_256(
                    try_admin_password.encode("utf-8")
                ).hexdigest(50)
                
                if try_password_hash == admin_password_hash:
                    session["admin_id"] = admin_id
                    session["role"] = "admin"
                    return jsonify({}), 200
        return jsonify({"message": "Missing credentials"}), 403
    except Exception as e:
        logger.error(f"An error occured {e}")
        return jsonify({"message": f"An error occured  {e}"}), 400


@admin_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({}), 200


@admin_bp.before_request
def restrict_to_admins():

    if request.method == "OPTIONS":
        return None 
     
    if request.endpoint == "admin.login":
        return None
    
    if session.get("role") != "admin":
        return (
            jsonify({"message": "Access denied. Administrator privileges required."}),
            403,
        )


@admin_bp.route("/rooms/all", methods=["GET"])
def get_all_rooms():
    try:
        availability = parse_bool_arg(request.args.get("availability"))
        min_budget = request.args.get("min_budget", type=int)
        max_budget = request.args.get("max_budget", type=int)

        rooms = None
        if availability is not None:
            query = Room.query.filter(Room.available == availability)
        else:
            query = Room.query

        if min_budget is not None:
            query = query.filter(Room.rent >= min_budget)

        if max_budget is not None:
            query = query.filter(Room.rent <= max_budget)

        rooms = query.all()

        return jsonify([r.room_Id for r in rooms]), 200

    except Exception as e:
        logger.error(f"An error occured {e}")
        return jsonify({"message": f"An error occured  {e}"}), 400


@admin_bp.route("/applications/details", methods=["GET"])
def check_application_details():
    try:
        application_id = request.args.get("application_id", type=int)
        if application_id is not None:
            application = db.session.get(Application, application_id)
            if application is not None:
                details = application.to_dict()
                details["submission_date"]
                return jsonify(details), 200

        return jsonify({"message": "Non-existing application"}), 422

    except Exception as e:
        logger.error(f"An error occured {e}")
        return jsonify({"message": f"An error occured  {e}"}), 400


@admin_bp.route("/applications/pending", methods=["GET"])
def check_pending_application():
    try:
        pending_applications = (
            Application.query.filter(Application.status == ApplicationStatus.PENDING)
            .order_by(Application.submission_date.desc())
            .all()
        )
        pending_applications_id = [app.application_Id for app in pending_applications]

        return jsonify(pending_applications_id), 200
    except Exception as e:
        logger.error(f"An error occured {e}")
        return jsonify({"message": f"An error occured  {e}"}), 400


@admin_bp.route("/applications/accept", methods=["PUT"])
def accept_student_application():
    try:
        application_id = request.args.get("application_id", type=int)
        admin_id = request.args.get("admin_id", type=int)
        if admin_id is not None:
            admin = db.session.get(Admin, admin_id)
            if admin is None:
                return jsonify({"message": "Can't perform the action"}), 403
            
            if admin_id != session.get("admin_id"):
                return jsonify({"message":"You are not allowed to do this"}), 403

            if application_id is not None:
                application = db.session.get(Application, application_id)
                if (
                    application is not None
                    and application.status == ApplicationStatus.PENDING
                ):
                    application.status = ApplicationStatus.ACCEPTED
                    application.admin_Id = admin_id
                    linkedRoom = application.linksTo
                    linkedRoom.available = False
                    db.session.commit()
                    return jsonify({}), 200

            return jsonify({"message": "Invalid identifier provided"}), 422
        else:
            return jsonify({"message": "Can't perform the action"}), 403

    except Exception as e:
        db.session.rollback()
        logger.error(f"An error occured {e}")
        return jsonify({"message": f"An error occured  {e}"}), 400


@admin_bp.route("/applications/reject", methods=["PUT"])
def reject_student_application():
    try:
        application_id = request.args.get("application_id", type=int)
        request_data = request.get_json()
        reason_for_refusal = None
        admin_id = request.args.get("admin_id", type=int)

        if admin_id is not None:
            admin = db.session.get(Admin, admin_id)
            if admin is None:
                return jsonify({"message": "Can't perform the action"}), 403
            
            if admin_id != session.get("admin_id"):
                return jsonify({"message":"You are not allowed to do this"}), 403

            if request_data is not None:
                reason_for_refusal = request_data.get("reason_for_refusal")

            if reason_for_refusal is None or len(reason_for_refusal.strip())==0:
                return jsonify({"message": "Missing reason for refusal"}), 422

            if application_id is not None and reason_for_refusal is not None:
                application = db.session.get(Application, application_id)
                if (
                    application is not None
                    and application.status == ApplicationStatus.PENDING
                ):
                    application.status = ApplicationStatus.REJECTED
                    application.reason_for_refusal = reason_for_refusal
                    application.admin_Id = admin_id
                    db.session.commit()
                    return jsonify({}), 200
            return jsonify({"message": "Invalid identifier provided"}), 422

        else:
            return jsonify({"message": "Can't perform the action"}), 403

    except Exception as e:
        db.session.rollback()
        logger.error(f"An error occured {e}")
        return jsonify({"message": f"An error occured  {e}"}), 400
