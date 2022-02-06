import os
import json
import string
import random

alphabet = sorted(string.digits + string.ascii_letters)

CONFIG = {
    "mirrors_base_url": "mirrors.tuna.tsinghua.edu.cn",
    "pypi_index_url": "https://pypi.tuna.tsinghua.edu.cn/simple",
    "npm_mirror_url": "http://registry.npmmirror.com/",
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

VERSION = ' 2.1.5 '

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

    if not os.path.exists('challenges'):
        os.makedirs('challenges')
        print('[+] Please put your challenges in ./challenges/')
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

def get_challenges():
    challenges = []
    for challenge in os.listdir('challenges'):
        if not os.path.isdir(os.path.join('challenges', challenge)):
            continue
        if not os.path.exists(os.path.join('challenges', challenge, 'config.json')):
            with open('template/config.json','r') as default_config:
                with open(os.path.join('challenges', challenge, 'config.json'),'w') as f:
                    f.write(default_config.read())
        else:
            with open(os.path.join('challenges', challenge, 'config.json'),'r', encoding='utf-8') as f:
                p = {
                    'name': challenge.replace(' ','_').replace('-','_'),
                    'dir': ''.join([random.choice(alphabet) for _ in range(16)])
                }
                p.update(json.load(f))
                if p['enable']:
                    challenges.append(p)
    return challenges

def get_all_files(path):
    files_ = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file != 'config.json':
                files_.append(os.path.join(root, file).replace('\\', '/'))
        for dir_ in dirs:
            files_ += get_all_files(os.path.join(root, dir_))
    return files_

def generate_dockerfile(challenges):
    print(f'[+] Generating Dockerfile...')

    dockerfile_data = {
        'mirrors_base_url': CONFIG['mirrors_base_url'],
        'pypi_index': '' if CONFIG['pypi_index_url'] == '' else f"-i {CONFIG['pypi_index_url']}",
        'npm_mirror_url': CONFIG['npm_mirror_url'],
        'extra_cmd': '',
        'copy_challenge_cmd': '',
        'copy_dirs': [],
        'chmod_cmd': '',
        'chmod_cmds': [],
        'pip_requirements': '',
        'node_server': '',
        'pip_list': [],
    }

    for challenge in challenges:
        dockerfile_data['pip_list'] += challenge['pip_requirements']

        if len(challenge['extra_cmd']) > 0:
            dockerfile_data['extra_cmd'] += f"# ==> for {challenge['name']}\n"
            for cmd in challenge['extra_cmd']:
                dockerfile_data['extra_cmd'] += f"RUN {cmd}\n"

        if challenge['all_copy'] or len(challenge['copy_files']) > 0:
            dockerfile_data['copy_challenge_cmd'] += f"# ==> for {challenge['name']}\n"
            if challenge['all_copy']:
                items = get_all_files(os.path.join('challenges',challenge['name']))
            else:
                items = [f"challenges/{challenge['name']}/" + i for i in challenge['copy_files']]
            dest = f"{challenge['dir']}/"
            dockerfile_data['copy_challenge_cmd'] += f"COPY {' '.join(items)} {dest}\n"

        script = f"#!/bin/sh\n\ncd /home/ctf/{challenge['dir']}\n"

        if CONFIG['show_echo_msg'] and len(challenge['echo_msg']) > 0:
            script += "echo \'\\e[32m{}\\e[0m\'\n".format((' \\e[33m' + challenge['name'] + ' \\e[32m').center(72,'='))

            if CONFIG['show_warn_msg']:
                script += "echo \'\\e[32m!!!  \\e[31m此环境为测试训练环境，安全性较弱，请勿执行恶意代码  \\e[32m!!!\\e[0m\'\n"
                script += "echo \'\\e[32m!!!   \\e[31mDO NOT EXECUTE HARMFUL CODE IN THIS TRAINING ENV   \\e[32m!!!\\e[0m\'\n"
                script += "echo \'\\e[32m{}\\e[0m\'\n".format('=' * 60)

            for item in challenge['echo_msg']:
                script += f"echo \'{item}\'\n"

            if challenge['download_file_name'] != "":
                script += f"echo \'题目附件：/{challenge['download_file_name']}\'\n"
            script += "echo \'\\e[32m{}\\e[0m\'\n".format('=' * 60)
            script += "echo \'\'\n"

        script += f"{challenge['launch']} {' '.join(challenge['args'])}\n"

        with open(f"tmp/run/{challenge['dir']}.sh",'wb') as f:
            f.write(script.encode())

        dockerfile_data['chmod_cmds'].append(f"chmod 755 /home/ctf/run/{challenge['dir']}.sh")
        dockerfile_data['chmod_cmds'].append(f"chmod -R 755 /home/ctf/{challenge['dir']}")

    if len(dockerfile_data['pip_list']) > 0:
        dockerfile_data['pip_requirements'] = ' '.join(dockerfile_data['pip_list'])
    else:
        dockerfile_data['pip_requirements'] = 'pip'

    template_name = 'Dockerfile'

    # choose one server
    if CONFIG['web_netcat_server']:
        dockerfile_data['node_server'] += "COPY web/webnc /build/\n"
        dockerfile_data['node_server'] += "COPY web/src/webnc /src/\n"
        dockerfile_data['node_server'] += "RUN cd /src && npm i --verbose && npm run build &&\\\n"
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

def generate_start_sh(challenges):
    print(f'[+] Generating launch script...')

    template = '#!/bin/sh\n\n'

    if CONFIG['web_netcat_server']:
        template += 'cd /home/ctf/web\n'
        template += f'nohup node server.js {CONFIG["server_port"]} '
        template += f'{CONFIG["port_range_start"]}-{CONFIG["port_range_start"] + len(challenges) - 1} '
        template += f'> /var/log/server.log 2>&1 &\n'
    elif CONFIG['download_server']:
        template += 'cd /home/ctf/web\n'
        template += f'nohup node server.js {CONFIG["server_port"]} > /var/log/server.log 2>&1 &\n'

    template += 'cd / && xinetd -dontfork'
    with open('tmp/start.sh','wb') as f:
        f.write(template.encode())

def generate_index(challenges):
    print(f'[+] Generating web index...')

    port = CONFIG['port_range_start']
    index_data = ""

    for challenge in challenges:
        row = f'<tr><td>{challenge["name"]}</td><td><code>{port}</code></td></tr>'
        port = port + 1
        index_data += row

    with open('template/index.html','r') as f:
        template = f.read()

    with open('tmp/index.html','wb') as f:
        template = template.replace('{challenges_trs}', index_data)
        if CONFIG['web_netcat_server']:
            template = template.replace('{web_netcat_link}', '<p> Web netcat: <a href="/wnc"><code><span class="url"></span>/wnc</code></a></p>')
        else:
            template = template.replace('{web_netcat_link}', '')
        f.write(template.encode())

def generate_xinetd(challenges):
    print(f'[+] Generating xinetd config...')

    port = CONFIG['port_range_start']

    with open('template/xinetd','r') as f:
        template = f.read()

    with open('xinetd','wb') as f:
        for challenge in challenges:
            challenge_data = {
                'port': port,
                'challenge_name': challenge['name'],
                'challenge_alian': challenge['dir']
            }

            f.write(template.format(**challenge_data).encode())
            f.write(b'\n\n')
            port += 1

def generate_dockercompose(challenges):
    dockercompose_data = {}

    print(f'[+] Generating docker-compose.yml...')

    with open('template/docker-compose.yml','r') as f:
        template = f.read()

    ports = ''
    port = CONFIG['port_range_start']
    ports += f'- "{port}-{port + len(challenges) - 1}:{port}-{port + len(challenges) - 1}"\n      '
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
    challenges = get_challenges()

    if(len(challenges) == 0):
        print('[!] No challenge found!')
        exit(1)

    print(f'[+] Loaded {len(challenges)} challenges')

    generate_start_sh(challenges)
    generate_index(challenges)
    generate_dockerfile(challenges)
    generate_xinetd(challenges)
    generate_dockercompose(challenges)

    ret = os.system('docker-compose --compatibility up --build -d')

    if ret != 0:
        print('[!] Error occured, exiting...')
        exit(ret)

    print('[+] Successfully generated CTF-NC container.')
    print('[+] Your challenges are now available at following ports:')

    port = CONFIG['port_range_start']
    for challenge in challenges:
        print(f" => [{port}] => {challenge['name']}")
        port = port + 1

    if CONFIG['download_server']:
        print(f'[+] Your web page is now available at http://localhost:{CONFIG["server_port"]}.')

    if CONFIG['web_netcat_server']:
        print(f'[+] Your web netcat is now available at http://localhost:{CONFIG["server_port"]}/wnc.')
