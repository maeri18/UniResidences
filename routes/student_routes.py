from flask import Blueprint, jsonify, request
from models.Room import Room, RoomTypeEnum, RoomAvailability
from models.Application import Application
from models.Contract import Contract
from models.Residence import Residence

import logging
import datetime

logger = logging.getLogger(__name__)

date = datetime.datetime.strftime(datetime.datetime.now(), "%a_%b_%Y-%H_%M_%S")
filename = "student_routes_" + date + ".log"
logging.basicConfig(filename=filename, encoding="utf-8", level=logging.DEBUG)

student_bp = Blueprint("student", __name__)


@student_bp.route("/rooms/available", methods=["GET"])
def get_free_rooms():
    """This route is to receive requests for getting which rooms are currently available.
    The request should contain the room type whose one wants to know the availability.
    If the room type is not precised (or is invalid), the availability for all room types is returned.
    """
    room_type = None
    try:
        room_type = RoomTypeEnum[request.args.get("room_type")]
    except Exception as e:
        logging.error(f"An error occured {e}")

    if room_type:
        rooms = Room.query.filter(
            Room.room_type == room_type, Room.availability == RoomAvailability.AVAILABLE
        ).all()
    else:
        rooms = Room.query.filter(Room.availability == RoomAvailability.AVAILABLE).all()

    return jsonify([r.to_dict() for r in rooms]), 200


@student_bp.route("/rooms/description", methods=["GET"])
def consult_room_description():
    room_id = request.args.get("room_id")
    if room_id:
        room = Room.query.filter(id == room_id).head()
        description = room.to_dict["description"]
        return jsonify({"description": description}), 200
    else:
        return jsonify({}), 422


@student_bp.route("/rooms/apply", methods=["POST"])
def apply():
    room_id = request.args.get("room_id")
    if room_id:
        room=Room.query.filter(id==room_id).head().to_dict()
        if room['availability'] == RoomAvailability.AVAILABLE.name:

        else:
            return jsonify(), 200
    else:
        return jsonify({}), 422
    pass


@student_bp.route("/inquiry", methods=["POST"])
def send_inquiry_to_admin():
    pass
