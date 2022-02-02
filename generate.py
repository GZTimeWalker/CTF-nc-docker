import os
import json
import string
import random

alphabet = sorted(string.digits + string.ascii_letters)

CONFIG = {
    "mirrors_base_url": "mirrors.tuna.tsinghua.edu.cn",
    "pypi_index_url": "https://pypi.tuna.tsinghua.edu.cn/simple",
    "port_range_start": 65100,
    "download_port": 65199,
    "hostname": "localhost",
    "download_server": True,
    "show_echo_msg": True,
    "show_warn_msg": True
}

HELLO = r'''
  ______   ________  ________       __    __   ______
 /      \ /        |/        |     /  \  /  | /      \
/$$$$$$  |$$$$$$$$/ $$$$$$$$/      $$  \ $$ |/$$$$$$  |
$$ |  $$/    $$ |   $$ |__  ______ $$$  \$$ |$$ |  $$/
$$ |         $$ |   $$    |/      |$$$$  $$ |$$ |
$$ |   __    $$ |   $$$$$/ $$$$$$/ $$ $$ $$ |$$ |   __
$$ \__/  |   $$ |   $$ |           $$ |$$$$ |$$ \__/  |
$$    $$/    $$ |   $$ |           $$ | $$$ |$$    $$/
 $$$$$$/     $$/    $$/            $$/   $$/  $$$$$$/
'''.split('\n')

VERSION = ' 0.1.0 '

def init():

    col, _ = os.get_terminal_size()
    print('=' * col)
    print('\n'.join(i.ljust(56).center(col) for i in HELLO))
    print(VERSION.center(col, '='))

    if not os.path.exists('tmp/run'):
        os.makedirs('tmp/run')
    else:
        for root, _, files in os.walk('tmp'):
            for file in files:
                os.remove(os.path.join(root,file))

    if not os.path.exists('global.json'):
        with open('template/global.json','r') as f:
            with open('global.json','w') as g:
                g.write(f.read())
        print('[+] Please edit your custom config in global.json')
    else:
        with open('global.json','r') as f:
            CONFIG.update(json.load(f))

    if not os.path.exists('problems'):
        os.makedirs('problems')
        print('[+] Please put your problems in ./problems/')
        print('[+] You can find examples at https://github.com/GZTimeWalker/CTF-nc-docker')

    if not os.path.exists('attachments'):
        os.makedirs('attachments')

    if not os.path.exists('template'):
        print('[!] No template available!')
        exit(1)
    else:
        requires = ['Dockerfile','docker-compose.yml','xinetd','config.json']
        for root, _, files in os.walk('template'):
            for file in requires:
                if file not in files:
                    print(f'Template file {os.path.join(root,file)} not found!')
                    exit(1)

def get_problems():
    problems = []
    for problem in os.listdir('problems'):
        if not os.path.isdir(os.path.join('problems', problem)):
            continue
        if not os.path.exists(os.path.join('problems', problem, 'config.json')):
            with open('template/config.json','r') as default_config:
                with open(os.path.join('problems', problem, 'config.json'),'w') as f:
                    f.write(default_config.read())
        else:
            with open(os.path.join('problems', problem, 'config.json'),'r', encoding='utf-8') as f:
                p = {
                    'name': problem.replace(' ','_').replace('-','_'),
                    'dir': ''.join([random.choice(alphabet) for _ in range(16)])
                }
                p.update(json.load(f))
                if p['enable']:
                    problems.append(p)
    return problems

def get_all_files(path):
    files_ = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file != 'config.json':
                files_.append(os.path.join(root, file).replace('\\', '/'))
        for dir_ in dirs:
            files_ += get_all_files(os.path.join(root, dir_))
    return files_

