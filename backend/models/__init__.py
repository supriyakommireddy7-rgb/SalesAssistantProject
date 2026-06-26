from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .admin import Admin
from .customer import Customer
from .email import Email
from .conversation import Conversation
from .knowledge_base import KnowledgeBase
from .notification import Notification
from .report import Report
from .activity_log import ActivityLog
