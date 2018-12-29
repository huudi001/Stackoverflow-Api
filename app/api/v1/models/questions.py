
QUESTIONS_LIST = []
import datetime
class Questions():
    def put(self, question_id, comment, date_posted,title):
        self.single_question = {}


        self.single_question['question_id'] = question_id
        self.single_question['title'] = title
        self.single_question['comment'] = comment
        self.single_question['date_posted'] = date_posted

        QUESTIONS_LIST.append(self.single_question)

        return {"message": "Question with title {} added successfully".format(title)}

    def get_single_question(self, question_id):
        question = [question for question in QUESTIONS_LIST if question['question_id'] == question_id]
        if not question:
            return {"message": "question does not exist"}
        return question

    def get_all_questions(self):
        if not QUESTIONS_LIST:
            return {"message": "there are no records in the record list"}
        return QUESTIONS_LIST

    def delete_question(self, question_id):
        question = self.get_single_question(question_id)
        QUESTIONS_LIST.remove(question)
