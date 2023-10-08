from prisma.models import Post, User

User.create_partial(
    "UserWithoutRelations",
    exclude_relational_fields=True,
)
Post.create_partial(
    "PostWithoutRelations",
    exclude_relational_fields=True,
)
