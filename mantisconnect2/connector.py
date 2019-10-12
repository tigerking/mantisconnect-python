from zeep import Client


class MantisSoapConnector:
    """
    Mantis soap connector
     request filter, version, issue of filter, enum data using mantis soap api
    """
    def  __init__(self, mantis_soap_url = "https://www.mantisbt.org/bugs/api/soap/mantisconnect.php?wsdl"):
        self.mantis_soap_url = mantis_soap_url
        self.client = None
        self.version = None

    def set_user_passwd(self, name, passwd):
        self.user_name = name
        self.user_passwd = passwd

    def connect(self):
        self.client = Client(self.mantis_soap_url)
        self.version = self.request_version()

    def request_version(self):
        return self.client.service.mc_version()

    def request_issue_get(self, issue_id):
        pass

    def request_enum_status(self):
        pass

    def request_enum_priorities(self):
        pass

    def request_enum_resolutions(self):
        pass

    def request_project(self, project_name):
        pass

    def request_filter_get(self, project_id):
        pass

    def request_filter_get_issue(self, project_id, filter_id, page_number=0, per_page=0):
        pass

    def request_filter_get_issue_header(self, project_id, filter_id, page_number=0, per_page=0):
        pass

    def get_projects(self):
        pass

    def get_categories(self, project):
        pass

    def create_new_issue(self, summary, project, category=None, description=None):
       pass


