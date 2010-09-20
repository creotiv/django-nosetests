"""This is a very basic example of a plugin that controls all test
output. In this case, it formats the output as ugly unstyled html.

Upgrading this plugin into one that uses a template and css to produce
nice-looking, easily-modifiable html output is left as an exercise for
the reader who would like to see his or her name in the nose AUTHORS file.
"""
import traceback
from nose.plugins import Plugin
import template
import time
from cStringIO import StringIO

class HtmlOutput(Plugin):
    """Output test results styled html.
    """
    
    name = 'html-output'
    score = 2 # run late
    
    def __init__(self):
        super(HtmlOutput, self).__init__()
        self.html = StringIO()
        self.start_time = time.time()
        self.html.write(template.HEADER)
        self.html.write(template.TITLE % time.strftime('%a %Y-%m-%d %H:%M %Z'))
        self.html.write(template.TABLE_HEADER)
    
    def options(self, parser, env):
        """Register commmandline options.
        """
        Plugin.options(self, parser, env)
        parser.add_option(
            "--html-output",
            default=env.get('NOSE_OUTPUT_FILE'),
            dest="outputFile", help="Dest. of output file")

    def configure(self, options, conf):
        """Configure plugin.
        """
        Plugin.configure(self, options, conf)
        self.output_file = options.outputFile
        self.conf = conf

    def addSuccess(self, test):
        self.html.write(template.TABLE_ROW_OK)
        
    def addError(self, test, err):
        err = self.formatErr(err)
        self.html.write(template.TABLE_ROW_FAIL % 'ERROR')
        self.html.write(template.TABLE_ROW_TRACEBACK % err)            

    def addFailure(self, test, err):
        err = self.formatErr(err)
        self.html.write(template.TABLE_ROW_FAIL % 'FAIL')
        self.html.write(template.TABLE_ROW_TRACEBACK % err)

    def finalize(self, result):
        if not result.wasSuccessful():
            res = '<span class="critical">FAILED</span>'     
        else:        
            res = '<span class="normal">OK</span>'

        self.html.write(template.TABLE_FOOTER %
                         (result.testsRun, time.time()-self.start_time,len(result.errors),len(result.failures),res))
        self.html.write(template.FOOTER)

        fp = file(self.output_file,'w')
        fp.write(self.html.getvalue())
        fp.close()

    def formatErr(self, err):
        exctype, value, tb = err
        return ''.join(traceback.format_exception(exctype, value, tb))
    
    def setOutputStream(self, stream):
        # grab for own use
        self.stream = stream        
        # return dummy stream
        class dummy:
            def write(self, *arg):
                pass
            def writeln(self, *arg):
                pass
            def isatty(self):
                pass
            def flush(self):
                pass
        d = dummy()
        return d

    def startContext(self, ctx):
        """try:
            n = ctx.__name__
        except AttributeError:
            n = str(ctx).replace('<', '').replace('>', '')
        self.html.extend(['<div>', '<div style="padding:10px;">', n, '</div>'])
        try:
            path = ctx.__file__.replace('.pyc', '.py')
            self.html.extend(['<div>', path, '</div>'])
        except AttributeError:
            pass
        """
        pass

    def stopContext(self, ctx):
        pass
    
    def startTest(self, test):
        self.html.write(template.TABLE_ROW_NAME % test.shortDescription() or str(test))
        
    def stopTest(self, test):
        pass
