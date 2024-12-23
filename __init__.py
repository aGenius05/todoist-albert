from albert import *

md_iid = "2.3"
md_version = "0.1"
md_name = "todoist"
md_description = "quickly add task to todoist"
md_url = "https://github.com/aGenius05/todoist-albert.git"
md_license = "MIT"
md_authors = "@aGenius05"
md_lib_dependencies = "todoist-api-python"

from todoist_api_python.api import TodoistAPI
import os

# TODO: make the extension do things
# TODO: make the extension do "add description"
# TODO: show help
# TODO: autocompletition for labels and projects
# TODO: create settings with API key and language
# TODO: send notification results

# {
#     "content":"string",
#     "description":"string",
#     "project_id":"string",
#     "labels":"array of strings",
#     "priority":"integer (1 to 4, 1 is normal, 4 is urgent)",
#     "due_string":"string",
#     "due_lang":"it"
# }

def push_item(str):
    os.system(f"echo {str} > ~/Desktop/test.txt") 
    return

class Plugin(PluginInstance, TriggerQueryHandler):
    def __init__(self):
        PluginInstance.__init__(self)
        TriggerQueryHandler.__init__(
            self, self.id, self.name, self.description,
            defaultTrigger='todo ',
            supportsFuzzyMatching=False
        )
        self.iconUrls = [f'file:{os.path.join(os.path.dirname(__file__), "todoist.svg")}']

    def handleTriggerQuery(self, query):
        query.add(StandardItem(
                id=self.id,
                iconUrls = self.iconUrls,
                text="add task",
                subtext="add this task to your todoist",
                actions = [
                    Action("submit", "send the task", lambda r=query.string.strip(): push_item(r)),
                    Action("add description", "add description and send the task", lambda r=query.string.strip(): push_item(r))
                ]
                )
        )