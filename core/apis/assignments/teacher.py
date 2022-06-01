from marshmallow.exceptions import ValidationError
from flask import Blueprint,abort
from core.libs.exceptions import FyleError
from core import db
from core.libs import helpers, assertions
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, GradeEnum

from core.apis.decorators import Principal
from .schema import AssignmentSchema, AssignmentSubmitSchema,AssignmentGradeSchema
from core.models.assignments import Assignment, AssignmentStateEnum
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignments(p,incoming_payload):
    """Grading of assignments by teacher"""
    assignment = AssignmentGradeSchema().load(incoming_payload)
    valid_grade = False
    if assignment.grade not in [GradeEnum.A,GradeEnum.B,GradeEnum.C,GradeEnum.D,'A','B','C','D']:
        raise ValidationError('This is a bad grade')
    assignment = Assignment.get_by_id(assignment.id)
    if assignment not in Assignment.query.all():
        assertions.base_assert(404,'assignment does not exists')
    assertions.assert_valid(assignment.state == AssignmentStateEnum.SUBMITTED,'only a submitted assignment can be graded')
    assertions.assert_valid(assignment.teacher_id == p.teacher_id, 'This assignment belongs to some other teacher')
    assertions.assert_valid(assignment.content != "",'Empty Assignment will not be graded')
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)
