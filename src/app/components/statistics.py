try:
    from app.components.stackexchange import StackExchangeClient ## if ran as a module from src
except ModuleNotFoundError:
    from stackexchange import StackExchangeClient # if ran as a script

class StackStatsCalculator:
    def __init__(self, answers):
        self.answers = answers
        self.comments = []
        self.stackexchange_client = StackExchangeClient()

    def compute(self):
        
        self.counter_of_accepted_answers = 0
        self.counter_of_not_accepted_answers = 0
        self.sum_accepted_scores = 0
        self.distinct_question_ids = set()
        for answer in self.answers:
            if answer.get('question_id') and answer.get('question_id') not in self.distinct_question_ids:
                self.distinct_question_ids.add(answer.get('question_id'))
            if answer.get('is_accepted'):
                self.counter_of_accepted_answers += 1
                self.sum_accepted_scores += float(answer.get('score', 0))
            else:
                self.counter_of_not_accepted_answers += 1
        self.avg_score_accepted_answers = self.sum_accepted_scores / self.counter_of_accepted_answers if self.counter_of_accepted_answers > 0 else 0
        self.avg_answer_count_per_question = (self.counter_of_accepted_answers + self.counter_of_not_accepted_answers) / len(self.distinct_question_ids) if len(self.distinct_question_ids) > 0 else 0
