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
import re
from time import sleep

# usage: todo <text> "<description>" #<project> @<labels> !!<priority> %<time>

class Plugin(PluginInstance, TriggerQueryHandler):
    def __init__(self):
        PluginInstance.__init__(self)
        TriggerQueryHandler.__init__(
            self, self.id, self.name, self.description,
            defaultTrigger='todo ',
            supportsFuzzyMatching=False
        )
        self.iconUrls = [f'file:{os.path.join(os.path.dirname(__file__), "todoist.svg")}']
        self._token = self.readConfig('todoist-token', str)
        if self._token is not None:
            self.api = TodoistAPI(self._token)
        self._language = self.readConfig('todoist-langauge', str)
        self.update_data()

    def update_token(self, token):
        self._token = token
        self.writeConfig('todoist-token', token)

    def update_language(self, language):
        self._language = language
        self.writeConfig('todoist-language', language)

    def configWidget(self):
        return [{'type':'label', 'text':'ATTENTION: you have to setup your API token in the command bar. You can later modify both the token and the language using the Alt key on the add task prompt.'},
                {'type':'label', 'text':'usage: todo <text> "<description>" #<project> @<labels> !!<priority> %<time>'},
                {'type':'label', 'text':'text, description, project, priority and time must be unique but you can add as many labels as you want. The time goes at the end of the query.'}]

    def update_data(self):
        try:
            self.projects_obj = self.api.get_projects()
            self.projects = [[],[]]
            self.projects[0] = [x.id for x in self.projects_obj]
            self.projects[1] = [x.name for x in self.projects_obj]
        except Exception as error:
            warning(error)
        try:
            self.labels_obj = self.api.get_labels()
            self.labels = []
            self.labels = [x.name for x in self.labels_obj]
        except Exception as error:
            warning(error)

    def push_item(self, todo_string):
        self.update_data()
        # description
        try:
            descr = re.findall("\".+\"", todo_string).pop().lstrip("\"").rstrip("\"")
        except:
            descr = ""
        # project
        try:
            project = re.findall("#\\w+", todo_string).pop().lstrip("#")
        except:
            project = ""
        task_labels = [x.lstrip("@") for x in re.findall("@\\w+", todo_string)]
        # priority
        try:
            prior = 5 - int(re.findall("!!\\d", todo_string)[0].lstrip("!!"))
        except:
            prior = 1
        # date and time
        try:
            time = re.findall("%.+$", todo_string).pop().lstrip("%")        
        except:
            time = ""
        # title
        text = todo_string[:len(todo_string)-(len(descr+project+time+''.join(task_labels)) +
                                              (1 if project != "" else 0 ) +
                                              (2 if descr != "" else 0) +
                                              len(task_labels) +
                                              (3 if prior != 1 else 0) +
                                              (1 if time != "" else 0) +
                                              todo_string.rstrip("%"+time).replace("\"" + descr + "\"", "").count(" "))].rstrip(" ")
        # check if project exists
        if project not in self.projects[1] and project != "":
            try:
                self.api.add_project(name=project)
                self.update_data()
            except Exception as error:
                warning(error)
        # check if labels exist
        for label in task_labels:
            if label not in self.labels:
                try:
                    self.api.add_label(name=label)
                except Exception as error:
                    warning(error)
        # send the task to your todoist
        try:
            if project == "":
                project = "Inbox"
            self.api.add_task(
                content=text,
                description=descr,
                project_id=self.projects[0][self.projects[1].index(project)],
                labels=task_labels,
                priority=prior,
                due_string=time,
                due_lang=self._language,
            )
            notification = Notification("Success", "Your task has been succesfully sent to your todoist")
            notification.send()
            sleep(1)
            notification.dismiss()
        except Exception as error:
            notification = Notification("Error", "something went wrong. You connection or the task's syntax could have been wrong. Please retry")
            notification.send()
            sleep(1)
            notification.dismiss()
            warning(error)

    def handleTriggerQuery(self, query):
        if not query.isValid:
            return
        if self._token is None:
            query.add(StandardItem(
                id=self.id,
                iconUrls = [f'file:{os.path.join(os.path.dirname(__file__), 'settings.svg')}'],
                text="register API token",
                subtext="store your API token",
                actions =[
                    Action("token", "store the token", lambda r=query.string.strip(): self.update_token(r))
                ]
            ))
        else:
            query.add(StandardItem(
                id=self.id,
                iconUrls = self.iconUrls,
                text="add task",
                subtext="add this task to your todoist",
                actions = [
                    Action("submit", "send the task", lambda r=query.string.strip(): self.push_item(r)),
                    Action("token", "change the token", lambda r=query.string.strip(): self.update_token(r)),
                    Action("language", "change language", lambda r=query.string.strip(): self.update_language(r))
                ]
            ))