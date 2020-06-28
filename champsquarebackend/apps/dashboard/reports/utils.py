from champsquarebackend.core.loading import get_class, get_classes

UserReportGenerator = get_classes('analytics.reports', ['UserReportGenerator'])

class GeneratorRepository(object):

    generators = [UserReportGenerator]

    def get_report_generators(self):
        return self.generators

    def get_generator(self, code):
        for generator in self.generators:
            if generator.code == code:
                return generator
        return None
