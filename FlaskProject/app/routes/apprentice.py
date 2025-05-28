from flask import Blueprint, render_template, request, redirect, url_for, g
from flask import flash

bp = Blueprint('apprentice', __name__, url_prefix='/apprentices')

@bp.route('/')
def list_apprentices():
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    g.cursor.execute("""
        SELECT COUNT(*) AS total FROM apprentis
    """)
    total = g.cursor.fetchone()['total']
    total_pages = (total + per_page - 1) // per_page

    g.cursor.execute("""
        SELECT a.id_apprenti, p.prenom, p.nom, a.annee_scolaire,
               t.id_formateur, tp.prenom AS trainer_prenom, tp.nom AS trainer_nom
        FROM apprentis a
        JOIN personnes p ON a.id_apprenti = p.id_personne
        LEFT JOIN formateurs t ON a.id_formateur = t.id_formateur
        LEFT JOIN personnes tp ON t.id_personne = tp.id_personne
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    apprentices = g.cursor.fetchall()

    return render_template('apprentice/list.html', apprentices=apprentices, page=page, total_pages=total_pages)

@bp.route('/create', methods=['GET', 'POST'])
def create_apprentice():
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

        # School + trainer
        annee_scolaire = request.form['annee_scolaire']
        id_formateur = request.form['id_formateur']

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

        # Insert apprentice
        g.cursor.execute("""
            INSERT INTO apprentis (id_apprenti, annee_scolaire, id_adresse, id_formateur)
            VALUES (%s, %s, %s, %s)
        """, (id_personne, annee_scolaire, id_adresse, id_formateur))
        g.db.commit()

        flash("Apprentice created successfully!")
        return redirect(url_for('apprentice.list_apprentices'))

    # Load existing trainers to show in dropdown
    g.cursor.execute("""
        SELECT f.id_formateur, p.prenom, p.nom
        FROM formateurs f
        JOIN personnes p ON f.id_personne = p.id_personne
    """)
    trainers = g.cursor.fetchall()

    return render_template('apprentice/create.html', trainers=trainers)

@bp.route('/edit/<int:id_apprenti>', methods=['GET', 'POST'])
def edit_apprentice(id_apprenti):
    if request.method == 'POST':
        # Personal info
        prenom = request.form['prenom']
        nom = request.form['nom']
        mail = request.form['mail']
        sexe = request.form['sexe']

        # Address
        ville = request.form['ville']
        rue = request.form['rue']
        nip = request.form['nip']
        pays = request.form['pays']

        # School info
        annee_scolaire = request.form['annee_scolaire']
        id_formateur = request.form['id_formateur']

        # Update personnes
        g.cursor.execute("""
            UPDATE personnes
            SET prenom=%s, nom=%s, mail=%s, sexe=%s
            WHERE id_personne = %s
        """, (prenom, nom, mail, sexe, id_apprenti))

        # Get id_adresse for this apprentice
        g.cursor.execute("SELECT id_adresse FROM apprentis WHERE id_apprenti = %s", (id_apprenti,))
        result = g.cursor.fetchone()
        id_adresse = result['id_adresse']

        # Update adresses
        g.cursor.execute("""
            UPDATE adresses
            SET ville=%s, rue=%s, nip=%s, pays=%s
            WHERE id_adresse = %s
        """, (ville, rue, nip, pays, id_adresse))

        # Update apprentis
        g.cursor.execute("""
            UPDATE apprentis
            SET annee_scolaire=%s, id_formateur=%s
            WHERE id_apprenti=%s
        """, (annee_scolaire, id_formateur, id_apprenti))

        g.db.commit()
        flash("Apprentice updated successfully!")
        return redirect(url_for('apprentice.list_apprentices'))

    # Load apprentice info
    g.cursor.execute("""
        SELECT a.*, p.prenom, p.nom, p.mail, p.sexe, ad.ville, ad.rue, ad.nip, ad.pays
        FROM apprentis a
        JOIN personnes p ON a.id_apprenti = p.id_personne
        JOIN adresses ad ON a.id_adresse = ad.id_adresse
        WHERE a.id_apprenti = %s
    """, (id_apprenti,))
    apprenti = g.cursor.fetchone()

    # Load trainers
    g.cursor.execute("""
        SELECT f.id_formateur, p.prenom, p.nom
        FROM formateurs f
        JOIN personnes p ON f.id_personne = p.id_personne
    """)
    trainers = g.cursor.fetchall()

    return render_template('apprentice/edit.html', apprenti=apprenti, trainers=trainers)


@bp.route('/delete/<int:id_apprenti>', methods=['GET', 'POST'])
def delete_apprentice(id_apprenti):
    # Load apprentice + trainer info
    g.cursor.execute("""
        SELECT a.id_apprenti, p.prenom, p.nom, a.id_formateur
        FROM apprentis a
        JOIN personnes p ON a.id_apprenti = p.id_personne
        WHERE a.id_apprenti = %s
    """, (id_apprenti,))
    apprenti = g.cursor.fetchone()

    if request.method == 'POST':
        if apprenti['id_formateur']:
            # Prevent deletion and show error
            return render_template('apprentice/delete.html', apprenti=apprenti, trainer_error=True)

        # Continue with deletion if no trainer
        g.cursor.execute("SELECT id_adresse FROM apprentis WHERE id_apprenti = %s", (id_apprenti,))
        id_adresse = g.cursor.fetchone()['id_adresse']

        g.cursor.execute("DELETE FROM notes WHERE id_apprenti = %s", (id_apprenti,))
        g.cursor.execute("DELETE FROM bureaux WHERE id_apprenti = %s", (id_apprenti,))
        g.cursor.execute("DELETE FROM apprentis WHERE id_apprenti = %s", (id_apprenti,))
        g.cursor.execute("DELETE FROM personnes WHERE id_personne = %s", (id_apprenti,))
        g.cursor.execute("DELETE FROM adresses WHERE id_adresse = %s", (id_adresse,))

        g.db.commit()
        flash("Apprentice deleted successfully!")
        return redirect(url_for('apprentice.list_apprentices'))

    return render_template('apprentice/delete.html', apprenti=apprenti, trainer_error=False)
