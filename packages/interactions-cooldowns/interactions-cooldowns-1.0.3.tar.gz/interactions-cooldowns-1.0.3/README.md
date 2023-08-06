# cooldowns
This is a quickstart and api docs for this module

## Quickstart
```python
import interactions
import interactions.ext.cooldown
guild_id = 0
token = ""
#create bot
bot = interactions.Client(token=token)
#create function on cooldown fail
async def error(ctx, t):
  await ctx.send(f"Wait {t} secconds")
#command
@bot.command(
    name="test",
    description="This is the first command I made!",
    scope=guild_id,
)
#define cooldown function and time of cooldown
@cooldown.cooldown(error, 10)
async def my_first_command(ctx: interactions.CommandContext):
  await ctx.send("Hi there!")
#start bot
bot.start()
```
## api
### cooldown.cooldown()
#### error
error function, leave `None` for placeholder
#### time
time of cooldown
#### _clean_timers
cleans all timers
