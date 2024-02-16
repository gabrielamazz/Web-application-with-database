# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Secret key for sessions
app.secret_key = 'your_secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'G@briela10'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)


# Daca am intrat in starea de loggedin din session ma duce catre index.html, intrand in sesiunea utilizatorului user
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))


#verifica daca sunt corecte user si password ma duce catre route home
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''  #msjul care urmeaza sa fie transmis
    if request.method == 'POST':   #extrage din formular
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #cursor ptr interogarea bazei de date
        cursor.execute('SELECT * FROM login WHERE user = %s AND password = %s', (username, password,)) #se executa query ptr a cauta user si parola specificate
        account = cursor.fetchone() #obtine rezultatul interogarii
        if account: #daca s-a gasit un user, sunt stocate info in session
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['user']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg) #daca esueaza, ma intoarce la index

# Add a logout route if needed
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    #daca formularul contine campurile user si parola, atunci extrage datele din form
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE user = % s', (username, )) #verifica daca exista deja un user cu numele specificat
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password:
            msg = 'Please fill out the form !'
        else: #daca sunt complete si user si parola, se introduc datele in tabela login
            cursor.execute('INSERT INTO login VALUES (NULL, % s, % s)', (username, password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/gestiune', methods=['GET', 'POST'])
def gestiune():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    oras_cautat = request.args.get('oras_cautat', '')  # Obține orașul din query string

    show_least_service_category = 'show_least_service_category' in request.args
    show_frequent_services = 'show_frequent_services' in request.args
    least_service_category = None
    frequent_services = None
    gestiuni = None

    if show_least_service_category:
        cursor.execute('''
            SELECT 
                c.CategorieID, 
                c.Denumire, 
                (SELECT COUNT(DISTINCT gs.GestiuneID) 
                 FROM Gestiune_Servicii gs 
                 JOIN Dispozitive d ON gs.DispozitivID = d.DispozitivID 
                 WHERE d.CategorieID = c.CategorieID) AS NumarServicii
            FROM Categorii c
            ORDER BY NumarServicii ASC
            LIMIT 1;
        ''')
        
        least_service_category = cursor.fetchone()
    elif show_frequent_services: 
        cursor.execute('''
            SELECT s.ServiciuID, s.Denumire AS NumeServiciu, COUNT(gs.ServiciuID) AS NumarServicii, c.Denumire AS NumeCategorie
            FROM Gestiune_Servicii gs
            JOIN Servicii s ON gs.ServiciuID = s.ServiciuID
            JOIN Dispozitive d ON gs.DispozitivID = d.DispozitivID
            JOIN Categorii c ON d.CategorieID = c.CategorieID
            GROUP BY s.ServiciuID, c.CategorieID
            ORDER BY NumarServicii DESC
        ''')
        frequent_services = cursor.fetchall()
        
    else:
        
        serviciu_id = request.form.get('serviciu_id')
        dispozitiv_id = request.form.get('dispozitiv_id')
        angajat_id = request.form.get('angajat_id')
        data_finalizare = request.form.get('data_finalizare')
        pret = request.form.get('pret')

        try:
            cursor.execute('INSERT INTO gestiune_servicii (ServiciuID, DispozitivID, AngajatID, Data_finalizare, Pret) VALUES (%s, %s, %s, %s, %s)', (serviciu_id, dispozitiv_id, angajat_id, data_finalizare, pret))
            mysql.connection.commit()
            flash('Înregistrarea de gestiune a fost adăugată cu succes.')
        except Exception as e:
            flash('A apărut o eroare la adăugarea înregistrării de gestiune.')
            print(e)
        finally:
            cursor.close()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Preluarea datelor pentru dropdown-uri
    cursor.execute('SELECT ServiciuID, Denumire FROM servicii')
    servicii = cursor.fetchall()
    cursor.execute('''
    SELECT d.DispozitivID, d.Denumire, d.Model,
    (SELECT CONCAT(c.Nume, ' ', c.Prenume) FROM Clienti c WHERE c.ClientID = d.ClientID) AS NumeClient
    FROM Dispozitive d
                ''')
    dispozitive = cursor.fetchall()
    cursor.execute('SELECT AngajatID, Nume, Prenume FROM angajati')
    angajati = cursor.fetchall()

    # Filtrarea înregistrărilor de gestiune pe baza orașului clientului
    if oras_cautat:
        cursor.execute('''
            SELECT gs.GestiuneID,
                   (SELECT s.Denumire FROM Servicii s WHERE s.ServiciuID = gs.ServiciuID) AS NumeServiciu,
                   (SELECT d.Denumire FROM Dispozitive d WHERE d.DispozitivID = gs.DispozitivID) AS NumeDispozitiv,
                   (SELECT d.Model FROM Dispozitive d WHERE d.DispozitivID = gs.DispozitivID) AS Model,
                   (SELECT CONCAT(c.Nume, ' ', c.Prenume) FROM Clienti c WHERE c.ClientID = (SELECT ClientID FROM Dispozitive WHERE DispozitivID = gs.DispozitivID)) AS NumeClient,
                   (SELECT CONCAT(a.Nume, ' ', a.Prenume) FROM Angajati a WHERE a.AngajatID = gs.AngajatID) AS NumeAngajat,
                   gs.Data_finalizare, gs.Pret
            FROM Gestiune_Servicii gs
            WHERE (SELECT c.Oras FROM Clienti c WHERE c.ClientID = (SELECT ClientID FROM Dispozitive WHERE DispozitivID = gs.DispozitivID)) = %s
        ''', (oras_cautat,))
        gestiuni = cursor.fetchall()
    else:
        cursor.execute('''
            SELECT gs.GestiuneID,
                   s.Denumire AS NumeServiciu,
                   d.Denumire AS NumeDispozitiv,
                   d.Model,
                   CONCAT(c.Nume, ' ', c.Prenume) AS NumeClient,
                   CONCAT(a.Nume, ' ', a.Prenume) AS NumeAngajat,
                   gs.Data_finalizare,
                   gs.Pret
            FROM Gestiune_Servicii gs
            JOIN Servicii s ON gs.ServiciuID = s.ServiciuID
            JOIN Dispozitive d ON gs.DispozitivID = d.DispozitivID
            JOIN Clienti c ON d.ClientID = c.ClientID
            JOIN Angajati a ON gs.AngajatID = a.AngajatID
        ''')
        gestiuni = cursor.fetchall()

    cursor.close()
    return render_template('gestiune.html', servicii=servicii, dispozitive=dispozitive, angajati=angajati, gestiuni=gestiuni, oras_cautat=oras_cautat,least_service_category=least_service_category, show_least_service_category=show_least_service_category,frequent_services=frequent_services, show_frequent_services=show_frequent_services)

@app.route('/actualizeaza_gestiune', methods=['POST'])
def actualizeaza_gestiune():
    gestiune_id = request.form.get('gestiune_id')
    data_finalizare_noua = request.form.get('data_finalizare_noua')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        cursor.execute('UPDATE Gestiune_Servicii SET Data_finalizare = %s WHERE GestiuneID = %s', (data_finalizare_noua, gestiune_id))
        mysql.connection.commit()
        flash('Data finalizare a fost actualizată pentru înregistrarea cu ID-ul ' + gestiune_id)
    except Exception as e:
        flash('A apărut o eroare la actualizarea datei de finalizare.')
        print(e)
    finally:
        cursor.close()

    return redirect(url_for('gestiune'))

@app.route('/servicii')
def servicii():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Selectează doar coloanele dorite, excluzând ServiciuID
    cursor.execute('SELECT ServiciuID, Denumire, Pret, Piesa_necesara FROM servicii')
    servicii = cursor.fetchall()
    cursor.close()
    return render_template('servicii.html', servicii=servicii)

@app.route('/actualizeaza_pret_serviciu', methods=['POST'])
def actualizeaza_pret_serviciu():
    serviciu_id = request.form.get('serviciu_id')
    pret_nou = request.form.get('pret_nou')

    # Convertim pret_nou într-un întreg
    try:
        pret_nou_int = int(pret_nou)
    except ValueError:
        flash('Prețul introdus nu este valid.')
        return redirect(url_for('servicii'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        cursor.execute('UPDATE Servicii SET Pret = %s WHERE ServiciuID = %s', (pret_nou_int, serviciu_id))
        mysql.connection.commit()
        flash('Prețul serviciului a fost actualizat.')
    except Exception as e:
        flash('A apărut o eroare la actualizarea prețului serviciului.')
        print(e)
    finally:
        cursor.close()

    return redirect(url_for('servicii'))

@app.route('/clienti', methods=['GET', 'POST'])
def clienti():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    clienti = []


    if request.method == 'POST':
            client_id_str = request.form.get('client_id_stergere')  # obține valoarea din formular sau None dacă nu există
            if client_id_str and client_id_str.isdigit():  # Verifică dacă string-ul există și conține doar cifre
                client_id = int(client_id_str)
                try:
                    cursor.execute('DELETE FROM clienti WHERE ClientID = %s', (client_id,))
                    mysql.connection.commit()
                    flash('Clientul a fost șters cu succes.')
                except Exception as e:
                    flash('A apărut o eroare la ștergerea clientului.')
                    print(e)
            else: 
                if all(key in request.form for key in ['nume', 'prenume', 'email', 'oras']):
            # Extragerea datelor din formular
                    nume = request.form['nume']
                    prenume = request.form['prenume']
                    telefon = request.form['telefon']
                    email = request.form['email']
                    oras = request.form['oras']
                try:
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) # Crearea unui nou cursor pentru operațiuni ulterioare
                    cursor.execute('INSERT INTO clienti (Nume, Prenume, Nr_telefon,Email, Oras) VALUES (%s, %s, %s, %s, %s)', (nume, prenume, telefon, email, oras))
                    mysql.connection.commit()
                    flash('Clientul a fost adăugat cu succes.')
                except Exception as e:
                    flash('A apărut o eroare la adăugarea clientului.')
                    print(e)
                else:
                    flash('Toate câmpurile sunt necesare pentru adăugarea unui client nou.')
    

    show_top = request.args.get('show_top') == 'true'
    show_pending_devices = request.args.get('show_pending_devices') == 'true'
    top_client = None
    pending_clients = None


    if show_top:
        cursor.execute('''
            SELECT 
                c.ClientID, 
                c.Nume, 
                c.Prenume, 
                (SELECT COUNT(DISTINCT gs.GestiuneID) 
                 FROM Gestiune_Servicii gs 
                 JOIN Dispozitive d ON gs.DispozitivID = d.DispozitivID 
                 WHERE d.ClientID = c.ClientID) AS NumarServicii
            FROM Clienti c
            ORDER BY NumarServicii DESC
            LIMIT 1;
        ''')
        top_client = cursor.fetchone()
    elif show_pending_devices:
        cursor.execute('''
            SELECT c.Nume, c.Prenume, d.Denumire AS DenumireDispozitiv
            FROM Clienti c
            JOIN Dispozitive d ON c.ClientID = d.ClientID
            WHERE d.DispozitivID NOT IN (
                SELECT gs.DispozitivID
                FROM Gestiune_Servicii gs
                WHERE gs.Data_finalizare IS NOT NULL AND gs.Data_finalizare <= CURDATE()
            );
        ''')
        pending_clients = cursor.fetchall()
            
    if not show_top and not show_pending_devices:
        cursor.execute('SELECT ClientID, Nume, Prenume, Nr_telefon, Email, Oras FROM clienti')
        clienti = cursor.fetchall()
    
        
    cursor.close()
    return render_template('clienti.html', clienti=clienti,show_top=show_top, top_client=top_client,show_pending_devices=show_pending_devices, pending_clients=pending_clients)


@app.route('/angajati')
def angajati():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cautare_departament = request.args.get('cautare_departament', '')

    show_top = 'show_top' in request.args
    top_angajati = None
    angajati = None
    if show_top:
        # Logica pentru a obține top 3 angajați
        cursor.execute('''
            SELECT a.AngajatID, a.Nume, a.Prenume, d.Nume_departament, COUNT(gs.AngajatID) AS NumarServicii
            FROM Angajati a
            JOIN departamente d ON a.DepartamentID = d.DepartamentID
            JOIN Gestiune_Servicii gs ON a.AngajatID = gs.AngajatID
            GROUP BY a.AngajatID, a.Nume, a.Prenume, d.Nume_departament
            ORDER BY NumarServicii DESC
            LIMIT 3;
        ''')
        top_angajati = cursor.fetchall()

    if cautare_departament:
        # Logica pentru afișarea angajaților filtrată după departament
        cursor.execute('''
            SELECT a.AngajatID, a.Nume, a.Prenume, d.Nume_departament, a.Nr_telefon, a.Email, a.CNP, a.Data_nasterii, a.Oras
            FROM Angajati a
            JOIN Departamente d ON a.DepartamentID = d.DepartamentID
            WHERE d.Nume_departament LIKE %s
        ''', ('%' + cautare_departament + '%',))
    else:
    # Selectează coloanele dorite din tabelul angajati
        cursor.execute('''SELECT a.AngajatID, a.Nume, a.Prenume, d.Nume_departament, a.Nr_telefon, a.Email, a.CNP, a.Data_nasterii, a.Oras
                        FROM angajati a
                        JOIN departamente d ON a.DepartamentID = d.DepartamentID''')
    angajati = cursor.fetchall()
    cursor.close()
    return render_template('angajati.html', angajati=angajati,top_angajati=top_angajati, show_top=show_top)

@app.route('/dispozitive', methods=['GET', 'POST'])
def dispozitive():
   cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   categorii = []
   clienti = []
   dispozitive = []
   cautare_categorie = request.args.get('cautare_categorie', '')  # Inițializează cu un șir gol dacă parametrul nu este prezent

   try:
        if request.method == 'POST':
            dispozitiv_id_str = request.form.get('dispozitiv_id_stergere')
            if dispozitiv_id_str and dispozitiv_id_str.isdigit():
                dispozitiv_id = int(dispozitiv_id_str)
                cursor.execute('DELETE FROM dispozitive WHERE DispozitivID = %s', (dispozitiv_id,))
                mysql.connection.commit()
                flash('Dispozitivul a fost șters cu succes.')
            else:
                # Logica pentru adăugarea dispozitivului...
                denumire = request.form.get('denumire')
                categorie_id = request.form.get('categorie_id') 
                client_id = request.form.get('client_id')
                model = request.form.get('model')
                specificatii = request.form.get('specificatii')

                # Asigurați-vă că toate câmpurile sunt completate
                if denumire and categorie_id and client_id and model and specificatii:
                    cursor.execute('INSERT INTO dispozitive (Denumire, CategorieID, ClientID, Model, Specificatii) VALUES (%s, %s, %s, %s, %s)', (denumire, categorie_id, client_id, model, specificatii))
                    mysql.connection.commit()
                    flash('Dispozitivul a fost adăugat cu succes.')
                else:
                    flash('Toate câmpurile sunt necesare pentru adăugarea unui dispozitiv.')
                return redirect(url_for('dispozitive'))
        
        
        cursor.execute('SELECT CategorieID, Denumire FROM categorii')
        categorii = cursor.fetchall()

        cursor.execute('SELECT ClientID, Nume, Prenume FROM clienti')
        clienti = cursor.fetchall()

        query = '''
            SELECT dispozitive.DispozitivID, dispozitive.Denumire AS DenumireDispozitiv, 
                   categorii.Denumire AS DenumireCategorie, 
                   clienti.Nume AS NumeClient, 
                   clienti.Prenume AS PrenumeClient,
                   dispozitive.Model AS Model,
                   dispozitive.Specificatii AS Specificatii
            FROM dispozitive
            JOIN categorii ON dispozitive.CategorieID = categorii.CategorieID
            JOIN clienti ON dispozitive.ClientID = clienti.ClientID
        '''
        if cautare_categorie:
            query += 'WHERE categorii.Denumire LIKE %s'
            cursor.execute(query, ('%' + cautare_categorie + '%',))
        else:
            cursor.execute(query)

        dispozitive = cursor.fetchall()
   except Exception as e:
        flash('A apărut o eroare: ' + str(e))
   finally:
        cursor.close()

   return render_template('dispozitive.html', categorii=categorii, clienti=clienti, dispozitive=dispozitive, cautare_categorie=cautare_categorie)

if __name__ == "__main__":
        app.run(host="localhost", port=int("5000"))

