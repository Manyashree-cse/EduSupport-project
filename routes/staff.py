from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
# from app import db
from extensions import db
from models.ticket import Ticket
from models.comment import Comment
from models.activity import Activity

staff = Blueprint("staff", __name__, url_prefix="/staff")

@staff.before_request
@login_required
def check_staff():
    if current_user.role not in ("staff", "admin"):
        abort(403)

@staff.route("/dashboard")
def dashboard():
    if current_user.role == "admin":
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    else:
        tickets = Ticket.query.filter_by(assigned_to=current_user.id).order_by(Ticket.created_at.desc()).all()

    return render_template("staff/dashboard.html", tickets=tickets)

@staff.route("/ticket/<int:ticket_id>")
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if current_user.role == "staff" and ticket.assigned_to != current_user.id:
        abort(403)

    activities = Activity.query.filter_by(ticket_id=ticket.id).order_by(Activity.created_at.desc()).all()
    return render_template("staff/ticket_detail.html", ticket=ticket, activities=activities)

@staff.route("/ticket/<int:ticket_id>/update", methods=["POST"])
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if current_user.role == "staff" and ticket.assigned_to != current_user.id:
        abort(403)

    new_status = request.form.get("status")
    allowed = ("ASSIGNED", "IN_PROGRESS", "PENDING", "RESOLVED")

    if new_status not in allowed:
        flash("Invalid status.", "danger")
        return redirect(url_for("staff.ticket_detail", ticket_id=ticket.id))

    old_status = ticket.status
    ticket.status = new_status

    if new_status == "RESOLVED":
        from datetime import datetime
        ticket.resolved_at = datetime.utcnow()

    db.session.add(Activity(
        ticket_id=ticket.id,
        user_id=current_user.id,
        action=f"Status changed from {old_status} to {new_status}",
        old_status=old_status,
        new_status=new_status
    ))

    comment = request.form.get("comment", "").strip()
    if comment:
        db.session.add(Comment(ticket_id=ticket.id, user_id=current_user.id, comment=comment))

    db.session.commit()
    flash("Ticket updated.", "success")
    return redirect(url_for("staff.ticket_detail", ticket_id=ticket.id))
