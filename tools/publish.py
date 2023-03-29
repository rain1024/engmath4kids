from models import Game

def generate_plan(day):
    pass

if __name__ == '__main__':
    game = Game()
    problems = game.problems
    for problem in problems:
        if "age" not in problem.data:
            raise Exception(f"Problem {problem.id} is missing age field")
    
    print(problems)
    