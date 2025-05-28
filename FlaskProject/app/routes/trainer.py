from flask import Blueprint, render_template, request, redirect, url_for, g
from flask import flash

bp = Blueprint('trainer', __name__, url_prefix='/trainers')

@bp.route('/')
def list_trainers():
    g.cursor.execute("""
        SELECT f.id_formateur, p.prenom, p.nom
        FROM formateurs f
        JOIN personnes p ON f.id_personne = p.id_personne
    """)
    trainers = g.cursor.fetchall()

    # Then for each trainer, fetch their apprentices
    for trainer in trainers:
        g.cursor.execute("""
            SELECT p.prenom, p.nom
            FROM apprentis a
            JOIN personnes p ON a.id_apprenti = p.id_personne
            WHERE a.id_formateur = %s
        """, (trainer['id_formateur'],))
        trainer['apprentices'] = g.cursor.fetchall()
    return render_template('trainer/list.html', trainers=trainers)

@bp.route('/create', methods=['GET', 'POST'])
def create_trainer():
    if request.method == 'POST':
        # Personal info
        prenom = request.form['prenom']
        nom = request.form['nom']
        mail = request.form['mail']
        sexe = request.form['sexe']

        # Address info
        ville = request.form['ville']
        rue = request.form['rue']
        nip = request.form['nip']
        pays = request.form['pays']

        # Insert address
        g.cursor.execute("""
            INSERT INTO adresses (ville, rue, nip, pays)
            VALUES (%s, %s, %s, %s)
        """, (ville, rue, nip, pays))
        g.db.commit()
        id_adresse = g.cursor.lastrowid

        # Insert person
        g.cursor.execute("""
            INSERT INTO personnes (prenom, nom, mail, sexe)
            VALUES (%s, %s, %s, %s)
        """, (prenom, nom, mail, sexe))
        g.db.commit()
        id_personne = g.cursor.lastrowid

        # Insert trainer
        g.cursor.execute("""
            INSERT INTO formateurs (id_adresse, id_personne)
            VALUES (%s, %s)
        """, (id_adresse, id_personne))
        g.db.commit()
        flash("Apprentice created successfully!")
        return redirect(url_for('trainer.list_trainers'))

    return render_template('trainer/create.html')


@bp.route('/edit/<int:id_formateur>', methods=['GET', 'POST'])
def edit_trainer(id_formateur):
    if request.method == 'POST':
        # Personal info
        prenom = request.form['prenom']
        nom = request.form['nom']
        mail = request.form['mail']
        sexe = request.form['sexe']

        # Address info
        ville = request.form['ville']
        rue = request.form['rue']
        nip = request.form['nip']
        pays = request.form['pays']

        # Get IDs
        g.cursor.execute("SELECT id_adresse, id_personne FROM formateurs WHERE id_formateur = %s", (id_formateur,))
        result = g.cursor.fetchone()
        id_adresse = result['id_adresse']
        id_personne = result['id_personne']

        # Update person
        g.cursor.execute("""
            UPDATE personnes
            SET prenom=%s, nom=%s, mail=%s, sexe=%s
            WHERE id_personne=%s
        """, (prenom, nom, mail, sexe, id_personne))

        # Update address
        g.cursor.execute("""
            UPDATE adresses
            SET ville=%s, rue=%s, nip=%s, pays=%s
            WHERE id_adresse=%s
        """, (ville, rue, nip, pays, id_adresse))

        g.db.commit()
        flash("Apprentice updated successfully!")
        return redirect(url_for('trainer.list_trainers'))

    # Load trainer data
    g.cursor.execute("""
        SELECT f.*, p.prenom, p.nom, p.mail, p.sexe, a.ville, a.rue, a.nip, a.pays
        FROM formateurs f
        JOIN personnes p ON f.id_personne = p.id_personne
        JOIN adresses a ON f.id_adresse = a.id_adresse
        WHERE f.id_formateur = %s
    """, (id_formateur,))
    trainer = g.cursor.fetchone()

    return render_template('trainer/edit.html', trainer=trainer)

@bp.route('/delete/<int:id_formateur>', methods=['GET', 'POST'])
def delete_trainer(id_formateur):
    # Load trainer info
    g.cursor.execute("""
        SELECT f.id_formateur, p.prenom, p.nom
        FROM formateurs f
        JOIN personnes p ON f.id_personne = p.id_personne
        WHERE f.id_formateur = %s
    """, (id_formateur,))
    trainer = g.cursor.fetchone()

    # Check if trainer has apprentices assigned
    g.cursor.execute("SELECT COUNT(*) AS total FROM apprentis WHERE id_formateur = %s", (id_formateur,))
    has_apprentices = g.cursor.fetchone()['total'] > 0

    if request.method == 'POST':
        if has_apprentices:
            return render_template('trainer/delete.html', trainer=trainer, trainer_error=True)

        # Get address and person ids
        g.cursor.execute("SELECT id_adresse, id_personne FROM formateurs WHERE id_formateur = %s", (id_formateur,))
        data = g.cursor.fetchone()
        id_adresse = data['id_adresse']
        id_personne = data['id_personne']

        # Delete trainer
        g.cursor.execute("DELETE FROM formateurs WHERE id_formateur = %s", (id_formateur,))
        g.cursor.execute("DELETE FROM personnes WHERE id_personne = %s", (id_personne,))
        g.cursor.execute("DELETE FROM adresses WHERE id_adresse = %s", (id_adresse,))

        g.db.commit()
        flash("Apprentice deleted successfully!")
        return redirect(url_for('trainer.list_trainers'))

    return render_template('trainer/delete.html', trainer=trainer, trainer_error=has_apprentices)
