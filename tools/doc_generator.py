from os import listdir
import yaml

class Problem:
    def __init__(self, id) -> None:
        self.id = id
        with open(f"problems/{self.id}/data.yaml") as f:
            data = yaml.safe_load(f)
        self.data = data
        print(data)

    def build(self):
        pass

class Game:
    def __init__(self):
        # read all problems from problems folder
        folders = listdir("problems")
        self.problems = [Problem(id) for id in folders]
    
    def build_problems(self):
        for problem in self.problems:
            problem.build()

if __name__ == '__main__':
    game = Game()
    game.build_problems()