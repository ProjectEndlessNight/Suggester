from flask import Flask, render_template, jsonify, request
import hjson
import datetime

app = Flask("EndlessNightSuggester")

##################################################
# base config, change me
BASETITLE = "Endless Night Suggestion Box" # title of the page
LIST_TITLE = " - Public Listing" # title of the public listing page
BACKTO = "http://127.0.0.1/" # link to go back to the homepage (required)
BACKTOTEXT = "Back to the homepage" # text shown on the back button
MOTD = "Submit suggestions for media to be added to Project Endless Night here." # message shown right before the form
FOOTER = "Copyright &copy;1984 (Big brother is watching) Project Endless Night - No rights reserved" # message shown in footer
ERROR_MSG = "Whoops, it seems your suggestion <b>already exists in the database</b>." # message shown when a suggestion is rejected for being a duplicate
SUCCESS_MSG = "Your suggestion has been added to the database. Check the public listing to see the current status of your media. Thank you for your contribution!" # message shown when a suggestion is accepted
ALLOWPUBLICVIEW = True # allow anybody to view suggestions
NOPUBLIC_MSG = "Public viewing of suggestions is disabled." # message shown when public viewing is disabled
PORT = 5000 # port to run the server on
ADMIN_PASSWD = "password" # password to access the admin panel
# more advanced config, you probably don't need to mess with this
# types are in the format ["type", "display name"]
TYPES = [["movies", "Movies"], ["tv", "TV"], ["music", "Music"], ["books", "eBooks"], ["audiobooks", "Audiobooks"], ["podcasts", "Podcasts"], ["roms", "Games (Console ROMs)"], ["pcgames", "Games (Windows, Linux, or MacOS)"], ["software", "Software/Warez"], ["genericvideo", "Other Video"], ["genericaudio", "Other Audio"], ["genericsoftware", "Other Software"], ["other", "Something completely different"]]
DEBUG = True # enables flask debug mode
# DO NOT CHANGE ANYTHING BELOW THIS LINE
TYPES_DICT = {i[0]: i[1] for i in TYPES}
##################################################

with open("suggestions.hjson", "r") as f:
    suggestions = hjson.load(f)

def save_suggestions():
    global suggestions
    with open("suggestions.hjson", "w") as f:
        hjson.dump(suggestions, f)

def load_suggestions():
    global suggestions
    with open("suggestions.hjson", "r") as f:
        suggestions = hjson.load(f)

def do_suggestion(formdata):
    global suggestions
    print("Adding suggestion for " + formdata["title"])
    load_suggestions()
    if formdata["type"] not in [i[0] for i in TYPES]:
        return False
    print("Checking for duplicates of name or URI")
    for i in suggestions["pending"]:
        if i["title"] == formdata["title"] or i["url"] == formdata["url"]:
            print("Duplicate found - aborting!")
            return False
    print("No duplicates found - adding suggestion")
    suggestions["pending"].append({"title": formdata["title"], "url": formdata["url"], "type": formdata["type"], "desc": formdata["desc"], "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    save_suggestions()
    return True

@app.route("/")
def index():
    return render_template("index.html", title=BASETITLE, backto=BACKTO, backto_text=BACKTOTEXT, motd=MOTD, types=TYPES, footer_msg=FOOTER, allow_pub=ALLOWPUBLICVIEW)

@app.route("/add", methods=["POST"])
def add_suggestion():
    success = do_suggestion(request.form)
    if not success:
        return render_template("message.html", title=BASETITLE, backto=BACKTO, backto_text=BACKTOTEXT, footer_msg=FOOTER, msg=ERROR_MSG) # simplifies things if the same file is used for both messages
    else:
        return render_template("message.html", title=BASETITLE, backto=BACKTO, backto_text=BACKTOTEXT, footer_msg=FOOTER, msg=SUCCESS_MSG)

@app.route("/list")
def public_list():
    if not ALLOWPUBLICVIEW:
        return render_template("message.html", title=BASETITLE, backto=BACKTO, backto_text=BACKTOTEXT, footer_msg=FOOTER, msg=NOPUBLIC_MSG)
    load_suggestions()
    return render_template("list.html", title=BASETITLE+LIST_TITLE, backto=BACKTO, backto_text=BACKTOTEXT, footer_msg=FOOTER, suggestions=suggestions["pending"]+suggestions["reviewed"], types=TYPES_DICT)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    # check password cookie
    if request.method == "POST":
        # literally just set the cookie and redirect to the admin page
        if request.form["password"] == ADMIN_PASSWD:
            resp = app.make_response(render_template("admin.html", title="(Admin) "+BASETITLE, backto=BACKTO, backto_text=BACKTOTEXT, footer_msg=FOOTER, suggestions=suggestions["pending"], types=TYPES_DICT))
            resp.set_cookie("password", ADMIN_PASSWD)
            return resp
        else:
            return render_template("admin_login.html", title="(Admin) "+BASETITLE, backto=BACKTO, backto_text=BACKTOTEXT, footer_msg=FOOTER, msg="Incorrect password!")
    if request.cookies.get("password") != ADMIN_PASSWD:
        return render_template("admin_login.html", title="(Admin) "+BASETITLE, backto=BACKTO, backto_text=BACKTOTEXT, footer_msg=FOOTER, msg="Please log in to access the admin panel.")
    else:
        return render_template("admin.html", title="(Admin) "+BASETITLE, backto=BACKTO, backto_text=BACKTOTEXT, footer_msg=FOOTER, suggestions=suggestions["pending"], types=TYPES_DICT)

@app.route("/admin/review", methods=["POST"])
def admin_review():
    if request.cookies.get("password") != ADMIN_PASSWD:
        return render_template("admin_login.html", title="(Admin) "+BASETITLE, backto=BACKTO, backto_text=BACKTOTEXT, footer_msg=FOOTER, msg="Please log in to access the admin panel.")
    if request.form["action"] == "accept":
        load_suggestions()
        suggestions["reviewed"].append(suggestions["pending"][int(request.form["id"])])
        suggestions["reviewed"][-1]["approved"] = True
        suggestions["pending"].pop(int(request.form["id"]))
        save_suggestions()
        return render_template("admin.html", title="(Admin) "+BASETITLE, backto=BACKTO, backto_text=BACKTOTEXT, footer_msg=FOOTER, suggestions=suggestions["pending"], types=TYPES_DICT)
    elif request.form["action"] == "reject":
        load_suggestions()
        suggestions["rejected"].append(suggestions["pending"][int(request.form["id"])])
        suggestions["pending"].pop(int(request.form["id"]))
        save_suggestions()
        return render_template("admin.html", title="(Admin) "+BASETITLE, backto=BACKTO, backto_text=BACKTOTEXT, footer_msg=FOOTER, suggestions=suggestions["pending"], types=TYPES_DICT)
    else:
        return render_template("admin.html", title="(Admin) "+BASETITLE, backto=BACKTO, backto_text=BACKTOTEXT, footer_msg=FOOTER, suggestions=suggestions["pending"], types=TYPES_DICT)

@app.route("/logout")
def admin_logout():
    # just removes the cookie
    resp = app.make_response(render_template("admin_login.html", title="(Admin) "+BASETITLE, backto=BACKTO, backto_text=BACKTOTEXT, footer_msg=FOOTER, msg="Successfully logged out."))
    resp.set_cookie("password", "", expires=0)
    return resp

if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)