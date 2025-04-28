from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session

XML_FILE = 'data/data.xml'
SELECTED_CHECKS_FILE = 'data/selected_checks.xml'
CHECK_DEFINITIONS_FILE = 'data/check_definitions.xml'

# Ensure XML file and structure exist
def initialize_xml():
    if not os.path.exists(XML_FILE):
        os.makedirs(os.path.dirname(XML_FILE), exist_ok=True)
        root = ET.Element("root")
        tree = ET.ElementTree(root)
        tree.write(XML_FILE)

def initialize_selected_checks_xml():
    if not os.path.exists(SELECTED_CHECKS_FILE):
        os.makedirs(os.path.dirname(SELECTED_CHECKS_FILE), exist_ok=True)
        root = ET.Element("selected_checks")
        tree = ET.ElementTree(root)
        tree.write(SELECTED_CHECKS_FILE)

def get_account_details(account_name):
    initialize_xml()
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
    except ET.ParseError:
        return None, None, None

    for entry in root.findall("entry"):
        if entry.find("account_name").text == account_name:
            application_name = entry.find("application_name").text
            service_now_name = entry.find("service_now_name").text
            timestamp = entry.find("timestamp").text
            return application_name, service_now_name, timestamp
    return None, None, None

def get_check_definitions():
    tree = ET.parse(CHECK_DEFINITIONS_FILE)
    root = tree.getroot()
    checks = {}
    for check in root.findall('check'):
        name = check.find('name').text
        how = check.find('how_to_perform').text
        outcome = check.find('expected_outcome').text
        checks[name] = {'how_to_perform': how, 'expected_outcome': outcome}
    return checks

@app.route("/", methods=["GET"])
def index():
    if 'account_name' in session:
        account_name = session['account_name']
        application_name, service_now_name, timestamp = get_account_details(account_name)
        return render_template("index.html", logged_in=True, account_name=account_name, application_name=application_name, service_now_name=service_now_name)
    else:
        return render_template("index.html", logged_in=False)

@app.route("/register", methods=["POST"])
def register():
    account_name = request.form.get("account_name")
    application_name = request.form.get("application_name")
    service_now_name = request.form.get("service_now_name")

    initialize_xml()
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    for entry in root.findall("entry"):
        if entry.find("account_name").text == account_name:
            return '''
                <script>
                    alert("Account already exists!");
                    window.location.href = "/";
                </script>
            '''

    new_entry = ET.SubElement(root, "entry")
    ET.SubElement(new_entry, "account_name").text = account_name
    ET.SubElement(new_entry, "application_name").text = application_name
    ET.SubElement(new_entry, "service_now_name").text = service_now_name
    ET.SubElement(new_entry, "timestamp").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tree.write(XML_FILE)
    return '''
        <script>
            alert("Registration Successful!");
            window.location.href = "/";
        </script>
    '''

@app.route("/login", methods=["POST"])
def login():
    account_name = request.form.get("account_name")
    application_name, service_now_name, timestamp = get_account_details(account_name)

    if application_name:
        session['account_name'] = account_name
        return redirect(url_for("index"))
    else:
        return '''
            <script>
                alert("Invalid account name!");
                window.location.href = "/";
            </script>
        '''

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route('/save_selected_checks', methods=['POST'])
def save_selected_checks():
    if 'account_name' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    account_name = session['account_name']
    data = request.get_json()
    selected = data['checks']

    initialize_selected_checks_xml()
    defs = get_check_definitions()
    tree = ET.parse(SELECTED_CHECKS_FILE)
    root = tree.getroot()

    user_elem = root.find(f"./user[@name='{account_name}']")
    if user_elem is None:
        user_elem = ET.SubElement(root, "user", name=account_name)

    for check_name in selected:
        if user_elem.find(f"./check[name='{check_name}']") is None:
            check_elem = ET.SubElement(user_elem, "check")
            ET.SubElement(check_elem, "name").text = check_name
            ET.SubElement(check_elem, "how_to_perform").text = defs[check_name]['how_to_perform']
            ET.SubElement(check_elem, "expected_outcome").text = defs[check_name]['expected_outcome']

    tree.write(SELECTED_CHECKS_FILE)
    return jsonify({"message": "Selected checks saved successfully!"})

@app.route('/get_selected_checks', methods=['GET'])
def get_selected_checks():
    if 'account_name' not in session:
        return jsonify([])

    account_name = session['account_name']
    initialize_selected_checks_xml()
    tree = ET.parse(SELECTED_CHECKS_FILE)
    root = tree.getroot()
    selected = []

    user_elem = root.find(f"./user[@name='{account_name}']")
    if user_elem is not None:
        for check in user_elem.findall('check'):
            selected.append({
                'name': check.find('name').text,
                'how_to_perform': check.find('how_to_perform').text,
                'expected_outcome': check.find('expected_outcome').text
            })

    return jsonify(selected)

if __name__ == "__main__":
    app.run(debug=True)
