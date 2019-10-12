from datetime import datetime

from mantisconnect.project import Issue
from mantisconnect.project import Project


class SimpleProject(Project):
    """
    Simple Project
    """
    def __init__(self, mantis_soap_connector, name):
        Project.__init__(self, mantis_soap_connector, name)

    def _make_issue_data_extension(self, new_issue, issue):
        pass

    def request_filter_date_submiited_issues(self, filter_name, per_page=50):
        issue_list = list()

        for issue in self._request_filter_time_range(filter_name, per_page):
            today = datetime.datetime.now().date()
            date_submitted = issue["date_submitted"].date()
            if date_submitted == today:
                issue_list.append(self.make_issue_data(issue))

        return issue_list

    def request_filter_last_updated_issues(self, filter_name, per_page=50):
        issue_list = list()

        for issue in self._request_filter_time_range(filter_name, per_page):
            today = datetime.datetime.now().date()
            last_updated = issue["last_updated"].date()
            if last_updated == today:
                issue_list.append(self.make_issue_data(issue))

        return issue_list

    def request_filter_all_issues(self, filter_name, per_page=50):
        issue_list = list()
        for issue in self._request_filter(filter_name, per_page):
            issue_list.append(self.make_issue_data(issue))

        return issue_list

    def request_filter_time_range_issues(self, filter_name, per_page=50, start_date=None, end_date=None):
        issue_list = list()

        for issue in self._request_filter_time_range(filter_name, per_page, start_date, end_date):
            issue_list.append(self.make_issue_data(issue))

        return issue_list
