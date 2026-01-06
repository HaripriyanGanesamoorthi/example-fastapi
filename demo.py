# @app.post("/post",status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     try:
#         cursor.execute(
#             """INSERT INTO posts (title,content,published)
#             VALUES (%s, %s, %s)
#             RETURNING * """,
#             (post.title,post.content,post.published)
#         )
#         new_post=cursor.fetchone()
#         conn.commit()
#         return {"data" : new_post}
#     except Exception as e:
#         conn.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
    
# @app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def create_user(user : schemas.Usercreate, db:Session = Depends(get_db)):
#     #just to debug and coofirm password details

#     print("Password before hshing:",user.password)
#     print("Password type:", type(user.password))
#     print("password length:",len(str(user.password)))

#     #hash the password - user.password
#     password_str = str(user.password)[:72]
#     hashed_password = pwd_context.hash(password_str)
#     # user.password = hashed_password
    
#     new_user = models.User(email=user.email, password=hashed_password)
#     # new_user.password = hashed_password
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user