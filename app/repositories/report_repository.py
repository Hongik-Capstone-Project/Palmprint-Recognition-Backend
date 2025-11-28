from app.models.report import Report

from .base import BaseRepository


class ReportRepository(BaseRepository[Report]):
    def __init__(self):
        super().__init__(Report)

    def get_by_user_query(self, user_id: int):
        return self.exact_query(Report.user_id, user_id)

    def get_by_auth_log_query(self, auth_log_id: int):
        return self.exact_query(Report.auth_log_id, auth_log_id)

    def get_by_status_query(self, status: str):
        return self.exact_query(Report.status, status)

    def search_by_type_query(self, keyword: str):
        return self.search_query(Report.report_type, keyword)

    def get_pending_query(self):
        return self.exact_query(Report.status, "pending")
