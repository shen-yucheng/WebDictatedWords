import flask
import pypinyin
import bs4

app = flask.Flask(__name__, static_url_path='')
app.config['JSON_AS_ASCII'] = False

with open(r".\static\index.html", encoding="utf-8") as file:
    index_html = file.read()


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

    def __init__(self, 词列表):
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

    def get_html(self):
        if self.soup is None:
            self.soup = new_tag()

            # 添加每道题
            for each_pinyin in self.pinyin_dict:
                self.soup.append(
                    new_tag(
                        rf'<div class="question"><p class="pinyin">{self.pinyin_dict[each_pinyin]}</p><pre class="kuohao">（{" " * (len(each_pinyin) * 3)}）</pre></div>'
                    )
                )

        return str(
            self.soup
        )


@app.route('/', methods=['get'])
def index():
    return index_html


@app.route('/pinyin', methods=['POST'])
def get_pinyin_html():
    return 看音写词(
        词列表=flask.request.form["content"].split(" "),
    ).get_html()


if __name__ == '__main__':
    app.run(
        host="192.168.1.7",
        port=80,
    )
