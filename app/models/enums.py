import enum


class RoleEnum(str, enum.Enum):
    admin = "admin"
    editor = "editor"
    viewer = "viewer"


class NewsCategory(str, enum.Enum):
    news = "News"
    announcement = "Announcement"
    event = "Event"
    alert = "Alert"


class PostStatus(str, enum.Enum):
    draft = "Draft"
    published = "Published"
    archived = "Archived"
