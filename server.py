#!/usr/bin/env python3
"""
Romi Oyo — Serveur web
Backend Python stdlib : http.server + socketserver
Déploiement : Railway (Nixpacks)
"""

import http.server
import socketserver
import json
import os
import hashlib
import uuid
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# ===== CONFIG =====
PORT        = int(os.environ.get('PORT', 8080))
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', 'admin2026romi')
EMAIL_FROM  = os.environ.get('NOTIF_EMAIL_FROM', '')
EMAIL_PASS  = os.environ.get('NOTIF_EMAIL_PASS', '')
EMAIL_TO    = os.environ.get('NOTIF_EMAIL_TO', '')

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))

# ===== FICHIERS DE DONNÉES =====
DATA_FILE        = os.path.join(BASE_DIR, 'data.json')
CONTACTS_FILE    = os.path.join(BASE_DIR, 'contacts.json')
AUDIENCES_FILE   = os.path.join(BASE_DIR, 'audiences.json')
RECLAMATIONS_FILE= os.path.join(BASE_DIR, 'reclamations.json')
USERS_FILE       = os.path.join(BASE_DIR, 'users.json')
SESSIONS_FILE    = os.path.join(BASE_DIR, 'sessions.json')

MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css':  'text/css; charset=utf-8',
    '.js':   'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png':  'image/png',
    '.jpg':  'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif':  'image/gif',
    '.webp': 'image/webp',
    '.svg':  'image/svg+xml',
    '.ico':  'image/x-icon',
    '.woff2':'font/woff2',
    '.woff': 'font/woff',
    '.ttf':  'font/ttf',
}

_lock = threading.Lock()

# ===== HELPERS JSON =====
def read_json(path, default=None):
    if default is None:
        default = {}
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return default

def write_json(path, data):
    with _lock:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def append_json_list(path, item):
    data = read_json(path, default=[])
    data.append(item)
    write_json(path, data)

