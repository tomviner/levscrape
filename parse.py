import re
import urllib
import logging
from datetime import datetime, date

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__file__)


# constants
TIME_FORMAT = '%I.%M %p'
NARRATOR = 'NARRATOR'


# TODO witness names need to be parsed from comments like:
# MS JOANNE KATHLEEN ROWLING (sworn)
witness = 'JK ROWLING'

# collect these from page metadata
date = date.today()
jk_url = "http://www.levesoninquiry.org.uk/wp-content/uploads/2011/11/Transcript-of-Afternoon-Hearing-24-November-2011.txt"



def strip_line_number(line):
    return re.sub('^ {12,14}\d{1,3}', '', line)

def generate_lines(url):
    for line in urllib.urlopen(url):
        yield line

def generate_speech(url):
    # init
    interviewer = None
    speaker = None
    remarks = []
    section_start_time = None

    lines = generate_lines(url)
    for i, numbered_line in enumerate(lines):
        previous_speaker = speaker
        raw_line = strip_line_number(numbered_line)
        line = raw_line.strip()
        if not line:
            continue
        logger.debug('%s', numbered_line)
        # skip page numbers
        if re.match('\d{1,4}', line):
            continue

        # NAMES: are in caps
        name = re.findall('([A-Z ]+): (.*)', line)
        if name:
            name, line = name[0]
            speaker = name
            if not interviewer:
                interviewer = speaker

        # Q. A.
        qa =  re.findall('(Q|A)\. (.*)', line)
        if qa:
            qa, line = qa[0]
            if qa=='Q':
                speaker = interviewer
            elif qa=='A':
                speaker = witness
            else:
                raise ValueError

        # 12 or spaces makes a comment
        note_re = '^ {12,}[a-zA-Z]'
        if re.search(note_re, raw_line):
            speaker = NARRATOR
        else:
            # (Comments or time)
            if line[0]=='(' and line[-1]==')':
                comment = line[1:-1]
                try:
                    tm = datetime.strptime(comment, TIME_FORMAT).time()
                except ValueError:
                    speaker = NARRATOR
                    line = comment
                else:
                    section_start_time = tm
                    line = None

        data_so_far = {
            'speaker': previous_speaker,
            'said': ' '.join(remarks),
            'section_start_time': section_start_time,
            }
        # when a speaker changes, yield the collected remarks
        # of the previous speaker
        if speaker != previous_speaker:
            yield data_so_far
            # reset the collection
            remarks = []

        if line:
            remarks.append(line)

    # yield the final remark
    yield data_so_far

if __name__ == '__main__':
    for ev in generate_speech(jk_url):
        dt = datetime.combine(date, ev['section_start_time'])
        print dt.strftime(TIME_FORMAT).lower(),
        print ev['speaker']
        print '\t', ev['said']
