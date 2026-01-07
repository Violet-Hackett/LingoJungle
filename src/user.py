import json
import state

class User:
    def __init__(self, unlocked_lesson_indices: list[int], knowledge: int):
        self.unlocked_lesson_indices = unlocked_lesson_indices
        self.knowledge = knowledge

    @staticmethod
    def load_user() -> ...:
        with open(state.USER_DATA_FP) as user_data_file:
            user_data = json.load(user_data_file) 
            unlocked_lesson_indices = user_data['unlocked_lesson_indices']
            knowledge = user_data['knowledge']
            return User(unlocked_lesson_indices, knowledge)
            
    def save_data(self):
        with open(state.USER_DATA_FP, "w") as user_data_file:
            user_data = self.__dict__
            json.dump(user_data, user_data_file)

USER: User = User.load_user()