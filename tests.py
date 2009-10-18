import unittest
import csscompressor

class TestCssCompressor(unittest.TestCase):
    
    def test_remove_comments(self):
        css = "/*This is a \nmultiline comment */\n\n// This is a regular comment\n"
        self.assertEquals(csscompressor.remove_comments(css), '\n\n\n')
    
    def test_normalize_whitespace(self):
        css = '\r\n\n\n\r\n\r\n    \t\t\t   '
        css = '\r\n'
        self.assertEquals(csscompressor.normalize_whitespace(css), ' ')
    
    def test_boxmodelhack(self):
        css = """#main {width: 960px; voice-family: "\\"}\\""; voice-family: inherit; width: 750px;}"""
        bmh_success = '#main {width: 960px; voice-family: ___PSEUDOCLASSBMH___; voice-family: inherit; width: 750px;}'
        converted = csscompressor.convert_boxmodelhack(css)
        self.assertEquals(converted, bmh_success)
        self.assertEquals(csscompressor.restore_boxmodelhack(converted), css)
    
    def test_remove_extra_spaces(self):
        css = "p :link{ color:   #000 }  p {  color:   #999  }  "
        self.assertEquals(csscompressor.remove_extra_spaces(css), 'p :link{color:#000}p{color:#999}')
    
    def test_add_missing_semicolon(self):
        css = "p {color: #000}"
        self.assertEquals(csscompressor.add_missing_semicolon(css), 'p {color: #000;}')
    
    def test_minify_zeros(self):
        css = "p {padding: 0px 0em 0% 0in} p {padding: 0cm 0mm 0pc } p {padding: 0pt 0ex } p{background-position:0 0;}"
        success = 'p {padding:0;} p {padding:0;} p {padding:0;} p{background-position:0 0;}'
        self.assertEquals(csscompressor.minify_zeros(css), success)
    
    def test_shorten_colors(self):
        css = 'p {color:rgb(51, 102,153);color:#11aABb;filter: chroma(color="#FFFFFF");}'
        success = 'p {color:#369;color:#1aB;filter: chroma(color="#FFFFFF");}'
        self.assertEquals(csscompressor.shorten_colors(css), success)
    
    def test_remove_empty_rules(self):
        css = "p {;} p {color: #000} p {}"
        success = " p {color: #000}"
        self.assertEquals(csscompressor.remove_empty_rules(css), success)
    
    def test_replace_multiple_semicolons(self):
        css = "p {color: #000;;;;}"
        success = "p {color: #000;}"
        self.assertEquals(csscompressor.replace_multiple_semicolons(css), success)

if __name__ == '__main__':
    unittest.main()