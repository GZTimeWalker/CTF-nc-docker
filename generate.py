import os
import json

CONFIG = {
    "mirrors_base_url": "mirrors.tuna.tsinghua.edu.cn",
    "port_range_start": 65100
}

def init():
    if not os.path.exists('problems'):
        os.makedirs('problems')
        print('Please put your problems in ./problems/')
        print('You can find examples at https://github.com/GZTimeWalker/CTF-nc-docker')

    if not os.path.exists('template'):
        print('No template available!')
        exit(1)
    else:
        requires = ['Dockerfile','docker-compose.yml','xinetd','config.json']
        for root, _, files in os.walk('template'):
            for file in requires:
                if file not in files:
                    print(f'Template file {os.path.join(root,file)} not found!')
                    exit(1)

    if os.path.exists('global.json'):
        with open('global.json','r') as f:
            CONFIG.update(json.load(f))

def get_problems():
    problems = []
    for root, dirs, _ in os.walk('problems'):
        for problem in dirs:
            if not os.path.exists(os.path.join(root, problem, 'config.json')):
                with open('template/config.json','r') as default_config:
                    with open(os.path.join(root, problem, 'config.json'),'w') as f:
                        f.write(default_config.read())
            else:
                with open(os.path.join(root, problem, 'config.json'),'r') as f:
                    p = {'name': problem}
                    p.update(json.load(f))
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
    dockerfile_data = {
        'mirrors_base_url': CONFIG['mirrors_base_url'],
        'apt_requirements': '',
        'extra_cmd': '',
        'copy_problem_cmd': '',
        'run_scripts': ''
    }

    for problem in problems:
        
        if not problem['enable']:
            continue

        if len(problem['apt_requirements']) > 0:
            dockerfile_data['apt_requirements'] += f"# ==> for {problem['name']}\n"
            dockerfile_data['apt_requirements'] += f"RUN apt -y install {' '.join(problem['apt_requirements'])}\n"

        if len(problem['extra_cmd']) > 0:
            dockerfile_data['extra_cmd'] += f"# ==> for {problem['name']}\n"
            for cmd in problem['extra_cmd']:
                dockerfile_data['extra_cmd'] += f"RUN {cmd}\n"

        if problem['all_copy'] or len(problem['copy_files']) > 0:
            dockerfile_data['copy_problem_cmd'] += f"# ==> for {problem['name']}\n"
            if problem['all_copy']:
                for item in get_all_files(os.path.join('problems',problem['name'])):
                    dockerfile_data['copy_problem_cmd'] += f"COPY {item} /home/ctf/{item.replace('problems/','')}\n"
            else:
                for item in problem['copy_files']:
                    dockerfile_data['copy_problem_cmd'] += f"COPY problems/{problem['name']}/{item} /home/ctf/{problem['name']}/{item}\n"

        script = f"cd /home/ctf/{problem['name']}\\n{problem['launch']} {' '.join(problem['args'])}\\n"
        dockerfile_data['run_scripts'] += f"RUN echo \'{script}\' > /home/ctf/run/{problem['name']}.sh\n"


    with open('template/Dockerfile','r') as f:
        template = f.read()

    with open('Dockerfile','w') as f:
        f.write(template.format(**dockerfile_data))

def generate_xinetd(problems):
    port = CONFIG['port_range_start']

    with open('template/xinetd','r') as f:
        template = f.read()

    with open('xinetd','wb') as f:
        for problem in problems:
            f.write((template % (port, problem['name'])).encode())
            f.write(b'\n\n')
            port = port + 1

def generate_dockercompose(problems):
    with open('template/docker-compose.yml','r') as f:
        template = f.read()

    data = ''
    port = CONFIG['port_range_start']
    for i in range(len(problems)):
        data += f"- {port + i}:{port + i}\n      "

    with open('docker-compose.yml','w') as f:
        f.write(template % data)

if __name__ == "__main__":
    init()
    problems = get_problems()
    if(len(problems) == 0):
        print('No problem found!')
        exit(1)
    generate_dockerfile(problems)
    generate_xinetd(problems)
    generate_dockercompose(problems)
    os.system('docker compose up -d --build')
