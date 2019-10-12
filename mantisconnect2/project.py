from abc import ABCMeta
from datetime import datetime


class ExtensionFieldAbstract(ABCMeta):
    """ Abstract extension field for issue data """
    pass


class Issue:
    """
    Issue
     - contains issue data that id, project, category, priority ...
     - use extension_field for custom field or user field
    """
    def __init__(self):
        self.issue_id = -1
        self.project = None
        self.category = None
        self.priority = None
        self.severity = None
        self.reporter = None
        self.assigner = None
        self.summary = None
        self.status = None
        self.resolution = None
        self.version = None
        self.date_submitted = datetime.now()
        self.last_updated = datetime.now()
        self.extension_field = None

    # def set_extension_field(self, extension_field: ExtensionFieldAbstract):
    def set_extension_field(self, extension_field):
        self.extension_field = extension_field


class Filter:
    """
    Filter of project
     - contains issue data that id, project, category, priority ...
     - use extension_field for custom field or user field
    """
    def __init__(self, name, f_id):
        self.name = name
        self.f_id = f_id

    def __str__(self):
        return " - filter: %s(id:%d)" % (self.name, self.f_id)


class Project:
    """
    Mantis project
     - offers issue data by project filter
    """
    def __init__(self, mantis_soap_connector, project_name):
        self.mc = mantis_soap_connector
        self.name = project_name
        self.p_id = -1
        self.filter_list = list()

        if self.mc:
            self.p_id = self.mc.request_project(project_name)
            if self.p_id <= 0:
                msg = "Not found project id {0}(name:{1})".format(self.p_id, project_name)
                raise IndexError(msg)

            for f in self.mc.request_filter_get(self.p_id):
                self.filter_list.append(Filter(f.name, f.id))

    def __repr__(self):
        msg = "%s(id:%d) project\n" % (self.name, self.p_id)
        for f in self.filter_list:
            msg += str(f)
            msg += "\n"
        return msg

    def _make_issue_data_extension(self, new_issue, issue):
        raise NotImplementedError("Must implements.")

    def make_issue_data(self, issue):
        new_issue = Issue()
        new_issue.project = self.name
        new_issue.issue_id = issue["id"]
        new_issue.category = issue["category"]
        new_issue.priority = issue["priority"]["name"]
        new_issue.severity = issue["severity"]["name"]
        new_issue.reporter = issue["reporter"]["real_name"]
        if issue["handler"]:
            new_issue.assigner = issue["handler"]["real_name"]
        new_issue.summary = issue["summary"]
        new_issue.status = issue["status"]["name"]
        new_issue.resolution = issue["resolution"]["name"]
        new_issue.version = issue["version"]
        new_issue.date_submitted = issue["date_submitted"]
        new_issue.last_updated = issue["last_updated"]

        self._make_issue_data_extension(new_issue, issue)
        return new_issue

    def clear_filter_list(self):
        self.filter_list.clear()

    def set_filter_list(self, filter_list):
        self.clear_filter_list()
        self.filter_list = filter_list

    def find_filter_id(self, filter_name):
        for f in self.filter_list:
            if f.name == filter_name:
                return f.f_id

        raise KeyError("Not found filter name.")

    def _request_filter(self, filter_name, per_page=50):
        """
        _request_filter
         get issue list data

         filter_name: filter name
         per_page: count of issue per page
         return: yield type issue data
        """
        f_id = self.find_filter_id(filter_name)
        page_num = 1

        while True:
            try:
                filter_issue_list = self.mc.request_filter_get_issue(self.p_id, f_id, page_num, per_page)
            except Exception as e:
                print('ERR: Skip page %d' % page_num)
                print(str(e))
                page_num += 1
                continue

            page_num += 1
            if not filter_issue_list:
                break

            for issue in filter_issue_list:
                yield issue

    def _request_filter_time_range(self, filter_name, per_page=50,
                                    start_date=None, end_date=None):
        """
        _request_filter_time_range
         get issue list data

         filter_name: filter name
         per_page: count of issue per page
         start_date: datetime for compare to last_updated issue
         end_date: datetime for compare to last_updated issue
         return: yield type issue data
        """
        page_num = 1
        f_id = self.find_filter_id(filter_name)
        stop_process = False

        if not start_date:
            start_date = datetime.now().date()

        if not end_date:
            end_date = datetime.now().date()

        while True:
            try:
                filter_issue_list = self.mc.request_filter_get_issue(self.p_id, f_id, page_num, per_page)
            except Exception as e:
                print('ERR: Skip page %d' % page_num)
                print(str(e))
                page_num += 1
                continue

            page_num += 1

            # no more data
            if not filter_issue_list:
                break

            for issue in filter_issue_list:
                last_updated = issue["last_updated"]
                #date_submitted = issue["date_submitted"]

                if last_updated.date() < start_date:
                    stop_process = True
                    break

                if last_updated.date() > end_date:
                    continue

                yield issue

            if stop_process:
                break
