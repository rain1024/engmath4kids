import yaml
import re
from os import listdir
import random
import time


class Problem:
    def __init__(self, id) -> None:
        self.id = id
        self.config_file = f"problems/{self.id}/data.yaml"
        with open(self.config_file) as f:
            data = yaml.safe_load(f)
        self.data = data

    def build(self, is_force=False):
        if "final" in self.data and self.data["final"] and not is_force:
            return
        # write README.md file
        if "title" not in self.data:
            raise Exception(f"Title in problem {self.id} is not defined")

        if "image" not in self.data:
            raise Exception(f"Image in problem {self.id} is not defined")

        options = self.data['options']
        answer = self.data['answer']
        random.shuffle(options)

        content = f"""\
<h1 align="center">
Problem {self.data['id']}: {self.data['title']}
</h1>
"""
        if "description" in self.data:
            content += f"""
<h4 align="center">
{self.data['description']}
</h4>\n
"""
        content += f"""\
<p align="center">
<img src="{self.data['image']}" height="512"/>
</p>\n
"""
        content += '<h3 align="center">'
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
        folders = sorted([int(x) for x in listdir("problems")])
        self.problems = [Problem(id) for id in folders]

    def build_problems(self, **kwargs):
        is_force = kwargs.get('is_force', False)
        for problem in self.problems:
            problem.build(is_force)
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
        text = "<!-- BEGIN MATH PROBLEMS -->\n\n"

        for topic in topics:
            text += f"\n## {topic['name']}\n\n"
            for problem in self.problems:
                tags = problem.data['tags'].split(',')
                if topic['id'] in tags:
                    text += f"* [{problem.data['id']}. {problem.data['title']}](problems/{problem.id})\n"
        text += "\n<!-- END MATH PROBLEMS -->"

        content = re.sub(match, text, content)
        with open("README.md", "w") as f:
            f.write(content)

    def build_game(self, **kwargs):
        self.build_problems(**kwargs)
        self.build_readme()


class AudioLibrary:
    sounds = {
        "bewildered": "bg_cute_bewildered_bQfO4z_mQUI.mp3",
        "cutest_bunny": "bg_cute_cutest_bunny_UeKehu5DE0Y.mp3",
        "funny_cat": "bg_cute_funny_cat_1pGgn9rfGZU.mp3",
        "furry_friends": "bg_cute_furry_friends_79w0HiP0uA0.mp3",
        "happy_footsteps": "bg_cute_happy_footsteps_RYsDvuSd-OA.mp3",
        "hide_and_seek": "bg_cute_hide_and_seek_ktBjO98Zm6U.mp3",
        "lazy_morning_coffee": "bg_cute_lazy_morning_coffee_CQ7vfhjbQBQ.mp3",
        "pretty_things": "bg_cute_pretty_things_sSMosqueSuQ.mp3",
        "riding_the_pink": "bg_cute_riding_the_pink_bus_3co7k1od8X4.mp3",
        "cute": "cute_bg.mp3",
    }

    @staticmethod
    def get(sound_id):
        return AudioLibrary.sounds[sound_id]

    def get_random():
        timestamp = int(time.time()*1000.0)
        random.seed(timestamp)
        sounds = list(AudioLibrary.sounds.values())
        sound = random.choice(sounds)
        return sound
