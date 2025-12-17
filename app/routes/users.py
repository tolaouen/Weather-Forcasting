from flask import Blueprint, url_for, redirect, render_template, flash, abort
from app.services.users import UserService
from app.forms.form_users import CreateUserForm, UpdateUserForm, ConfirmDeleteUserForm
from sqlalchemy.orm import Session
from app.database import get_db


users_router = Blueprint("users", __name__, url_prefix="/users")

#  Get all users route
@users_router.route("/", methods=["GET"])
def index(db: Session = get_db()):
    users = UserService.get_all(db)
    return render_template("users/index.html", users=users)

# Get User by ID route
@users_router.route("/<int:user_id>", methods=["GET"])
def detail(user_id: int, db: Session = get_db()):
    user = UserService.get_by_id(user_id, db)

    if not user:
        abort(404, description="User not found")

    return render_template("users/detail.html", user=user)

# Create User route
@users_router.route("/create", methods=["GET", "POST"])
def create(db: Session = get_db()):
    form = CreateUserForm()

    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data,
        }
        password = form.password.data   
        user = UserService.create(data, password, db)
        flash(f"User {user.username} created successfully!.", "success")
        return redirect(url_for("users.detail", user_id=user.id))
    return render_template("users/create.html", form=form)


# Update Users Route
@users_router.route("/<int:user_id>/edit", methods=["GET", "POST"])
def edit(user_id: int, db: Session = get_db()):

    user = UserService.get_by_id(user_id, db)
    if not user:
        abort(404, description="User not found")

    form = UpdateUserForm(original_user=user, obj=user)

    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data,
        }
        password = form.password.data or None
        UserService.update(user, data, password, db)
        flash(f"User {user.username} was updated succesfully!.", "success")
        return redirect(url_for("users.edit", user_id=user.id))
    return render_template("users/edit.html", form=form, user=user)

# Delete user confirm Route
@users_router.route("/<int:user_id>/delete", methods=["GET"])
def detete_confirm(user_id: int, db: Session = get_db()):
    user = UserService.get_by_id(user_id, db)
    if not user:
        abort(404, "User Not Found")

    form = ConfirmDeleteUserForm()
    return render_template("users/delete_confirm.html", user=user, form=form)       

# Delete user route
@users_router("/<int:user_id>/delete", methods=["POST"])
def delete(user_id: int, db: Session = get_db()):
    user = UserService.get_by_id(user_id, db)

    if not user:
        abort(404, "User not Found")

    UserService.delete(user)
    flash("User was delete succesfully!.", "success")
    return redirect(url_for("users.index"))