from typing import Optional
from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi import Body
from pydantic import BaseModel

app = FastAPI()
#Post Model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

#List for dummy data posts  
posts: list[Post] = []

#Helper function to find post by id
def find_post(id):
    for p in posts:
        if id == p["post_id"]:
            return p

#Root route
@app.get('/')
def root():
    return {"message": "Konnichiwa! :D"}

#Create a post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post = post.model_dump()
    post["post_id"] = len(posts) + 1
    posts.append(post)
    return {"data": post}

#Get all posts
@app.get('/posts')
def get_posts():
    return {"posts": posts}

#Get post by id
@app.get('/posts/{post_id}')
def get_post(post_id: int):
    post = find_post(post_id)
    if post:
        return {"message": f'Post with id {post_id} found!', "post": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} could not be found :(")

#Delete a post
@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} does not exist :(")
    posts.remove(post)

#Update a post
@app.put('/posts/{post_id}')
def update_post(post_id: int, updated_post: Post):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} does not exist :(")
    updated_post = updated_post.model_dump()
    updated_post["post_id"] = post_id
    posts.insert(posts.index(post), updated_post)
    posts.remove(post)
    return {"message": f"Post with id {post_id} successfully updated!", "data": updated_post}