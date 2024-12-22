from albert import *

md_iid = "0.26"
md_version = "0.1"
md_name = "todoist"
md_description = "quickly add task to todoist"
md_url = "" # update github url
md_license = "MIT"
md_authors = "@aGenius05"
md_lib_dependencies = "todoist-api-python"


class Plugin(PluginInstance, TriggerQueryHandler):
    def __init__(self):
        PluginInstance.__init__(self)
        TriggerQueryHandler.__init__(
            self, self.id, self.name, self.description,
            defaultTrigger='todo '
        )

    def handleTriggerQuery(self, query):
        if not query.isValid:
            return
        results = []
        uid = os.getuid()
        for dir_entry in os.scandir("/proc"):
            try:
                if dir_entry.name.isdigit() and dir_entry.stat().st_uid == uid:
                    proc_command = (
                        open(os.path.join(dir_entry.path, "comm"), "r").read().strip()
                    )
                    if query.string in proc_command:
                        debug(proc_command)
                        proc_cmdline = (
                            open(os.path.join(dir_entry.path, "cmdline"), "r")
                            .read()
                            .strip()
                            .replace("\0", " ")
                        )
                        results.append(
                            StandardItem(
                                id="kill",
                                iconUrls=["xdg:process-stop"],
                                text=proc_command,
                                subtext=proc_cmdline,
                                actions=[
                                    Action(
                                        "terminate",
                                        "Terminate process",
                                        lambda pid=int(dir_entry.name): os.kill(
                                            pid, SIGTERM
                                        ),
                                    ),
                                    Action(
                                        "kill",
                                        "Kill process",
                                        lambda pid=int(dir_entry.name): os.kill(
                                            pid, SIGKILL
                                        ),
                                    ),
                                ],
                            )
                        )
            except FileNotFoundError:  # TOCTOU dirs may disappear
                continue
            except IOError:  # TOCTOU dirs may disappear
                continue
        query.add(results)
