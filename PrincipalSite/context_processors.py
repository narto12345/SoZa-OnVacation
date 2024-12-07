def custom_context(request):
    return {"is_authenticated": request.session.get("is_authenticated", False)}
