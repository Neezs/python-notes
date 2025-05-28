from flask import Blueprint, render_template, request, redirect, url_for, g
from flask import flash

bp = Blueprint('grade', __name__, url_prefix='/grades')

@bp.route('/')
def list_grades():
    g.cursor.execute("""
        SELECT n.id_note, n.valeur, p.prenom AS apprenti_prenom, b.nom AS branche_nom, s.valeur AS semestre
        FROM notes n
        JOIN apprentis a ON n.id_apprenti = a.id_apprenti
        JOIN personnes p ON a.id_apprenti = p.id_personne
        JOIN branches b ON n.id_branche = b.id_branche
        JOIN semestres s ON n.id_semestre = s.id_semestre

    """)
    grades = g.cursor.fetchall()
    return render_template('grade/list.html', grades=grades)

@bp.route('/create', methods=['GET', 'POST'])
def create_grade():
    if request.method == 'POST':
        id_apprenti = request.form['id_apprenti']
        id_branche = request.form['id_branche']
        id_semestre = request.form['id_semestre']
        valeur = request.form['valeur']

        g.cursor.execute("""
            INSERT INTO notes (valeur, id_apprenti, id_semestre, id_branche)
            VALUES (%s, %s, %s, %s)
        """, (valeur, id_apprenti, id_semestre, id_branche))
        g.db.commit()
        flash("Apprentice created successfully!")
        return redirect(url_for('grade.list_grades'))

    # Load dropdown options
    g.cursor.execute("""
        SELECT a.id_apprenti, p.prenom, p.nom
        FROM apprentis a
        JOIN personnes p ON a.id_apprenti = p.id_personne
    """)
    apprentices = g.cursor.fetchall()

    g.cursor.execute("SELECT * FROM branches")
    branches = g.cursor.fetchall()

    g.cursor.execute("SELECT id_semestre, valeur FROM semestres")
    semestres = g.cursor.fetchall()

    return render_template(
        'grade/create.html',
        apprentices=apprentices,
        branches=branches,
        semestres=semestres
    )

@bp.route('/edit/<int:id_note>', methods=['GET', 'POST'])
def edit_grade(id_note):
    if request.method == 'POST':
        id_apprenti = request.form['id_apprenti']
        id_branche = request.form['id_branche']
        id_semestre = request.form['id_semestre']
        valeur = request.form['valeur']

        g.cursor.execute("""
            UPDATE notes
            SET valeur = %s,
                id_apprenti = %s,
                id_semestre = %s,
                id_branche = %s
            WHERE id_note = %s
        """, (valeur, id_apprenti, id_semestre, id_branche, id_note))
        g.db.commit()
        flash("Apprentice updated successfully!")
        return redirect(url_for('grade.list_grades'))

    # Fetch current grade
    g.cursor.execute("SELECT * FROM notes WHERE id_note = %s", (id_note,))
    note = g.cursor.fetchone()

    # Fetch dropdown data
    g.cursor.execute("""
        SELECT a.id_apprenti, p.prenom
        FROM apprentis a
        JOIN personnes p ON a.id_apprenti = p.id_personne
    """)
    apprentices = g.cursor.fetchall()

    g.cursor.execute("SELECT * FROM branches")
    branches = g.cursor.fetchall()

    g.cursor.execute("SELECT id_semestre, valeur FROM semestres")
    semestres = g.cursor.fetchall()

    return render_template(
        'grade/edit.html',
        note=note,
        apprentices=apprentices,
        branches=branches,
        semestres=semestres
    )

@bp.route('/delete/<int:id_note>', methods=['GET', 'POST'])
def delete_grade(id_note):
    if request.method == 'POST':
        g.cursor.execute("DELETE FROM notes WHERE id_note = %s", (id_note,))
        g.db.commit()
        flash("Apprentice deleted successfully!")
        return redirect(url_for('grade.list_grades'))

    g.cursor.execute("SELECT * FROM notes WHERE id_note = %s", (id_note,))
    note = g.cursor.fetchone()

    return render_template('grade/delete.html', note=note)
