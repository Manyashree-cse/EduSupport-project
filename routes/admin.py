from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
# from app import db
from extensions import db
from models.ticket import Ticket
from models.user import User
from models.activity import Activity

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.before_request
@login_required
def check_admin():
    if current_user.role != "admin":
        abort(403)

@admin.route("/dashboard")
def dashboard():
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    stats = {
        "total": len(tickets),
        "open": sum(t.status in ("OPEN", "ASSIGNED") for t in tickets),
        "progress": sum(t.status == "IN_PROGRESS" for t in tickets),
        "pending": sum(t.status == "PENDING" for t in tickets),
        "resolved": sum(t.status in ("RESOLVED", "CLOSED") for t in tickets),
        "breached": sum(t.sla_breached for t in tickets),
    }
    staff_users = User.query.filter_by(role="staff").order_by(User.name).all()
    return render_template("admin/dashboard.html", tickets=tickets, stats=stats, staff_users=staff_users)

@admin.route("/ticket/<int:ticket_id>/assign", methods=["POST"])
def assign_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    staff_id = request.form.get("staff_id")

    staff_user = User.query.filter_by(id=staff_id, role="staff").first()
    if not staff_user:
        flash("Invalid staff member.", "danger")
        return redirect(url_for("admin.dashboard"))

    ticket.assigned_to = staff_user.id
    old_status = ticket.status
    if ticket.status == "OPEN":
        ticket.status = "ASSIGNED"

    db.session.add(Activity(
        ticket_id=ticket.id,
        user_id=current_user.id,
        action=f"Ticket assigned to {staff_user.name}",
        old_status=old_status,
        new_status=ticket.status
    ))
    db.session.commit()

    flash("Ticket assigned successfully.", "success")
    return redirect(url_for("admin.dashboard"))

@admin.route("/ticket/<int:ticket_id>")
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    activities = Activity.query.filter_by(ticket_id=ticket.id).order_by(Activity.created_at.desc()).all()
    staff_users = User.query.filter_by(role="staff").order_by(User.name).all()
    return render_template("admin/ticket_detail.html", ticket=ticket, activities=activities, staff_users=staff_users)

@admin.route("/create-staff", methods=["POST"])
def create_staff():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not name or not email or len(password) < 6:
        flash("Name, email and a 6+ character password are required.", "danger")
        return redirect(url_for("admin.dashboard"))

    if User.query.filter_by(email=email).first():
        flash("Email already exists.", "warning")
        return redirect(url_for("admin.dashboard"))

    user = User(name=name, email=email, role="staff")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    flash("Staff account created.", "success")
    return redirect(url_for("admin.dashboard"))
