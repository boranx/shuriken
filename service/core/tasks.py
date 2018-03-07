from __future__ import absolute_import, unicode_literals
from subprocess import Popen, PIPE, STDOUT
from core import celery


@celery.task(bind=True)
def cmd_runner(self, cmd, type='runner'):
    output = ""
    self.update_state(state='PROGRESS',
                      meta={'output': output,
                            'hostname': "",
                            'description': "",
                            'returncode': None})
    proc = Popen([cmd], stdout=PIPE, stderr=STDOUT, shell=True)
    for line in iter(proc.stdout.readline, ''):
        print str(line)
        output = output + line
        self.update_state(state='PROGRESS', meta={
            'output': output, 'hostname': self.request.hostname, 'description': "", 'returncode': None})

    return_code = proc.poll()
    if return_code is 0:
        meta = {'output': output,
                'hostname': self.request.hostname,
                'returncode': proc.returncode,
                'description': "Task run successfully"
               }
        self.update_state(state='FINISHED',
                          meta=meta)
    elif return_code is not 0:
        # failure
        meta = {'output': output,
                'hostname': self.request.hostname,
                'returncode': return_code,
                'description': unicode.format("Celery ran the task, but {0} reported error", type)
               }
        self.update_state(state='FAILED',
                          meta=meta)
    if len(output) is 0:
        output = "no output, maybe no matching hosts?"
        meta = {'output': output,
                'hostname': self.request.hostname,
                'returncode': return_code,
                'description': unicode.format("Celery ran the task, but {0} reported error", type)
               }
    return meta
