from apps.company.models import Company


class AllCompanyListUseCase:

    def execute(self):
        return self._factory()

    def _factory(self):
        self._companies = Company.objects.all().order_by('-created_at')
        return self._companies
