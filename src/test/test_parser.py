import unittest
import modules.parser

SRC = (
    '<!DOCTYPE html>\n'
    '<html lang="ru" class="no-js">\n'
    '<head param="aaa"><title>Test</title>\n'
    '<script>var h1="aaa<hehe>";\n'
    'window.aaaaaa = 1'
    '</script>\n'
    '</head>\n'
    '<body><h1>Parse me!</h1>\n'
    '<li class="post-stats__item post-stats__item_comments">\n'
    '<div>Сейчас на фоне уязвимости Logjam&nbsp;все в индустрии в очередной раз обсуждают\n'
    'проблемы и особенности TLS. Я хочу воспользоваться этой возможностью&#44; чтобы\n'
    ' поговорить об одной из них, а именно — о настройке ciphersiutes.</div>\n'
    '       <a href="https://habr.com/ru/post/441442/#comments" class="post-stats__comments-link" rel="nofollow">\n'
    '        <svg class="icon-svg_post-comments" width="16" height="16">\n'
    '            <use xlink:href="https://habr.com/images/1550655534/common-svg-sprite.svg#comment" /></svg>\n'
    '                <span class="post-stats__comments-count" title="Читать комментарии">293</span>\n'
    '      </a>\n'
    '  </li>\n'
    '</body></html>\n')

EXPECTED = (
    '<!DOCTYPE html>\n'
    '<html lang="ru" class="no-js">\n'
    '<head param="aaa"><title>Test</title>\n'
    '<script>var h1="aaa<hehe>";\n'
    'window.aaaaaa = 1'
    '</script>\n'
    '</head>\n'
    '<body><h1>Parse me!</h1>\n'
    '<li class="post-stats__item post-stats__item_comments">\n'
    '<div>Сейчас™ на фоне уязвимости Logjam™&nbsp;все в индустрии в очередной раз обсуждают\n'
    'проблемы и особенности TLS. Я хочу воспользоваться этой возможностью&#44; чтобы\n'
    ' поговорить об одной из них, а именно™ — о настройке ciphersiutes.</div>\n'
    '       <a href="http://127.0.0.1:8080/ru/post/441442/#comments" class="post-stats__comments-link" rel="nofollow">\n'
    '        <svg class="icon-svg_post-comments" width="16" height="16">\n'
    '            <use xlink:href="http://127.0.0.1:8080/images/1550655534/common-svg-sprite.svg#comment" /></svg>\n'
    '                <span class="post-stats__comments-count" title="Читать комментарии">293</span>\n'
    '      </a>\n'
    '  </li>\n'
    '</body></html>\n')


class ParserTests(unittest.TestCase):
    def test_parser(self):
        hrefs = (('https://habr.com/', 'http://127.0.0.1:8080/'),)
        parser = modules.parser.MyHTMLParser(convert_charrefs=False, hrefs=hrefs)
        parser.feed(SRC)
        result = parser.get_result()
        self.assertEqual(EXPECTED, result, "Wrong result")
