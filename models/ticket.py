# from app import db
from extensions import db
from datetime import datetime, timedelta

class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=False, default="MEDIUM")
    status = db.Column(db.String(30), nullable=False, default="OPEN")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

    student = db.relationship("User", foreign_keys=[student_id])
    assignee = db.relationship("User", foreign_keys=[assigned_to])
    category = db.relationship("Category")

    @property
    def age_days(self):
        return max(0, (datetime.utcnow() - self.created_at).days)

    @property
    def sla_hours(self):
        return {"LOW": 120, "MEDIUM": 72, "HIGH": 24, "URGENT": 4}.get(self.priority, 72)

    @property
    def sla_deadline(self):
        return self.created_at + timedelta(hours=self.sla_hours)

    @property
    def sla_breached(self):
        if self.status in ("RESOLVED", "CLOSED"):
            return False
        return datetime.utcnow() > self.sla_deadline

    @property
    def age_text(self):
        seconds = max(0, int((datetime.utcnow() - self.created_at).total_seconds()))
        days, rem = divmod(seconds, 86400)
        hours, _ = divmod(rem, 3600)
        if days:
            return f"{days}d {hours}h"
        return f"{hours}h"
