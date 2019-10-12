# -*- coding: utf-8 -*-

import mantisconnect2.connector


class MantisSoapConnectorV2(mantisconnect2.connector.MantisSoapConnector):
    """
    Mantis soap connector v2
    """

    def __init__(self, mantis_soap_url="https://www.mantisbt.org/bugs/api/soap/mantisconnect.php?wsdl"):
        self.mantis_soap_url = mantis_soap_url
        self.client = None
        self.version = None

    def request_issue_get(self, issue_id):
        return self.client.service.mc_issue_get(self.user_name, self.user_passwd, issue_id)

    def request_enum_status(self):
        return self.client.service.mc_enum_status(self.user_name, self.user_passwd)

    def request_enum_priorities(self):
        return self.client.service.mc_enum_priorities(self.user_name, self.user_passwd)

    def request_enum_resolutions(self):
        return self.client.service.mc_enum_resolutions(self.user_name, self.user_passwd)

    def request_project(self, project_name):
        return self.client.service.mc_project_get_id_from_name(self.user_name, self.user_passwd, project_name)

    def request_filter_get(self, project_id):
        return self.client.service.mc_filter_get(self.user_name, self.user_passwd, project_id)

    def request_filter_get_issue(self, project_id, filter_id, page_number=0, per_page=0):
        return self.client.service.mc_filter_get_issues(self.user_name, self.user_passwd,
                                                        project_id, filter_id, page_number, per_page)

    def request_filter_get_issue_header(self, project_id, filter_id, page_number=0, per_page=0):
        return self.client.service.mc_filter_get_issue_headers(self.user_name, self.user_passwd,
                                                               project_id, filter_id, page_number, per_page)

    def get_projects(self):
        # print('* get_projects ...')
        return self.client.service.mc_projects_get_user_accessible(self.user_name, self.user_passwd)

    def get_categories(self, project):
        project_id = self._get_project_id(project)
        if project_id > 0:
            return self.client.service.mc_project_get_categories(self.user_name, self.user_passwd, project_id)
        else:
            return []

    def create_new_issue(self, summary, project, category=None, description=None):
        print('* create_new_issue ...')
        issueData = self._create_object('IssueData')
        project_id = self._get_project_id(project)
        issueData['project'] = {'id': project_id}  # ATS project
        if category is None:
            category_list = self.get_categories(project_id)
            if len(category_list) > 0:
                category = category_list[0]

        issueData['summary'] = summary
        issueData['description'] = description
        issueData['category'] = category

        print('> new issue data: {}'.format(issueData))
        return self.client.service.mc_issue_add(self.user_name, self.user_passwd, issueData)

    def _get_project_id(self, project):
        if isinstance(project, int):
            return project
        prj = self.find_project(project_name=project)
        if prj:
            return prj.id
        else:
            return -1

    def find_project(self, project_name):
        for prj in self.client.service.mc_projects_get_user_accessible(self.user_name, self.user_passwd):
            if prj.name == project_name:
                return prj

        return None

    def _create_object(self, name):
        return self.client.get_type('ns0:' + name)()
