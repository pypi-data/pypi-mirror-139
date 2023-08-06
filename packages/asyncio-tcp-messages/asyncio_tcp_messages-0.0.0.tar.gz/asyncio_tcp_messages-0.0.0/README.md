A library for developing applications with a message-based protocol on top of TCP based on asyncio.Opens the possibility of adding controllers that are responsible for specific commands, the ability to define and validate command arguments.

1. First, you need to create an object of the App class

   ```
   import asyncio

   from main import App

   app = App()

   #Your code

   if __name__ == '__main__':
       asyncio.run(app.run())

   ```
2. Examples of some simple tasks that our framework uses.

   ```
   @app.command(name='sum')
   async def custom_sum(arg1: int, arg2: int) -> str:
       return str(arg1 + arg2)


   @app.command()
   async def add_person(person: Person):
       people.append(person)


   @app.command()
   async def get_person(name: str) -> str:
       return '\n'.join(str(person) for person in people if person.name == name)

   ```
