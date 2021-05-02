import subprocess
import threading
import os

def test_stdout():
    while True:
        # occupiedProcess.acquire()

        # def read():
        print(p.stdout.readline().decode('utf8'), end='')
        p.stdout.flush()

        # m = Process(target=read)
        # m.start()
        # m.join(timeout=1)

        # occupiedProcess.release()

def test_stderr():
    while True:
        print(p.stderr.readline().decode('utf8'), end='')
        p.stderr.flush()

os.chdir('.\\fairgame-master')

# p = subprocess.Popen('py -3.8 -m pipenv run py app.py amazon',
#                      stdin=subprocess.PIPE,
#                      stdout=subprocess.PIPE)
# p = subprocess.Popen('py -3.8 -m pipenv run py app.py amazon')
p = subprocess.Popen('py -3.8 -m pipenv run py app.py amazon', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# p = subprocess.Popen('py test_file.py', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# threading.Thread(target=test_stdout, daemon=True).start()

# occupiedProcess = threading.Lock()

# occupiedProcess.acquire()

# p.stdin.write(b'woohooo\n')
# p.stdin.flush()

# occupiedProcess.release()

# print('Waiting on stderr')
# stderr = p.stderr.readline()
# p.stderr.flush()
# if stderr:
#     print(stderr.decode('utf8'), end='')

print('Waiting on stdout')
stdout = p.stdout.readline()
p.stdout.flush()
if stdout:
    print(stdout.decode('utf8'), end='')
# print(p.stdout.readline().decode('utf8'), end='')
# p.stdout.flush()

# out, _ = p.communicate(s.encode())
# print(out.decode('utf8'))
