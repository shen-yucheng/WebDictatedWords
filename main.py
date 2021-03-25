import flask
import silent_words_test

app = flask.Flask(__name__, static_url_path='')
app.config['JSON_AS_ASCII'] = False

raw_html = open(r".\static\print.html", encoding="utf-8").read()


@app.route('/zip', methods=['POST'])
def get_pdf():
    title = flask.request.form["title"] if flask.request.form["title"] != "" else "看音写词"

    return flask.send_file(
        silent_words_test.看音写词(words_text=flask.request.form["content"], title=title, raw_html=raw_html).get_zip(),
        attachment_filename=f"{title}.zip",
        mimetype="application/zip",
        as_attachment=True
    )


if __name__ == '__main__':
    app.run()
