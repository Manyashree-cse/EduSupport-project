from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
# from app import db
from extensions import db
from models.ticket import Ticket
from models.category import Category
from models.comment import Comment
from models.activity import Activity

student = Blueprint("student", __name__, url_prefix="/student")

@student.before_request
@login_required
def check_student():
    if current_user.role != "student":
        abort(403)

@student.route("/dashboard")
def dashboard():
    tickets = Ticket.query.filter_by(student_id=current_user.id).order_by(Ticket.created_at.desc()).all()
    stats = {
        "total": len(tickets),
        "open": sum(t.status in ("OPEN", "ASSIGNED") for t in tickets),
        "pending": sum(t.status == "PENDING" for t in tickets),
        "resolved": sum(t.status in ("RESOLVED", "CLOSED") for t in tickets),
    }
    return render_template("student/dashboard.html", tickets=tickets, stats=stats)

@student.route("/tickets")
def tickets():
    tickets = Ticket.query.filter_by(student_id=current_user.id).order_by(Ticket.created_at.desc()).all()
    return render_template("student/tickets.html", tickets=tickets)

@student.route("/ticket/create", methods=["GET", "POST"])
def create_ticket():
    categories = Category.query.order_by(Category.name).all()

    if request.method == "POST":
        category_id = request.form.get("category_id")
        subject = request.form.get("subject", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "MEDIUM").upper()

        if not category_id or not subject or not description:
            flash("Category, subject and description are required.", "danger")
            return render_template("student/create_ticket.html", categories=categories)

        if priority not in ("LOW", "MEDIUM", "HIGH", "URGENT"):
            priority = "MEDIUM"

        ticket = Ticket(
            student_id=current_user.id,
            category_id=int(category_id),
            subject=subject,
            description=description,
            priority=priority
        )
        db.session.add(ticket)
        db.session.flush()

        db.session.add(Activity(
            ticket_id=ticket.id,
            user_id=current_user.id,
            action="Ticket created",
            new_status="OPEN"
        ))
        db.session.commit()

        flash(f"Ticket #{ticket.id} created successfully.", "success")
        return redirect(url_for("student.ticket_detail", ticket_id=ticket.id))

    return render_template("student/create_ticket.html", categories=categories)

@student.route("/ticket/<int:ticket_id>")
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if ticket.student_id != current_user.id:
        abort(403)

    activities = Activity.query.filter_by(ticket_id=ticket.id).order_by(Activity.created_at.desc()).all()
    return render_template("student/ticket_detail.html", ticket=ticket, activities=activities)

@student.route("/ticket/<int:ticket_id>/comment", methods=["POST"])
def add_comment(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.student_id != current_user.id:
        abort(403)

    text = request.form.get("comment", "").strip()
    if not text:
        flash("Comment cannot be empty.", "danger")
    elif ticket.status == "CLOSED":
        flash("Closed tickets cannot receive new comments.", "warning")
    else:
        db.session.add(Comment(ticket_id=ticket.id, user_id=current_user.id, comment=text))
        db.session.commit()
        flash("Comment added.", "success")

    return redirect(url_for("student.ticket_detail", ticket_id=ticket.id))

@student.route("/ticket/<int:ticket_id>/close", methods=["POST"])
def close_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.student_id != current_user.id:
        abort(403)

    if ticket.status != "RESOLVED":
        flash("Only resolved tickets can be closed.", "warning")
        return redirect(url_for("student.ticket_detail", ticket_id=ticket.id))

    old = ticket.status
    ticket.status = "CLOSED"
    db.session.add(Activity(
        ticket_id=ticket.id,
        user_id=current_user.id,
        action="Student closed ticket",
        old_status=old,
        new_status="CLOSED"
    ))
    db.session.commit()
    flash("Ticket closed.", "success")
    return redirect(url_for("student.ticket_detail", ticket_id=ticket.id))