def generate_dockerfile(problems):
    print(f'[+] Generating Dockerfile...')
    dockerfile_data = {
        'mirrors_base_url': CONFIG['mirrors_base_url'],
        'pypi_index': '' if CONFIG['pypi_index_url'] == '' else f"-i {CONFIG['pypi_index_url']}",
        'extra_cmd': '',
        'copy_problem_cmd': '',
        'copy_dirs': [],
        'chmod_cmd': '',
        'chmod_cmds': [],
        'pip_requirements': '',
        'pip_list': [],
    }

    for problem in problems:

        dockerfile_data['pip_list'] += problem['pip_requirements']

        if len(problem['extra_cmd']) > 0:
            dockerfile_data['extra_cmd'] += f"# ==> for {problem['name']}\n"
            for cmd in problem['extra_cmd']:
                dockerfile_data['extra_cmd'] += f"RUN {cmd}\n"

        if problem['all_copy'] or len(problem['copy_files']) > 0:
            dockerfile_data['copy_problem_cmd'] += f"# ==> for {problem['name']}\n"
            if problem['all_copy']:
                items = get_all_files(os.path.join('problems',problem['name']))
            else:
                items = [f"problems/{problem['name']}/" + i for i in problem['copy_files']]
            dest = f"{problem['dir']}/"
            dockerfile_data['copy_problem_cmd'] += f"COPY {' '.join(items)} {dest}\n"

        script = f"#!/bin/sh\n\ncd /home/ctf/{problem['dir']}\n"

        if CONFIG['show_echo_msg'] and len(problem['echo_msg']) > 0:
            script += "echo \'\\e[32m{}\\e[0m\'\n".format((' \\e[33m' + problem['name'] + ' \\e[32m').center(72,'='))

            if CONFIG['show_warn_msg']:
                script += "echo \'\\e[32m!!!  \\e[31m此环境为测试训练环境，安全性较弱，请勿执行恶意代码  \\e[32m!!!\\e[0m\'\n"
                script += "echo \'\\e[32m!!!   \\e[31mDO NOT EXECUTE HARMFUL CODE IN THIS TRAINING ENV   \\e[32m!!!\\e[0m\'\n"
                script += "echo \'\\e[32m{}\\e[0m\'\n".format('=' * 60)

            for item in problem['echo_msg']:
                script += f"echo \'{item}\'\n"

            if problem['download_file_name'] != "":
                script += f"echo \'题目附件：http://{CONFIG['hostname']}:{CONFIG['download_port']}/{problem['download_file_name']}\'\n"
            script += "echo \'\\e[32m{}\\e[0m\'\n".format('=' * 60)
            script += "echo \'\'\n"

        script += f"{problem['launch']} {' '.join(problem['args'])}\n"

        with open(f"tmp/run/{problem['dir']}.sh",'wb') as f:
            f.write(script.encode())

        dockerfile_data['chmod_cmds'].append(f"chmod 755 /home/ctf/run/{problem['dir']}.sh")
        dockerfile_data['chmod_cmds'].append(f"chmod -R 755 /home/ctf/{problem['dir']}")

    if len(dockerfile_data['pip_list']) > 0:
        dockerfile_data['pip_requirements'] = ' '.join(dockerfile_data['pip_list'])
    else:
        dockerfile_data['pip_requirements'] = 'pip'

    dockerfile_data['chmod_cmd'] = "RUN " + ' && \\\n '.join(dockerfile_data['chmod_cmds'])

    with open('template/Dockerfile','r') as f:
        template = f.read()

    with open('Dockerfile','wb') as f:
        f.write(template.format(**dockerfile_data).encode())

def generate_start_sh():
    print(f'[+] Generating launch script...')

    template = '#!/bin/sh\n\n'

    if CONFIG['download_server']:
        template += 'cd /home/ctf/files\n'
        template += f'nohup python3 -m http.server {CONFIG["download_port"]} > /var/log/file.log 2>&1 &\n'

    template += 'cd / && xinetd -dontfork'
    with open('tmp/start.sh','wb') as f:
        f.write(template.encode())

def generate_index(problems):
    print(f'[+] Generating web index...')

    port = CONFIG['port_range_start']
    index_data = ""

    for problem in problems:

        row = f'<tr><td>{problem["name"]}</td><td><code>nc <span class="hostname"></span> {port}</code></td></tr>'
        port = port + 1
        index_data += row + '\n'

    with open('template/index.html','r') as f:
        template = f.read()

    with open('tmp/index.html','wb') as f:
        f.write(template.replace('{problems_trs}', index_data).encode())

def generate_xinetd(problems):
    print(f'[+] Generating xinetd config...')

    port = CONFIG['port_range_start']

    with open('template/xinetd','r') as f:
        template = f.read()

    with open('xinetd','wb') as f:
        for problem in problems:

            problem_data = {
                'port': port,
                'problem_name': problem['name'],
                'problem_alian': problem['dir']
            }

            f.write(template.format(**problem_data).encode())
            f.write(b'\n\n')
            port += 1

def generate_dockercompose(problems):
    print(f'[+] Generating docker-compose.yml...')

    with open('template/docker-compose.yml','r') as f:
        template = f.read()

    data = ''
    port = CONFIG['port_range_start']

    for _ in problems:
        data += f"- {port}:{port}\n      "
        port = port + 1

    port = CONFIG['download_port']
    data += f"- {port}:{port}\n      "

    with open('docker-compose.yml','w') as f:
        f.write(template % data)

if __name__ == "__main__":
    init()
    problems = get_problems()
    if(len(problems) == 0):
        print('[!] No problem found!')
        exit(1)

    print(f'[+] Loded {len(problems)} problems')

    generate_start_sh()
    generate_index(problems)
    generate_dockerfile(problems)
    generate_xinetd(problems)
    generate_dockercompose(problems)

    ret = os.system('docker-compose --compatibility up --build -d')

    if ret != 0:
        print('[!] Error occured, exiting...')
        exit(0)

    print('[+] Successfully generated CTF-NC container.')
    print('[+] Your problems are now available at following ports:')
    port = CONFIG['port_range_start']
    for problem in problems:

        print(f" => [{port}] => {problem['name']}")
        port = port + 1

    if CONFIG['download_server']:
        print(f'[+] Your web page is now available at http://{CONFIG["hostname"]}:{CONFIG["download_port"]}.')
