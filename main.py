import flask
import pypinyin
import bs4
import re
import pdfkit
import io

index_html = open(r".\static\index.html", encoding="utf-8").read()
raw_html = open(r".\static\print.html", encoding="utf-8").read()


def new_tag(html: str = ""):
    soup = bs4.BeautifulSoup(html, "lxml")

    try:
        if soup.html.head is not None:
            assert len(soup.html.head.contents) == 1
            tag = soup.head.contents[0]
        elif soup.html.body is not None:
            assert len(soup.html.body.contents) == 1
            tag = soup.body.contents[0]
        else:
            raise

        return tag
    except AttributeError:
        return bs4.BeautifulSoup(features="lxml")


class 看音写词:
    soup = None
    pdf = None

    def __init__(self, 词列表, title="看音写词"):
        def pinyin(词):
            try:
                每个字的拼音 = iter(
                    pypinyin.pinyin(词)
                )
                __pinyin__ = next(每个字的拼音)[0]

                for each_pinyin in 每个字的拼音:
                    __pinyin__ = f"{__pinyin__} {each_pinyin[0]}"

                return __pinyin__
            except StopIteration:
                return ""

        self.pinyin_dict = {每个词: pinyin(每个词) for 每个词 in 词列表}
        self.title = title

    def get_html(self):
        if self.soup is None:
            self.soup = bs4.BeautifulSoup(raw_html, "lxml")

            # 添加标题
            self.soup.append(
                new_tag(
                    rf"<h1>{self.title}</h1>"
                )
            )

            # 添加题目
            for each_pinyin in self.pinyin_dict:
                self.soup.append(
                    new_tag(
                        rf'<div class="question"><p class="pinyin">{self.pinyin_dict[each_pinyin]}</p><pre class="kuohao">（{" " * (len(each_pinyin) * 3)}）</pre></div>'
                    )
                )

        return str(
            self.soup
        )

    def get_pdf(self):
        if self.soup is None:
            self.pdf = pdfkit.from_string(
                self.get_html(),
                False
            )
        return self.pdf


app = flask.Flask(__name__, static_url_path='')
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['get'])
def index():
    return index_html


@app.route('/pdf', methods=['POST'])
def pdf():
    title = flask.request.form["title"] if flask.request.form["title"] != "" else "看音写词"
    看音写词obj = 看音写词(
        词列表=re.sub(
            r"\\.",
            " ",
            repr(flask.request.form["content"])[1:-1]
        ).split(" "),
        title=title
    )

    return flask.send_file(
        io.BytesIO(
            看音写词obj.get_pdf()
        ),
        attachment_filename=f"{title}.pdf",
        mimetype="application/pdf"
    )


if __name__ == '__main__':
    app.run(
        host="192.168.1.7",
        port=80,
    )
