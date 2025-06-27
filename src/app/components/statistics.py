try:
    from app.components.stackexchange import StackExchangeClient ## if ran as a module from src
except ModuleNotFoundError:
    from stackexchange import StackExchangeClient # if ran as a script

class StackStatsCalculator:
    def __init__(self, answers = None):
        self.answers = answers
        self.comments = []
        self.is_computed = False
        self.stackexchange_client = StackExchangeClient()

    def compute_top_answers_comment_count(self) -> dict:
        self.top_10_answers = sorted(self.answers, key = lambda x: x['score'], reverse=True)[:10]
        answer_ids = [answer['answer_id'] for answer in self.top_10_answers]
        results = {str(id): 0 for id in answer_ids}
        self.comments = self.stackexchange_client.get_comments(answer_ids)
        if 'error' in self.comments:
            raise Exception("Error fetching comments: ", self.comments)
            
        for comment in self.comments:
            answer_id = str(comment['post_id'])
            results[answer_id] = results.get(answer_id, 0) + 1
        return {
            "top_ten_answers_comment_count": results
        }

    def compute_aggregates(self) -> dict:
        """
        Computes statistics for the provided answers.
        - Calculates the total number of accepted answers.
        - Computes the average score of accepted answers.
        - Determines the average answer count per question.
        """
        self.counter_of_accepted_answers = 0
        self.counter_of_not_accepted_answers = 0
        self.sum_accepted_scores = 0.0
        self.distinct_question_ids = set()

        for answer in self.answers:
            question_id = answer.get('question_id')
            is_accepted = answer.get('is_accepted', False)
            score = float(answer.get('score', 0))

            if question_id:
                self.distinct_question_ids.add(question_id)

            if is_accepted:
                self.counter_of_accepted_answers += 1
                self.sum_accepted_scores += score
            else:
                self.counter_of_not_accepted_answers += 1

        self.total_questions = len(self.distinct_question_ids)
        self.total_answers = self.counter_of_accepted_answers + self.counter_of_not_accepted_answers

        self.avg_score_accepted_answers = (
            round(self.sum_accepted_scores / self.counter_of_accepted_answers, 3)
            if self.counter_of_accepted_answers > 0
            else 0.0
        )
        self.avg_answer_count_per_question = (
            round(self.total_answers / self.total_questions, 3)
            if self.total_questions > 0
            else 0.0
        )
        return {
            "total_accepted_answers": self.counter_of_accepted_answers,
            "accepted_answers_average_score": self.avg_score_accepted_answers,
            "average_answers_per_question": self.avg_answer_count_per_question,
        }

    def compute(self) -> dict:
        """
        Combines the results of `compute_top_answers_comment_count` and `compute_aggregates`
        into one unified dictionary.
        """
        top_answers_comments = self.compute_top_answers_comment_count()
        aggregates = self.compute_aggregates()
        self.is_computed = True
        return {**aggregates, **top_answers_comments}

    def __repr__(self):
        "Returns distributed measures"
        if not self.is_computed:
            raise Exception("Not computed")
        return {
            "total_answers": self.total_answers,
            "total_questions": self.total_questions,
            "total_accepted_answers": self.counter_of_accepted_answers,
            "total_not_accepted_answers": self.counter_of_not_accepted_answers,
            "sum_accepted_scores": self.sum_accepted_scores,

        }