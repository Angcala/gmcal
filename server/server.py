from sanic import Sanic, text

# give me a context place and make a factory for the app instantiation
app = Sanic("GMCal")

@app.get("/")
async def handler(request):
    return text("It's your GM Cal pal")

@app.get("/sessions/<name>")
async def sessions_handler(request, name):
    user = app.ctx.member_service.get_by_name(name)
    
    sessions = app.ctx.session_service.list_users_sessions(user)
    
    # TODO: make sessions json and figure out of this is the right response type
    return json(sessions)
