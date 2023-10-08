from fastapi import FastAPI

from prisma import Prisma
from prisma.models import Post, User
from prisma.partials import PostWithoutRelations, UserWithoutRelations
from prisma.types import UserUpdateInput

app = FastAPI()
prisma = Prisma(auto_register=True)


@app.on_event("startup")
async def startup() -> None:
    if not prisma.is_connected():
        await prisma.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    if prisma.is_connected():
        await prisma.disconnect()


@app.get(
    "/users",
    response_model=list[UserWithoutRelations],
)
async def list_users(take: int = 10) -> list[User]:
    return await User.prisma().find_many(take=take)


@app.post(
    "/users",
    response_model=UserWithoutRelations,
)
async def create_user(name: str, email: str | None = None) -> User:
    return await User.prisma().create({"name": name, "email": email})


@app.put(
    "/users/{user_id}",
    response_model=UserWithoutRelations,
)
async def update_user(
    user_id: str,
    name: str | None = None,
    email: str | None = None,
) -> User | None:
    data: UserUpdateInput = {}

    if name is not None:
        data["name"] = name

    if email is not None:
        data["email"] = email

    return await User.prisma().update(
        where={
            "id": user_id,
        },
        data=data,
    )


@app.delete(
    "/users/{user_id}",
    response_model=User,
)
async def delete_user(user_id: str) -> User | None:
    return await User.prisma().delete(
        where={
            "id": user_id,
        },
        include={
            "posts": True,
        },
    )


@app.get(
    "/users/{user_id}",
    response_model=UserWithoutRelations,
)
async def get_user(user_id: str) -> User | None:
    return await User.prisma().find_unique(
        where={
            "id": user_id,
        },
    )


@app.get(
    "/users/{user_id}/posts",
    response_model=list[PostWithoutRelations],
)
async def get_user_posts(user_id: str) -> list[Post]:
    user = await User.prisma().find_unique(
        where={
            "id": user_id,
        },
        include={
            "posts": True,
        },
    )
    if user is not None:
        # we are including the posts, so they will never be None
        assert user.posts is not None
        return user.posts
    return []


@app.post(
    "/users/{user_id}/posts",
    response_model=PostWithoutRelations,
)
async def create_post(user_id: str, title: str, published: bool) -> Post:
    return await Post.prisma().create(
        data={
            "title": title,
            "published": published,
            "author": {
                "connect": {
                    "id": user_id,
                },
            },
        }
    )


@app.get(
    "/posts",
    response_model=list[PostWithoutRelations],
)
async def list_posts(take: int = 10) -> list[Post]:
    return await Post.prisma().find_many(take=take)


@app.get(
    "/posts/{post_id}",
    response_model=Post,
)
async def get_post(post_id: str) -> Post | None:
    return await Post.prisma().find_unique(
        where={
            "id": post_id,
        },
        include={
            "author": True,
        },
    )


@app.delete(
    "/posts/{post_id}",
    response_model=Post,
)
async def delete_post(post_id: str) -> Post | None:
    return await Post.prisma().delete(
        where={
            "id": post_id,
        },
        include={
            "author": True,
        },
    )
