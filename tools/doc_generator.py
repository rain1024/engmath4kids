from os import listdir
import yaml
import random
import re

class Problem:
    def __init__(self, id) -> None:
        self.id = id
        self.config_file = f"problems/{self.id}/data.yaml"
        with open(self.config_file) as f:
            data = yaml.safe_load(f)
        self.data = data

    def build(self, is_force =  False):
        if "final" in self.data and self.data["final"] and not is_force:
            return
        # write README.md file
        if not "title" in self.data:
            raise Exception(f"Title in problem {self.id} is not defined")

        if not "image" in self.data:
            raise Exception(f"Image in problem {self.id} is not defined")
        
        options = self.data['options']
        answer = self.data['answer']
        random.shuffle(options)
        
        content = f"""\
<h1 align="center">
Problem {self.data['id']}: {self.data['title']}
</h1>

<p align="center">
<img src="{self.data['image']}" height="512"/>
</p>

<h3 align="center">\
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
        print(f"Problems built: {len(self.problems)}")
    
    def build_readme(self):
        # read game data
        with open("game_data.yaml") as f:
            topics = yaml.safe_load(f)

        print("Build readme")
        with open("README.md") as f:
            content = f.read()
            # find the start and end of the table
        # replace <!-- BEGIN MATH PROBLEMS --> ... <!-- END MATH PROBLEMS -->
        # with the new table
        match = re.compile(r"<!-- BEGIN MATH PROBLEMS -->.*<!-- END MATH PROBLEMS -->", re.MULTILINE | re.DOTALL)
        text = f"<!-- BEGIN MATH PROBLEMS -->\n\n"

        for topic in topics:
            text += f"## {topic['name']}\n\n"
            for problem in self.problems:
                tags = problem.data['tags'].split(',')
                if topic['id'] in tags:
                    text += f"* [{problem.data['id']}. {problem.data['title']}](problems/{problem.id})\n"
        text += f"\n<!-- END MATH PROBLEMS -->"

        content = re.sub(match, text, content)
        with open("README.md", "w") as f:
            f.write(content)

    def build_game(self):
        self.build_problems()
        self.build_readme()

if __name__ == '__main__':
    import sys
    is_force = False
    if(len(sys.argv) > 1):
        is_force = True
    game = Game()
    game.build_game()