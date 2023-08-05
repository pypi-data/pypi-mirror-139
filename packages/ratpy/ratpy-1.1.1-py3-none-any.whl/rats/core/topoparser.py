import platform
import pathlib
from bs4 import BeautifulSoup as bs

if platform.system() == 'Windows':
    topopath = '\\topo\\'
else:
    topopath = '/topo/'
packagepath = pathlib.Path(__file__).parent.parent.resolve()


def extractscale(instanceName, edblist):
    edbs = [i for i in edblist] # stop this modifying core attribute of class
    # need to organically identify the topo file
    # print(f'EDBLIST: {edblist}')
    import os
    for filename in os.listdir(str(packagepath) + topopath):
        if 'topology' in filename.lower() and 'xml' in filename:
            topofile = filename

    print(str(packagepath) + topopath + topofile)
    with open(str(packagepath) + topopath + topofile, 'r') as f:
        content = f.readlines()
        content = "".join(content)
        soup = bs(content, 'lxml')
        # print('MADE SOUP')
    device = soup.find('de:device', {'instancename': instanceName})
    print('='*12)
    print(device)
    board = device['instancename']
    description = {}
    units = {}
    minimum = {}
    maximum = {}

    with open(str(packagepath) + topopath + f'DEVICE_{device["type"]}_{device["variant"]}.xml', 'r') as f:
        content = f.readlines()
        content = "".join(content)
        soup = bs(content, 'lxml')

    for edb in edbs:
        addr42 = soup.find('ep:interfaceaddress', {'addr': '42'})
        data = addr42.find('is:setting', {'id': edb})
        description[edb] = data['description']
        units[edb] = data['unit']
        minimum[edb] = int(data['minvalue'])
        maximum[edb] = int(data['maxvalue'])

    scalingfactors = dict(descriptions=description, units=units, minimum=minimum, maximum=maximum)
    print('scaling factors determined')

    return scalingfactors


def testcase(netid, e):
    output = extractscale(netid, e)
    return output

# testcase('ION_GUIDE', [1,3])



