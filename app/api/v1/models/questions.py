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
