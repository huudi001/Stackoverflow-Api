from flask import Flask, request, jsonify, make_response , Blueprint
from ..models import questions
from ..models.questions import QUESTIONS_LIST


question = Blueprint('question', __name__, url_prefix='/api/v1/question')

Question = questions.Questions()

@question.route('/questions', methods=['POST'])
def post_question():
    data = request.get_json()
    if not data:
         return jsonify({"message: Fields cannot be empty"}), 400
    question_id = len(QUESTIONS_LIST) + 1
    title = data.get('title')
    comment = data.get('comment')
    date_posted = data.get('date_posted')

    response = jsonify(Question.put(question_id, title, comment, date_posted))
    response.status_code = 200

    return response
