from flask import Flask, render_template, jsonify, request

app = Flask("ENsuggester")

##################################################
# base config, change me
BASETITLE = "Endless Night Suggestion Box"
BACKTO = "http://127.0.0.1/"
BACKTOTEXT = "Back to the homepage"
MOTD = "Submit suggestions for media to be added to Project Endless Night here."
FOOTER = "Copyright &copy;1984 (Big brother is watching) Project Endless Night - No rights reserved"
# more advanced config, you probably don't need to mess with this
TYPES = [["movies", "Movies"], ["tv", "TV"], ["music", "Music"], ["books", "eBooks"], ["audiobooks", "Audiobooks"], ["podcasts", "Podcasts"], ["roms", "Games (Console ROMs)"], ["pcgames", "Games (Windows, Linux, or MacOS)"], ["software", "Software/Warez"], ["genericvideo", "Other Video"], ["genericaudio", "Other Audio"], ["genericsoftware", "Other Software"], ["other", "Something completely different"]]
##################################################

@app.route("/")
def index():
    return render_template("index.html", title=BASETITLE, backto=BACKTO, backto_text=BACKTOTEXT, motd=MOTD, types=TYPES, footer_msg=FOOTER)

@app.route("/add", methods=["POST"])
def add_suggestion():
    print(request.form)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)