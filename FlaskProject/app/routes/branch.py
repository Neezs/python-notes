from flask import Blueprint, render_template, request, redirect, url_for, g
from flask import flash

bp = Blueprint('branch', __name__, url_prefix='/branches')

@bp.route('/')
def list_branches():
    g.cursor.execute("SELECT * FROM branches")
    branches = g.cursor.fetchall()
    return render_template('branch/list.html', branches=branches)

@bp.route('/create', methods=['GET', 'POST'])
def create_branch():
    if request.method == 'POST':
        nom = request.form['nom']

        g.cursor.execute("""
            INSERT INTO branches (nom)
            VALUES (%s)
        """, (nom,))
        g.db.commit()
        flash("Apprentice created successfully!")
        return redirect(url_for('branch.list_branches'))

    return render_template('branch/create.html')

@bp.route('/edit/<int:id_branche>', methods=['GET', 'POST'])
def edit_branch(id_branche):
    if request.method == 'POST':
        nom = request.form['nom']

        g.cursor.execute("""
            UPDATE branches
            SET nom = %s
            WHERE id_branche = %s
        """, (nom, id_branche))
        g.db.commit()
        flash("Apprentice updated successfully!")
        return redirect(url_for('branch.list_branches'))

    g.cursor.execute("SELECT * FROM branches WHERE id_branche = %s", (id_branche,))
    branch = g.cursor.fetchone()

    return render_template('branch/edit.html', branch=branch)

@bp.route('/delete/<int:id_branche>', methods=['GET', 'POST'])
def delete_branch(id_branche):
    if request.method == 'POST':
        # Delete any grades that use this branch first
        g.cursor.execute("DELETE FROM notes WHERE id_branche = %s", (id_branche,))
        # Then delete the branch
        g.cursor.execute("DELETE FROM branches WHERE id_branche = %s", (id_branche,))
        g.db.commit()
        flash("Apprentice deleted successfully!")
        return redirect(url_for('branch.list_branches'))

    g.cursor.execute("SELECT * FROM branches WHERE id_branche = %s", (id_branche,))
    branch = g.cursor.fetchone()

    return render_template('branch/delete.html', branch=branch)
