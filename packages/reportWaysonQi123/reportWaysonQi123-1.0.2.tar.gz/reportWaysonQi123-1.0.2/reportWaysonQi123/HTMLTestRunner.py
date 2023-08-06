
__original_author__ = ""
__update_author__ = ""
__version__ = ""

import datetime
import io
import os
import sys
import unittest
import unittest
from xml.sax import saxutils
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('reportWaysonQi123', 'templates'))


class OutputRedirector(object):

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(bytes(s, 'UTF-8'))

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


class TemplateMixin(object):


    DIR = os.path.dirname(os.path.abspath(__file__))
    STYLESHEET_DIR = os.path.join(DIR, 'static', 'css')
    JAVASCRIPT_DIR = os.path.join(DIR, 'static', 'js')
    HTMLTEMPLATE_DIR = os.path.join(DIR, 'templates')

    STATUS = {
        0: 'pass',
        1: 'fail',
        2: 'error',
        3: 'skip'
    }

    DEFAULT_TITLE = 'GLR Automation Test Report'
    DEFAULT_DESCRIPTION = ''


TestResult = unittest.TestResult


class _TestResult(TestResult):

    def __init__(self, verbosity=1):
        super().__init__()
        self.stdout0 = None
        self.stderr0 = None
        self.outputBuffer = None

        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.skip_count = 0

        self.verbosity = verbosity

        self.result = []

    def startTest(self, test):
        TestResult.startTest(self, test)

        # just one buffer for both stdout and stderr
        self.outputBuffer = io.BytesIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):

        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()

    def stopTest(self, test):
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1

        TestResult.addSuccess(self, test)
        output = self.complete_output()

        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('OK ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addFailure(self, test, err):
        self.failure_count += 1

        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()

        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('Fail  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')

    def addError(self, test, err):
        self.error_count += 1

        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()

        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('Error  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addSkip(self, test, err):
        self.skip_count += 1

        TestResult.addSkip(self, test, err)
        _, _exc_str = self.skipped[-1]
        output = self.complete_output()

        self.result.append((3, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('Skip  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('S')


class HTMLTestRunner(TemplateMixin):
    def __init__(self, stream=sys.stdout, verbosity=2, title=None, description=None,
                 theme=None, stylesheet=None, htmltemplate=None, javascript=None):
        self.stream = stream
        self.verbosity = verbosity

        self.start_time = datetime.datetime.now()
        self.duration = None

        self.title = title or self.DEFAULT_TITLE
        self.description = description or self.DEFAULT_DESCRIPTION

        theme = theme or 'default'
        self.htmltemplate = htmltemplate or f'{theme}.html'
        self.stylesheet = stylesheet or f'{theme}.css'
        self.javascript = javascript or f'{theme}.js'

    def run(self, test):
        result = _TestResult(self.verbosity)
        test(result)

        self.duration = datetime.datetime.now() - self.start_time
        data = self.generate_data(result)
        html = self.generate_report(data)

        print(f'\nTime Elapsed: {self.duration}', file=sys.stderr)
        result.pytestreport_data = data
        result.pytestreport_html = html

        return result

    def generate_report(self, data):
        html_template = self.get_html_template()
        output = html_template.render(**data)

        self.stream.write(output.encode('utf-8'))
        return output

    def generate_data(self, result):
        report_detail = self._generate_report_detail(result)
        report_summary = self.get_report_summary(result)
        report_summary['suite_count'] = report_detail['suite_count']
        return {
            'generator': 'PyTestReport %s' % __version__,
            'title': saxutils.escape(self.title),
            'description': saxutils.escape(self.description),
            'stylesheet': self.get_stylesheet(),
            'javascript': self.get_javascript(),
            'report_detail': report_detail,
            'report_summary': report_summary
        }

    def get_report_summary(self, result):
        start_time = str(self.start_time)[:19]
        duration = str(self.duration)
        status = {
            'pass': result.success_count,
            'fail': result.failure_count,
            'error': result.error_count,
            'skip': result.skip_count,
            'count': result.skip_count + result.error_count + result.failure_count + result.success_count
        }
        return {
            'start_time': start_time,
            'duration': duration,
            'status': status,
            'suite_count': 0
        }

    def get_stylesheet(self):
        with open(os.path.join(self.STYLESHEET_DIR, self.stylesheet), encoding='utf-8') as f:
            return f.read()

    def get_javascript(self):
        with open(os.path.join(self.JAVASCRIPT_DIR, self.javascript), encoding='utf-8') as f:
            return f.read()

    def get_html(self):
        with open(os.path.join(self.HTMLTEMPLATE_DIR, self.htmltemplate), encoding='utf-8') as f:
            return f.read()

    def get_html_template(self):
        html = self.get_html()
        return env.from_string(html)

    def _generate_report_detail(self, result):
        tests = []
        sorted_result = self.sort_result(result.result)
        for cid, (cls, cls_results) in enumerate(sorted_result, 1):
            # subtotal for a class
            np = nf = ne = ns = 0
            for n, t, o, e in cls_results:
                if n == 0:  # pass
                    np += 1
                elif n == 1:    # fail
                    nf += 1
                elif n == 2:    # error
                    ne += 1
                else:       # skip
                    ns += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__.split("\n")[0] if cls.__doc__ else ""
            desc = '%s: %s' % (name, doc) if doc else name

            test = {
                'summary': {
                    'desc': desc,
                    'count': np + nf + ne + ns,
                    'pass': np,
                    'fail': nf,
                    'error': ne,
                    'skip': ns,
                    'cid': 'testclass%s' % cid,
                    'status': (ne and self.STATUS[2]) or (nf and self.STATUS[1]) or (ns and self.STATUS[3]) or self.STATUS[0]
                }, 'detail': []
            }

            for tid, (n, t, o, e) in enumerate(cls_results, 1):
                test['detail'].append(self._generate_report_test(cid, tid, n, t, o, e))

            tests.append(test)

        return {
            'tests': tests,
            'count': str(result.success_count + result.failure_count + result.error_count + result.skip_count),
            'pass': str(result.success_count),
            'fail': str(result.failure_count),
            'error': str(result.error_count),
            'skip': str(result.skip_count),
            'suite_count': len(sorted_result)
        }

    def _generate_report_test(self, cid, tid, n, t, o, e):
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool(o or e)
        tid = 'test%s.%s.%s' % (self.STATUS[n], cid, tid)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name

        uo = o if isinstance(o, str) else o.decode('utf-8')
        ue = e if isinstance(e, str) else e.decode('utf-8')

        return {
            'has_output': has_output,
            'tid': tid,
            'desc': desc,
            'output': saxutils.escape(str(uo) + str(ue)),
            'status': self.STATUS[n],
            'status_code': n
        }

    @staticmethod
    def sort_result(result_list):
        rmap = {}
        for n, t, o, e in result_list:
            cls = t.__class__
            rmap.setdefault(cls, []).append((n, t, o, e))
        return rmap.items()



class TestProgram(unittest.TestProgram):


    def runTests(self):
        fp = None
        if self.testRunner is None:
            fp = open('report/GLR Automation Test Report.html', 'wb')
            self.testRunner = HTMLTestRunner(fp, verbosity=self.verbosity)
        unittest.TestProgram.runTests(self)
        if fp:
            fp.close()


main = TestProgram

if __name__ == "__main__":
    main(module=None)