def now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# ===== EMAIL =====
def send_email(subject, body):
    if not all([EMAIL_FROM, EMAIL_PASS, EMAIL_TO]):
        return
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From']    = EMAIL_FROM
        msg['To']      = EMAIL_TO
        msg.attach(MIMEText(body, 'html', 'utf-8'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as srv:
            srv.login(EMAIL_FROM, EMAIL_PASS)
            srv.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    except Exception as e:
        print(f'[EMAIL] Erreur envoi : {e}')

def notify_email(subject, body):
    threading.Thread(target=send_email, args=(subject, body), daemon=True).start()

# ===== AUTH =====
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def check_session(token):
    sessions = read_json(SESSIONS_FILE, {})
    return token in sessions

def create_session():
    token = str(uuid.uuid4())
    sessions = read_json(SESSIONS_FILE, {})
    sessions[token] = now_str()
    write_json(SESSIONS_FILE, sessions)
    return token

# ===== HANDLER =====
class RomiHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f'[{now_str()}] {fmt % args}')

    def send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, path):
        try:
            with open(path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, 'Page non trouvée')

    def send_file(self, path):
        ext = os.path.splitext(path)[1].lower()
        mime = MIME_TYPES.get(ext, 'application/octet-stream')
        try:
            with open(path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Cache-Control', 'public, max-age=86400')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode('utf-8'))
        except Exception:
            return {}

    def get_token(self):
        auth = self.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            return auth[7:]
        return ''

    # ===== GET =====
    def do_GET(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip('/')

        # Page d'accueil
        if path in ('', '/'):
            self.send_html(os.path.join(BASE_DIR, 'index.html'))
            return

        # Pages HTML
        if path == '/admin':
            self.send_html(os.path.join(BASE_DIR, 'admin.html'))
            return
        if path == '/gestion':
            self.send_html(os.path.join(BASE_DIR, 'gestion.html'))
            return

        # Fichiers statiques
        if path.startswith('/static/'):
            file_path = os.path.join(BASE_DIR, path.lstrip('/'))
            if os.path.isfile(file_path):
                self.send_file(file_path)
            else:
                self.send_error(404)
            return

        # data.json direct (fallback frontend)
        if path == '/data.json':
            self.send_file(DATA_FILE)
            return

        # ===== API GET =====
        if path == '/api/load':
            data = read_json(DATA_FILE)
            self.send_json(data)
            return

        if path == '/api/stats':
            if not check_session(self.get_token()):
                self.send_json({'error': 'Non autorisé'}, 401)
                return
            contacts    = read_json(CONTACTS_FILE, [])
            audiences   = read_json(AUDIENCES_FILE, [])
            reclamations= read_json(RECLAMATIONS_FILE, [])
            data        = read_json(DATA_FILE)
            self.send_json({
                'contacts':     len(contacts),
                'audiences':    len(audiences),
                'reclamations': len(reclamations),
                'visites':      data.get('stats', {}).get('visites', 0)
            })
            return

        if path == '/api/contacts':
            if not check_session(self.get_token()):
                self.send_json({'error': 'Non autorisé'}, 401)
                return
            self.send_json(read_json(CONTACTS_FILE, []))
            return

        if path == '/api/audiences':
            if not check_session(self.get_token()):
                self.send_json({'error': 'Non autorisé'}, 401)
                return
            self.send_json(read_json(AUDIENCES_FILE, []))
            return

        if path == '/api/reclamations':
            if not check_session(self.get_token()):
                self.send_json({'error': 'Non autorisé'}, 401)
                return
            self.send_json(read_json(RECLAMATIONS_FILE, []))
            return

        self.send_error(404, 'Route non trouvée')

    # ===== POST =====
    def do_POST(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip('/')
        body   = self.read_body()

        # --- Connexion admin ---
        if path == '/api/login':
            users = read_json(USERS_FILE, {})
            pwd_hash = hash_password(body.get('password', ''))
            user = users.get(body.get('username', ''))
            if user and user.get('password') == pwd_hash:
                token = create_session()
                self.send_json({'success': True, 'token': token})
            else:
                self.send_json({'error': 'Identifiants incorrects'}, 401)
            return

        # --- Contact ---
        if path == '/api/contact':
            nom     = str(body.get('nom', '')).strip()
            email   = str(body.get('email', '')).strip()
            sujet   = str(body.get('sujet', '')).strip()
            message = str(body.get('message', '')).strip()
            if not all([nom, email, sujet, message]):
                self.send_json({'error': 'Tous les champs sont requis.'}, 400)
                return
            record = {'id': str(uuid.uuid4()), 'type': 'contact', 'nom': nom, 'email': email, 'sujet': sujet, 'message': message, 'date': now_str()}
            append_json_list(CONTACTS_FILE, record)
            notify_email(f'[Romi Oyo] Nouveau contact : {sujet}',
                f'<b>De :</b> {nom} ({email})<br><b>Sujet :</b> {sujet}<br><br>{message}')
            self._update_stat('contacts')
            self.send_json({'success': True, 'message': 'Votre message a bien été envoyé. Nous vous répondrons sous 48h.'})
            return

        # --- Audience ---
        if path == '/api/audience':
            nom     = str(body.get('nom', '')).strip()
            tel     = str(body.get('telephone', '')).strip()
            objet   = str(body.get('objet', '')).strip()
            message = str(body.get('message', '')).strip()
            if not all([nom, tel, objet, message]):
                self.send_json({'error': 'Veuillez remplir tous les champs obligatoires.'}, 400)
                return
            record = {'id': str(uuid.uuid4()), 'type': 'audience', 'nom': nom, 'telephone': tel, 'email': body.get('email', ''), 'objet': objet, 'message': message, 'date': now_str(), 'statut': 'en_attente'}
            append_json_list(AUDIENCES_FILE, record)
            notify_email(f'[Romi Oyo] Demande d\'audience : {objet}',
                f'<b>Nom :</b> {nom}<br><b>Tél :</b> {tel}<br><b>Objet :</b> {objet}<br><br>{message}')
            self._update_stat('audiences')
            self.send_json({'success': True, 'message': 'Votre demande d\'audience a bien été enregistrée. L\'équipe du député vous contactera sous 48h.'})
            return

        # --- Réclamation ---
        if path == '/api/reclamation':
            nom      = str(body.get('nom', '')).strip()
            tel      = str(body.get('telephone', '')).strip()
            quartier = str(body.get('quartier', '')).strip()
            type_req = str(body.get('type', '')).strip()
            message  = str(body.get('message', '')).strip()
            if not all([nom, tel, quartier, type_req, message]):
                self.send_json({'error': 'Veuillez remplir tous les champs obligatoires.'}, 400)
                return
            record = {'id': str(uuid.uuid4()), 'type': 'reclamation', 'nom': nom, 'telephone': tel, 'quartier': quartier, 'categorie': type_req, 'message': message, 'date': now_str(), 'statut': 'nouveau'}
            append_json_list(RECLAMATIONS_FILE, record)
            notify_email(f'[Romi Oyo] Réclamation ({type_req}) — {quartier}',
                f'<b>Nom :</b> {nom}<br><b>Tél :</b> {tel}<br><b>Quartier :</b> {quartier}<br><b>Type :</b> {type_req}<br><br>{message}')
            self._update_stat('reclamations')
            self.send_json({'success': True, 'message': 'Votre réclamation a bien été enregistrée. Le bureau du député en prend note.'})
            return

        # --- Compteur visites ---
        if path == '/api/track-visit':
            self._update_stat('visites')
            self.send_json({'success': True})
            return

        # --- Mise à jour data (admin) ---
        if path == '/api/update-data':
            if not check_session(self.get_token()):
                self.send_json({'error': 'Non autorisé'}, 401)
                return
            data = read_json(DATA_FILE)
            # Autoriser la mise à jour de certains champs seulement
            allowed_keys = ['biographie', 'chiffres', 'actions', 'fondation', 'assemblee', 'actualites', 'galerie', 'temoignages', 'contact']
            for k in allowed_keys:
                if k in body:
                    data[k] = body[k]
            write_json(DATA_FILE, data)
            self.send_json({'success': True, 'message': 'Données mises à jour.'})
            return

        self.send_json({'error': 'Route non trouvée'}, 404)

    # ===== OPTIONS (CORS) =====
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def _update_stat(self, key):
        data = read_json(DATA_FILE)
        stats = data.get('stats', {'visites': 0, 'contacts': 0, 'audiences': 0, 'reclamations': 0})
        stats[key] = stats.get(key, 0) + 1
        data['stats'] = stats
        write_json(DATA_FILE, data)


# ===== INITIALISATION =====
def init_files():
    """Créer les fichiers JSON si absents."""
    for path, default in [
        (CONTACTS_FILE, []),
        (AUDIENCES_FILE, []),
        (RECLAMATIONS_FILE, []),
        (SESSIONS_FILE, {}),
        (USERS_FILE, {
            'admin': {
                'password': hashlib.sha256(b'admin2026romi').hexdigest(),
                'role': 'admin'
            }
        }),
    ]:
        if not os.path.exists(path):
            write_json(path, default)
            print(f'[INIT] Fichier créé : {path}')


# ===== DÉMARRAGE =====
if __name__ == '__main__':
    init_files()
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(('', PORT), RomiHandler) as httpd:
        print(f'')
        print(f'  ███████╗ ██████╗ ███╗   ███╗██╗     ██████╗ ██╗   ██╗ ██████╗ ')
        print(f'  ██╔══██╗██╔═══██╗████╗ ████║██║    ██╔═══██╗╚██╗ ██╔╝██╔═══██╗')
        print(f'  ███████╗██║   ██║██╔████╔██║██║    ██║   ██║ ╚████╔╝ ██║   ██║')
        print(f'  ██╔══██╗██║   ██║██║╚██╔╝██║██║    ██║   ██║  ╚██╔╝  ██║   ██║')
        print(f'  ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║    ╚██████╔╝   ██║   ╚██████╔╝')
        print(f'  ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═════╝    ╚═╝    ╚═════╝ ')
        print(f'')
        print(f'  Député de Ouenzé 3 — Brazzaville, République du Congo')
        print(f'  Serveur démarré sur le port {PORT}')
        print(f'  http://localhost:{PORT}')
        print(f'')
        httpd.serve_forever()
