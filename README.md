# todoist-albert
Albert plugin to quickly add task to todoist

## setup
you have to copy the plugin inside your plugin folder
```bash
git clone https://github.com/aGenius05/todoist-albert.git $HOME/.local/share/albert/python/plugins/todoist/
```
once installed the command bar will ask you for your API token, paste it after the plugin keyboard(default id "todo ") `todo <token>`
## usage
```
todo <text> "<description>" #<project> @<labels> !!<priority> %<time>
```
you can add as many labels as you want but just one of all the other attributes. Time goes at the end.