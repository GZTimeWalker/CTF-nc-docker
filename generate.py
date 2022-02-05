import os
import json
import string
import random

alphabet = sorted(string.digits + string.ascii_letters)

CONFIG = {
    "mirrors_base_url": "mirrors.tuna.tsinghua.edu.cn",
    "pypi_index_url": "https://pypi.tuna.tsinghua.edu.cn/simple",
    "npm_mirror_url": "http://registry.npmmirror.com/",
    "hostname": "localhost",
    "port_range_start": 65100,
    "download_server": True,
    "web_netcat_server": True,
    "server_port": 65199,
    "show_echo_msg": True,
    "show_warn_msg": True,
    "resource_limit": {
        "enable": True,
        "max_memory": "512M",
        "max_cpu": "0.5"
    }
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

VERSION = ' 2.0.2 '

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
        requires = ['Dockerfile','Dockerfile.build','docker-compose.yml','xinetd','config.json','index.html','global.json']
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
        'npm_mirror_url': CONFIG['npm_mirror_url'],
        'extra_cmd': '',
        'copy_problem_cmd': '',
        'copy_dirs': [],
        'chmod_cmd': '',
        'chmod_cmds': [],
        'pip_requirements': '',
        'node_server': '',
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
                script += f"echo \'题目附件：/{problem['download_file_name']}\'\n"
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

    template_name = 'Dockerfile'

    # choose one server
    if CONFIG['web_netcat_server']:
        dockerfile_data['node_server'] += "COPY web/webnc /build/\n"
        dockerfile_data['node_server'] += "COPY web/src/webnc /src/\n"
        dockerfile_data['node_server'] += "RUN cd /src && npm i && npm run build &&\\\n"
        dockerfile_data['node_server'] += "    mkdir -p /build/static/wnc && mv /src/build/* /build/static/wnc\n"
    elif CONFIG['download_server']:
        dockerfile_data['node_server'] += "COPY web/fileonly /build/\n"

    if CONFIG['web_netcat_server'] or CONFIG['download_server']:
        template_name = 'Dockerfile.build'

    if CONFIG['download_server']:
        dockerfile_data['node_server'] += "COPY tmp/index.html attachments /build/static/\n"

    dockerfile_data['chmod_cmd'] = "RUN " + ' && \\\n '.join(dockerfile_data['chmod_cmds'])

    with open(f'template/{template_name}','r') as f:
        template = f.read()

    with open('Dockerfile','wb') as f:
        f.write(template.format(**dockerfile_data).encode())

def generate_start_sh(problems):
    print(f'[+] Generating launch script...')

    template = '#!/bin/sh\n\n'

    if CONFIG['web_netcat_server']:
        template += 'cd /home/ctf/web\n'
        template += f'nohup node server.js {CONFIG["server_port"]} '
        template += f'{CONFIG["port_range_start"]}-{CONFIG["port_range_start"] + len(problems) - 1} '
        template += f'> /var/log/server.log 2>&1 &\n'
    elif CONFIG['download_server']:
        template += 'cd /home/ctf/web\n'
        template += f'nohup node server.js {CONFIG["server_port"]} > /var/log/server.log 2>&1 &\n'

    template += 'cd / && xinetd -dontfork'
    with open('tmp/start.sh','wb') as f:
        f.write(template.encode())

def generate_index(problems):
    print(f'[+] Generating web index...')

    port = CONFIG['port_range_start']
    index_data = ""

    for problem in problems:
        row = f'<tr><td>{problem["name"]}</td><td><code>{port}</code></td></tr>'
        port = port + 1
        index_data += row

    with open('template/index.html','r') as f:
        template = f.read()

    with open('tmp/index.html','wb') as f:
        template = template.replace('{problems_trs}', index_data)
        if CONFIG['web_netcat_server']:
            template = template.replace('{web_netcat_link}', '<p> Web netcat: <code><span class="url"></span>/wnc</code></p>')
        else:
            template = template.replace('{web_netcat_link}', '')
        f.write(template.encode())

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
    dockercompose_data = {}

    print(f'[+] Generating docker-compose.yml...')

    with open('template/docker-compose.yml','r') as f:
        template = f.read()

    ports = ''
    port = CONFIG['port_range_start']
    ports += f'- "{port}-{port + len(problems) - 1}:{port}-{port + len(problems) - 1}"\n      '
    port = CONFIG['server_port']
    ports += f'- "{port}:{port}"'

    dockercompose_data['ports'] = ports

    res_lim = ''

    if CONFIG['resource_limit']['enable']:
        res_lim += 'deploy:\n      resources:\n        limits:\n'
        res_lim += f'          cpus: "{CONFIG["resource_limit"]["max_cpu"]}"\n'
        print(f'[+] Container CPU limit: {CONFIG["resource_limit"]["max_cpu"]}')
        res_lim += f'          memory: "{CONFIG["resource_limit"]["max_memory"]}"\n'
        print(f'[+] Container Memory limit: {CONFIG["resource_limit"]["max_memory"]}')

    dockercompose_data['resource_limit'] = res_lim

    with open('docker-compose.yml','w') as f:
        f.write(template.format(**dockercompose_data))

if __name__ == "__main__":
    init()
    problems = get_problems()

    if(len(problems) == 0):
        print('[!] No problem found!')
        exit(1)

    print(f'[+] Loaded {len(problems)} problems')

    generate_start_sh(problems)
    generate_index(problems)
    generate_dockerfile(problems)
    generate_xinetd(problems)
    generate_dockercompose(problems)

    ret = os.system('docker-compose --compatibility up --build -d')

    if ret != 0:
        print('[!] Error occured, exiting...')
        exit(ret)

    print('[+] Successfully generated CTF-NC container.')
    print('[+] Your problems are now available at following ports:')

    port = CONFIG['port_range_start']
    for problem in problems:
        print(f" => [{port}] => {problem['name']}")
        port = port + 1

    if CONFIG['download_server']:
        print(f'[+] Your web page is now available at http://{CONFIG["hostname"]}:{CONFIG["server_port"]}.')

    if CONFIG['web_netcat_server']:
        print(f'[+] Your web netcat is now available at http://{CONFIG["hostname"]}:{CONFIG["server_port"]}/wnc.')
