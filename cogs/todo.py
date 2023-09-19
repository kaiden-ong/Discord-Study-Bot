import discord
from discord.ext import commands
from discord.ui import Button, View

class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.todo_lists = {}
        self.completed_lists = {}

    # List of commands
    @commands.command(name='add', help='(ie. !add Math HW): Adds "Math HW" task ')
    async def add_task(self, ctx, *, task):
        user_id = ctx.author.id
        if user_id not in self.todo_lists:
            self.todo_lists[user_id] = []
            self.completed_lists[user_id] = []
        self.todo_lists[user_id].append(task)
        print(f'{self.todo_lists}!')
        await ctx.send(f'Task "{task}" added successfully!')
    
    @commands.command(name='todo', help='(ie. !todo): View todo list')
    async def view_todo(self, ctx):
        user_id = ctx.author.id
        if user_id not in self.todo_lists:
            await ctx.send("You haven't created any tasks yet!")
            return

        user_list = self.todo_lists.get(user_id, [])
        indexed_list = self.__print_todo(user_list)
        await ctx.send(indexed_list)

    @commands.command(name='completed', help='(ie. !completed): View completed tasks')
    async def view_completed(self, ctx):
        user_id = ctx.author.id
        if user_id not in self.completed_lists:
            await ctx.send("You haven't completed any tasks yet!")
            return

        user_list = self.completed_lists.get(user_id, [])
        indexed_list = self.__print_completed(user_list)
        await ctx.send(indexed_list)

    @commands.command(name='view', help='(ie. !view): View todo and completed lists')
    async def view_lists(self, ctx):
        user_id = ctx.author.id
        if user_id not in self.completed_lists:
            await ctx.send("You haven't created or completed any tasks yet!")
            return
        
        indexed_lists = self.__print_both(user_id)
        await ctx.send(indexed_lists)

    @commands.command(name='remove', help='(ie. !remove 1): Removes task number 1 from todo list ')
    async def remove_task(self, ctx, *, task_index: int):
        user_id = ctx.author.id
        user_list = self.todo_lists.get(user_id, [])
        if user_id not in self.todo_lists:
            await ctx.send("You haven't created any tasks yet!")
        elif task_index < 1 or task_index > len(user_list):
            await ctx.send("Invalid task index!")
        else:
            removed_task = user_list.pop(task_index - 1)
            indexed_list = f'Task "{removed_task}" removed successfully!\n' + self.__print_todo(user_list)
            await ctx.channel.send(indexed_list)

    @commands.command(name='checkoff', help='(ie. !checkoff 1): Moves task 1 from todo to completed')
    async def checkoff_task(self, ctx, *, task_index: int):
        user_id = ctx.author.id
        user_list = self.todo_lists.get(user_id, [])
        if task_index < 1 or task_index > len(user_list):
                await ctx.send("Invalid task index!")
                return
    
        # await ctx.send(f"Are you sure you are done with {message.content}?")
        completed_task = user_list.pop(task_index - 1)
        self.completed_lists[user_id].append(completed_task)
        indexed_list = self.__print_both(user_id)
        await ctx.send(indexed_list)

    @commands.command(name='reset', help='(ie. !reset): Reset both lists')
    async def reset_lists(self, ctx):
        user_id = ctx.author.id
        if user_id not in self.todo_lists or (len(self.todo_lists[user_id]) == 0 and len(self.completed_lists[user_id]) == 0):
            await ctx.send("You haven't completed or created any tasks yet")
            return
        
        
        confirm_button = discord.ui.Button(style=discord.ButtonStyle.green, label="Confirm")
        cancel_button = discord.ui.Button(style=discord.ButtonStyle.red, label="Cancel")

        view = View()
        view.add_item(confirm_button)
        view.add_item(cancel_button)

        await ctx.send("Are you sure you want to reset your lists?", view=view) 

        async def confirm_button_callback(interaction):
            await interaction.response.edit_message(content="Reset confirmed! Todo and Completed lists have been reset.", view=None)
            self.todo_lists.pop(user_id, None)
            self.completed_lists.pop(user_id, None)
        async def cancel_button_callback(interaction):
            await interaction.response.edit_message(content="Reset canceled!", view=None)
        confirm_button.callback = confirm_button_callback
        cancel_button.callback = cancel_button_callback

    # Private methods
    def __print_todo(self, list):
        indexed_list = "```Todo List:\n" + "\n".join(f"{i + 1}: {task.capitalize()}" for i, task in enumerate(list)) + "```"
        if len(list) == 0:
            indexed_list = "```No tasks right now!```"
        return indexed_list
    
    def __print_completed(self, list):
        indexed_list = "```Completed:\n" + "\n".join(f"{i + 1}: {task.capitalize()}" for i, task in enumerate(list)) + "```"
        if len(list) == 0:
            indexed_list = "```Finish some tasks to see them here!```"
        return indexed_list
    
    def __print_both(self, user_id):
        todo_list = self.todo_lists.get(user_id, [])
        completed_list = self.completed_lists.get(user_id, [])
        return self.__print_todo(todo_list) + self.__print_completed(completed_list)

async def setup(bot):
    await bot.add_cog(Todo(bot))