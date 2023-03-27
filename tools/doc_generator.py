from os import listdir
import yaml
import random

class Problem:
    def __init__(self, id) -> None:
        self.id = id
        self.config_file = f"problems/{self.id}/data.yaml"
        with open(self.config_file) as f:
            data = yaml.safe_load(f)
        self.data = data
        print(data)

    def build(self, is_force =  False):
        if "final" in self.data and self.data["final"] and not is_force:
            return
        # write README.md file
        if not "title" in self.data:
            raise Exception(f"Title in problem {self.data['id']} is not defined")
        
        print(self.data)
        options = self.data['options']
        answer = self.data['answer']
        random.shuffle(options)
        
        print(options)
        content = f"""\
<h1 align="center">
Problem {self.data['id']}: {self.data['title']}
</h1>

<p align="center">
<img src="{self.data['image']}" height="512"/>
</p>

<h3 align="center">
"""
        choices = ['A', 'B', 'C', 'D']
        for choice, item in zip(choices, options):
            if item['value'] == answer:
                result_url = "https://raw.githubusercontent.com/rain1024/math/main/assets/win0.png"
            else:
                result_url = "https://raw.githubusercontent.com/rain1024/math/main/assets/lose0.png"
            content += f"<span><a href=\"{result_url}\">{choice}. {item['value']}</a></span>"
            content += "&nbsp;&nbsp;&nbsp;&nbsp;\n"
            
        content += "</h3>"
        with open(f"problems/{self.id}/README.md", "w") as f:       
            f.write(content)
        self.data['final'] = True
    
    def save_config(self):
        print(self.data)
        with open(self.config_file, "w") as f:
            yaml.dump(self.data, f)

class Game:
    def __init__(self):
        # read all problems from problems folder
        folders = listdir("problems")
        self.problems = [Problem(id) for id in folders]
    
    def build_problems(self):
        for problem in self.problems:
            problem.build()
            problem.save_config()

if __name__ == '__main__':
    # game = Game()
    # game.build_problems()
    
    # get first arguement
    import sys
    print(sys.argv)
    is_force = False
    if(len(sys.argv) > 1):
        is_force = True
    problem = Problem("3")
    problem.build(is_force)
    problem.save_config()