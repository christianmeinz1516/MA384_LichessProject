import re

class PGNParser:
    HEADER_REGEX = re.compile(r'\[(?P<tag_name>[A-Za-z0-9]+)\s"(?P<tag_value>[^"]+)"\]')
    
    def __init__(self, pgn_file):
        self.pgn_file = pgn_file
        self.game_num = 0
    
    def parse_headers(self, lines):
        matches = [self.HEADER_REGEX.match(line) for line in lines]
        matches = {m.group('tag_name'): m.group('tag_value') for m in matches if m}
        return matches
    
    def find_event(self, headers_lines):
        for line in headers_lines:
            if line.startswith('[Event') and line.find('Classical'):
                return {'Event': 'Classical'}
        return {}

    def parse_pgn(self):
        lines = []
        headers = []
        moves = []
        emptylines = 0
        # read until we find an empty line
        while emptylines < 2:
            line = self.pgn_file.readline()#.decode('utf-8')
            lines.append(line)
            if line == '\n':
                emptylines += 1
                continue
            elif line == '':
                self.pgn_file.close()
                break
            if line.startswith('['):
                headers.append(line)
            else:
                moves.append(line)

        #headers = self.parse_headers(headers)
        headers = self.parse_headers(headers)
        moves = ''.join(moves).strip()

        data = ''.join(lines)
        # if headers are not found, return None
        if not headers:
            return None, None, data

        return headers, moves, data
    
    def has_next(self):
        return not self.pgn_file.closed
    
    def next(self):
        headers, moves, data = self.parse_pgn()
        self.game_num += 1
        return headers, moves, data
