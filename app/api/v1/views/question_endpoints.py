from flask import request, jsonify,  Blueprint
from ..models import questions
from ..models.questions import QUESTIONS_LIST


question = Blueprint('question', __name__, url_prefix='/api/v1')

Question = questions.Questions()

@question.route('/questions', methods=['POST'])
def post_question():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"}), 400
    question_id = len(QUESTIONS_LIST) + 1
    title = data.get('title')
    comment = data.get('comment')
    date_posted = data.get('date_posted')
    question_info = [title, comment, date_posted]


    for i in question_info:
        if i is None or not i:
            return jsonify({"message": "Required fields are missing"}), 206

    response = jsonify(Question.put(question_id, title, comment, date_posted))
    response.status_code = 200

    return response
@question.route('/questions', methods=['GET'])
def all_questions():
    response = jsonify(Question.get_all_questions())
    response.status_code = 200
    return response

@question.route('/questions<int:question_id>', methods=['GET'])
def get_one_question(question_id):
    response = jsonify(Question.get_single_question(question_id))
    response.status_code = 200
    return response

@question.route('/questions<int:question_id>', methods=['DELETE'])
def remove_question(question_id):
    response = jsonify(Question.delete_question(question_id))
    response.status_code = 200

    return response
