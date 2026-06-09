from flask import Blueprint, jsonify, request
from models.Room import Room
from models.Application import Application, ApplicationStatus
from models import db
from models.Student import Student
from models.Admin import Admin

import logging
import datetime

admin_bp = Blueprint("admin", __name__)
