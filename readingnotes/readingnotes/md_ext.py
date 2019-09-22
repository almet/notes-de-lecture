from markdown.preprocessors import Preprocessor


class BlockquotesPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        for line in lines:
            if line.startswith('>'):
                new_lines.append('&nbsp;')
                new_lines.append(line)
            else:
                new_lines.append(line)
        return new_lines