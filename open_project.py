#!/usr/bin/python
# encoding: utf-8

#icon size 200%
#icon dimensions w:63 h:60

import sys

from workflow import Workflow, ICON_WEB

log = None


projects = []
with open('projects_list.txt', 'r') as f:
    header = f.readline()
    for l in f:
        ln = l.strip().split()
        projects.append({
            "id": ln[0],
            "name": " ".join(ln[1:-1]),
            "number": ln[-1],
            "search": " ".join(ln).upper()
        })


def main(wf):
    # The Workflow instance will be passed to the function
    # you call from `Workflow.run`

    # Get args from Workflow as normalized Unicode
    args = wf.args

    # Add an item to Alfred feedback

    selected_project = [p for p in projects if p['id'] == args[0].split(' ')[0]]

    if len(selected_project) == 1:
        search = None
        if len(args[0].split(' ')) > 1:
            search = " ".join(args[0].split(' ')[1:]).lower()
        proj = selected_project[0]
        url = "https://console.cloud.google.com/home?project=%s" % proj['id']
        title = "Home/Dashboard"
        links = [
            {
                'url': 'home',
                'title': 'Home / Dashboard',
                'icon': 'ICONS/HOME.png'
            },
            {
                'url': 'appengine',
                'title': 'App Engine',
                'icon': 'ICONS/APPENGINE.png'
            },
            {
                'url': 'compute',
                'title': 'Compute Engine',
                'icon': 'ICONS/COMPUTE.png'
            },
            {
                'url': 'billing',
                'title': 'Billing',
                'icon': 'ICONS/BILLING.png'
            },
            {
                'url': 'kubernets',
                'title': 'Container Engine',
                'icon': 'ICONS/DATASTORE.png'
            },
            {
                'url': 'datastore',
                'title': 'Datastore',
                'icon': 'ICONS/COMPUTE.png'
            },
            {
                'url': 'logs',
                'title': 'Logging',
                'icon': 'ICONS/LOGGING.png'
            },
            {
                'url': 'networking',
                'title': 'Networking',
                'icon': 'ICONS/NETWORKING.png'
            },
        ]
        for link in links:
            if not search or search in link['title'].lower():
                wf.add_item(
                    link['title'], 
                    proj['name'],
                    icon=link['icon'],
                    valid=True,
                    arg="https://console.cloud.google.com/%s?project=%s" % (link['url'], proj['id'])
                )
    else:
        for proj in [p for p in projects if args[0].upper() in p['search']]:
            wf.add_item(
                proj['name'], 
                "%s (%s)" % (proj['id'], proj['number']),
                icon='ICONS/GCP.png',
                uid=proj['id'],
                autocomplete=proj['id'] + " ",
                arg="https://console.cloud.google.com/home/dashboard?project=%s" % proj['id']
            )

    # Send output to Alfred
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))