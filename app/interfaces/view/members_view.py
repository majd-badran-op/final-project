from typing import Optional
from flask import abort, jsonify, request, Response
from flask.views import MethodView
from domain.entities.member_entity import Member

class MemberView(MethodView):
    ...
