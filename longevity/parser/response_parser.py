from longevity.parser import InitState


class ResponseParser:
    """ Parses the HTML returned by the SSA web site """

    @staticmethod
    def parse(html: str):
        state = InitState()
        with open(html) as fp:
            for line in fp:
                line = line.strip()
                state = state.handleLine(line)
        pass
