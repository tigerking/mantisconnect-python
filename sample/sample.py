# -*- coding: utf-8 -*-

import sys
# from mantisconnect2.simple_project import Issue
from mantisconnect2.simple_project import SimpleProject
from mantisconnect2.connector_interface import create_mantis_soap_connector

def more_test(mc):
    # Must use project name in mantis
    p = SimpleProject(mc, "ATS")

    filter_name = "ATB"

    # Get issue object list
    # see Issue class (mantisconnect/project.py)
    issue_list = p.request_filter_all_issues(filter_name, 10)

    # Write your code
    #
    for issue in issue_list:
        print("{0} {1}".format(issue.issue_id, issue.summary))


if __name__ == "__main__":

    if sys.version[0] < 3:
        reload(sys)
        sys.setdefaultencoding('utf8')
    
    url = "https://your.mantis.com/api/soap/mantisconnect.php?wsdl"
    username = "mantis_user"
    password = "mantis_password"

    mc = create_mantis_soap_connector(url)
    mc.set_user_passwd(username, password)
    mc.connect()

    print("Connent %s" % url)
    print("Mantis SOAP MC Version:" + mc.version)

    project = mc.find_project(1)
    print(project)

    DIV_LINE ='\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n'
    print(DIV_LINE)
    
    project = mc.find_project('ATS')
    print(project)
    print(DIV_LINE)
    
    print('priorities = {}'.format(mc.request_enum_priorities()))
    print(DIV_LINE)

    print('resolutions = {}'.format(mc.request_enum_resolutions()))
    print(DIV_LINE)

    print('projects ATS = {}'.format(mc.request_project('ATS')))
    print(DIV_LINE)

    issue = mc.request_issue_get(10)
    print('# issue 10 = {}'.format(issue))
    print(DIV_LINE)

    response = mc.get_categories(project='ATS')
    print(response)
    print(DIV_LINE)

    # response = mc.create_new_issue('summary demo 002', project=1, description='I am description demo 002')
    # print(response)
    # print(DIV_LINE)

    # legacy test code
    # more_test(mc)

    print('### done ###')

