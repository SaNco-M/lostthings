@app.post("/register", response_model=UserResponseSchema)
async def register(
    user_data: UserCreateSchema, engine: LostAndFound = Depends(get_engine)
):
    user = await engine.register_user(
        name=user_data.name, contact_info=user_data.contact_info
    )

    return user