import re
from io import StringIO
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    HREF_REGEX = re.compile(r'https://habr.com/')
    NORMAL = 0
    IN_SCRIPT = 1

    def __init__(self, *args, hrefs=None, **kwargs):
        self._writer = StringIO()
        self._state = self.NORMAL
        self._hrefs = hrefs
        super().__init__(*args, **kwargs)

    def handle_data(self, data):
        if self._state == self.NORMAL:
            self._writer.write(self.parse_words(data))
        else:
            self._writer.write(data)

    def parse_words(self, src_text):
        return re.sub(r'(\b[\w]{6}\b)', r'\1™', src_text, re.MULTILINE + re.DOTALL)

    def get_result(self):
        return self._writer.getvalue()

    def handle_comment(self, data):
        self._writer.write('<!--{}-->'.format(data))

    def handle_pi(self, data):
        self._writer.write('<?{}>'.format(data))

    def handle_decl(self, decl):
        self._writer.write('<!{}>'.format(decl))

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self._state = self.IN_SCRIPT
        else:
            self._state = self.NORMAL
        tag_text = self.get_starttag_text()
        if self._hrefs:
            for old, new in self._hrefs:
                tag_text = tag_text.replace(old, new)
        self._writer.write(tag_text)

    def handle_endtag(self, tag):
        self._state = self.NORMAL
        self._writer.write('</{}>'.format(tag))

    def handle_startendtag(self, tag, attrs):
        tag_text = self.get_starttag_text()
        if self._hrefs:
            for old, new in self._hrefs:
                tag_text = tag_text.replace(old, new)
        self._writer.write(tag_text)
