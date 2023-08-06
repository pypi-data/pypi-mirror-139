import time
from functools import wraps
class cooldown:
    def __init__(self, function, cal:"function"=None, cool:int=10):
        self.function = function
        self.js = {}
        self.cool = cool
        self.cal = cal
    def _clean_timers(self):
        jsondata = [obj for obj in self.js if time.time()- self.js[obj] >= self.cool]
        self.js = jsondata
    def data(self, ctx):
        js = self.js
        try:
            data = js[str(ctx.author.user.id)]
        except:
            t = time.time()
            js[str(ctx.author.user.id)] = t
            return (True, t)
        if time.time()-data >= self.cool:
            data = time.time()
            return (True, data)
        else:
            return (False, data)
    def __call__(self, tc):
        print(tc)
        func = tc
        @wraps(tc)
        async def new_func(ctx: "CommandContext", *args, **kwargs):
            # todo cooldown logic
            data = self.data(ctx)
            if data[0]:
                return await tc(ctx, *args, **kwargs)
            if self.cal:
                return await self.function(ctx, self.cool-(time.time()-data[1]))
            await ctx.send("This command is currently on cooldown")
            new_data = filter(lambda attr: attr not in dir(type(func)), dir(func))
            for new_attr in new_data:
                old_attr = getattr(func, new_attr)
                setattr(new_func, new_attr, old_attr)
        return new_func
