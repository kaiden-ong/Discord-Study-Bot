import discord
import os
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv

load_dotenv()

class ConfirmCancelView(View):
    def __init__(self, task):
        super().__init__()
        self.task = task

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, custom_id="confirm_button")
    async def confirm_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_list = self.todo_lists.get(user_id, [])
        if self.task in user_list:
            user_list.remove(self.task)
            self.completed_lists.setdefault(user_id, []).append(self.task)
            await interaction.response.send_message(f"You confirmed that you are done with {self.task}!")
        else:
            await interaction.response.send_message(f"The task '{self.task}' doesn't exist in your Todo list.")

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, custom_id="cancel_button")
    async def cancel_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("You canceled the task completion.")

class MyClient(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.todo_lists = {}
        self.completed_lists = {}

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        user_id = message.author.id

        if (message.content.startswith('!add ')):
            if user_id not in self.todo_lists:
                self.todo_lists[user_id] = []
                self.completed_lists[user_id] = []
            self.todo_lists[user_id].append(message.content[len('!add'):].strip())
            print(f'{self.todo_lists}!')
            
        if (message.content.startswith('!todo')):
            user_list = self.todo_lists.get(user_id, [])
            if len(user_list) == 0:
                indexed_list = "You have completed all tasks for now!"
            else:
                indexed_list = "```" + "\n".join(f"{i + 1}: {task.capitalize()}" for i, task in enumerate(user_list)) + "```"
            await message.channel.send(indexed_list)

        if (message.content.startswith('!remove ')):
            if user_id not in self.todo_lists:
                await message.channel.send("You haven't created any tasks yet!")
            else:
                user_list = self.todo_lists.get(user_id, [])
                remove_index = int(message.content[len('!remove'):].strip()) - 1
                user_list.pop(remove_index)
                indexed_list = "```" + "\n".join(f"{i + 1}: {task.capitalize()}" for i, task in enumerate(user_list)) + "```"
                await message.channel.send(indexed_list)


        if (message.content.startswith('!checkoff ')):
            remove_index = int(message.content[len('!checkoff'):].strip()) - 1
            user_list = self.todo_lists.get(user_id, [])
            if remove_index < 0 or remove_index >= len(user_list):
                await message.channel.send("Invalid task index!")
            else:
                completed_task = user_list[remove_index]
                confirm_view = ConfirmCancelView(completed_task)
                confirm_message = await message.channel.send(f"Are you sure you are done with {completed_task}?", view=confirm_view)
                confirm_view.message = confirm_message
                confirm_view.task = completed_task


        if (message.content.startswith('!completed')):
            if user_id not in self.completed_lists:
                await message.channel.send("You haven't created any tasks yet!")
            elif len(self.completed_lists[user_id]) == 0:
                await message.channel.send("You haven't completed any tasks yet!")
            else:
                user_list = self.completed_lists.get(user_id, [])
                indexed_list = "```" + "\n".join(f"{i + 1}: {task.capitalize()}" for i, task in enumerate(user_list)) + "```"
                await message.channel.send(indexed_list)

        if (message.content.startswith('!view')):
            if user_id not in self.todo_lists:
                await message.channel.send("You haven't created any tasks yet!")
            else:
                todo = self.todo_lists.get(user_id, [])
                if len(todo) == 0:
                    indexed_todo = "You have no tasks to do right now!"
                else:
                    indexed_todo = "\n".join(f"{i + 1}: {task.capitalize()}" for i, task in enumerate(todo))
                completed = self.completed_lists.get(user_id, [])
                if len(completed) == 0:
                    indexed_completed = "Finish some tasks first to see them here!"
                else:
                    indexed_completed = "\n".join(f"{i + 1}: {task.capitalize()}" for i, task in enumerate(completed))
                combined = "```" + "Todo:\n" + indexed_todo + "\nCompleted:\n" + indexed_completed + "```"
                await message.channel.send(combined)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('TOKEN'))

        # if (message.content.startswith('!checkoff ')):
        #     await message.channel.send(f"Are you sure you are done with {message.content}?")
        #     user_list = self.todo_lists.get(user_id, [])
        #     remove_index = int(message.content[len('!checkoff'):].strip()) - 1
        #     completed_task = user_list.pop(remove_index)
        #     self.completed_lists[user_id].append(completed_task)
        #     if len(user_list) == 0:
        #         await message.channel.send("You have completed all tasks for now!")
        #     else:
        #         indexed_list = "```" + "\n".join(f"{i + 1}: {task.capitalize()}" for i, task in enumerate(user_list)) + "```"
        #         await message.channel.send(indexed_list)