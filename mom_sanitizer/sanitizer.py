#!/usr/bin/env python3
#----------------------------------------

import os, sys, fnmatch, fileinput, re, argparse

parser = argparse.ArgumentParser(description='''Welcome to Mom_Sanitizer. A
regex solution to simplify searching for specific strings and offer the ability
to have those masked (intended for log files to maintain Policy compliance).''')
parser.add_argument("source_path", help='''directory(s) where search begins with
the format "/path/to/your/mom"''')
parser.add_argument("-r", "--recursive", help='''Default is True, when flagged for
False the search will only return files from the present directory''',
default=False, action='store_true')
parser.add_argument("file_pattern", help='''Please offer a shell expression pattern
to identify the files to address: Pattern Meaning / * matches everything / ? matches
any single character /[seq] matches any character in seq / [!seq] matches any
character not in seq (ex. '[!.]*.py')''')
parser.add_argument("search_terms", nargs='*', help='''Must be >= 1 until we fix
that, traverses through file(s) and prints search_term (or its regex matches)
and its found location''')
parser.add_argument("-mask", "--obfuscation", help='''Default is False. When True,
will obfuscate all found search terms with "***"''', default=False, action='store_true')
parser.add_argument("-i", "--ignore_case", help='''Default is True.  When False,
will follow specified character cases''', default=True, action='store_false')
parser.add_argument("-b", "--brief", help='''Default is False.  When True, will
output only File Header and Line Data (omitting aggregated results following
files)''', default=False, action='store_true')

args = parser.parse_args()

class Program_Data(object):
#-------------------------------------------------------------------------------
#---Initialization Method for Primary Data Object Class-------------------------
#-------------------------------------------------------------------------------
    def __init__(self, args):

        self.source_path = args.source_path
        self.file_pattern = args.file_pattern
        self.search_terms_list = args.search_terms
        self.recursive = args.recursive
        self.obfuscation = args.obfuscation
        self.ignore_case = args.ignore_case

#-------------------------------------------------------------------------------
#---Child Aggregate Object Class for Primary Data Object Class------------------
#-------------------------------------------------------------------------------

    class Aggregate_Data_Object(object):

        def __init__(self, search_terms, _main=False, _dir=False, _file=False, _line=False):

            class New_Dict(dict):
                def __init__(self, search_terms, aggregated=False, by_term=False):
                    if aggregated:
                        pass
                    if by_term:
                        for term in search_terms:
                            self[term] = 0

            self.aggregated = New_Dict(search_terms, aggregated=True)

            if _main:
                self.aggregated['total_dirs_searched'] = 0
                self.aggregated['total_matches'] = 0
                self.aggregated['dirs_searched'] = []
                self.aggregated['total_files_searched'] = 0
                self.aggregated['files_searched'] = []
                self.aggregated['total_lines_searched'] = 0
                self.aggregated['by_dir'] = New_Dict(search_terms, aggregated=True)
            if _dir:
                self.aggregated['total_files_searched'] = 0
                self.aggregated['total_matches'] = 0
                self.aggregated['files_searched'] = []
                self.aggregated['total_lines_searched'] = 0
                self.aggregated['by_file'] = New_Dict(search_terms, aggregated=True)
            if _file:
                self.aggregated['total_matches'] = 0
                self.aggregated['total_lines_searched'] = 0
                self.aggregated['by_line'] = New_Dict(search_terms, aggregated=True)

            self.aggregated.total_matches = 0
            self.aggregated['by_term'] = New_Dict(search_terms, by_term=True)

#-------------------------------------------------------------------------------
#-------Methods on Aggregate Data Object Class----------------------------------
#-------------------------------------------------------------------------------

        def increase_match_count(self, term, count=1):
            self.aggregated['by_term'][term] += count
            self.aggregated.total_matches += count

        def update_aggregate_count(self, key, count=1):
            self.aggregated[key] += count
        def update_aggregate_count_base(self, base, key, count=1):
            base.aggregated[key] += count

        def update_aggregate_list(self, key, item):
            self.aggregated[key].append(item)

        def aggregate_list_check(self, attr, item):
            if self.__contains__(attr):
                return item in self.aggregate[attr]

#-------------------------------------------------------------------------------
#---Methods on Primary Data Object Class----------------------------------------
#-------------------------------------------------------------------------------

    def recursive_switch(self):
        '''INCLUDE DOCSTRING HERE'''
        def scantree_recursive(source_path, file_pattern):
            for entry in os.scandir(source_path):
                if not entry.path.startswith('.') and entry.is_dir(follow_symlinks=False):
                    if self.obfuscation:
                        self.total_results.update_aggregate_list('dirs_searched', entry)
                    for entry in scantree_recursive(entry.path, file_pattern):
                        if self.obfuscation:
                            self.total_results.update_aggregate_list('dirs_searched', entry)
                        yield(entry)
                else:
                    if fnmatch.fnmatch(entry.name, file_pattern):
                        yield(entry.path)

        def scantree_non_recursive(source_path, file_pattern):
            for entry in os.scandir(source_path):
                if entry.is_dir(follow_symlinks=False):
                    if self.obfuscation:
                        self.total_results.update_aggregate_count('total_dirs_searched')
                        self.total_results.update_aggregate_list('dirs_searched', entry)
                    pass
                else:
                    if fnmatch.fnmatch(entry.name, file_pattern):
                        yield(entry.path)

        if not self.recursive:
            valid_files = list(scantree_non_recursive(self.source_path, self.file_pattern))
            self.__setattr__('valid_files', valid_files)
        else:
            valid_files = list(scantree_recursive(self.source_path, self.file_pattern))
            self.__setattr__('valid_files', valid_files)

    def regex_formulation(self):

        pattern_string = r''

        for i, term in enumerate(self.search_terms_list):
            if i == 0:
                pattern_string += '(?P<search_term_{}>{})'.format(i+1,term)
            else:
                pattern_string += '|(?P<search_term_{}>{})'.format(i+1,term)
        pattern_string += '+'
        if self.ignore_case:
            match_term = re.compile(pattern_string, re.I)
        else:
            match_term = re.compile(pattern_string)

        self.__setattr__('match_term', match_term)

    def ignore_case_update_terms(self):
        if self.ignore_case:
            for i, term in enumerate(self.search_terms_list):
                self.search_terms_list[i] = term.lower()

    def create_aggregate_object(self, _file=False, _dir=False, file_name=None, dir_name=None, line_num=None):

        if not _dir and not _file:
            self.total_results = self.Aggregate_Data_Object(self.search_terms_list, _main=True)
        if _dir:
            self.total_results.aggregated['by_dir'][dir_name] = self.Aggregate_Data_Object(search_terms=self.search_terms_list, _dir=_dir)
        if _file:
            self.total_results.aggregated['by_dir'][dir_name].aggregated['by_file'][file_name] = self.Aggregate_Data_Object(self.search_terms_list, _file=_file)

    def regex_sub_func(self, match_object):
        len_match = len(match_object.group(0))
        return '*' * len_match

    def obfuscation_function(self):

        user_response = input('''WARNING!!! This will edit all files searched ,specified!
        Is this OK: Y(yes)(enter) or N(no)? ''')

        valid_true_choices = ['y', 'Y', 'YES', 'yes', '\n']
        valid_false_choices = ['n', 'N', 'NO', 'no']

        if user_response in valid_true_choices:
            valid_files = self.__getattribute__('valid_files')
            with fileinput.input(files=valid_files, inplace=True) as fobj:
                for line in fobj:
                    print(self.match_term.sub(self.regex_sub_func, line))
        else:
            print('use: mom_sanitizer --help for information regarding option flags')


    def regex_func_switch(self, obfuscation, compile_object, line):

        def sub_func(match_object):
            len_match = len(match_object.group(0))
            return '*' * len_match

        if obfuscation:
            compile_object.sub(sub_func, line)

    def increase_aggregated_match_results(self, match_term, dir_name=None, file_name=None, line_num=None):

        self.total_results.aggregated['total_matches'] += 1

        self.total_results.aggregated['by_term'][match_term] += 1

        if dir_name != None:
            #print('by dir: {} total matches increase by 1'.format(dir_name))
            self.total_results.aggregated['by_dir'][dir_name].aggregated.total_matches +=1
            #print('by dir: {} and by term: {} increase by 1'.format(dir_name, match_term))
            self.total_results.aggregated['by_dir'][dir_name].aggregated['by_term'][match_term] +=1
            if file_name != None:
                #print('by dir: {}, and by file: {} increase total matches by 1'.format(dir_name, file_name, match_term))
                self.total_results.aggregated['by_dir'][dir_name].aggregated['by_file'][file_name].aggregated.total_matches +=1
                #print('by dir: {}, by file: {} and by term: {} increase by 1'.format(dir_name, file_name, match_term))
                self.total_results.aggregated['by_dir'][dir_name].aggregated['by_file'][file_name].aggregated['by_term'][match_term] +=1
                if line_num != None:
                    self.total_results.aggregated['by_dir'][dir_name].aggregated['by_file'][file_name].aggregated['by_line'][line_num].aggregated.total_matches +=1
                    self.total_results.aggregated['by_dir'][dir_name].aggregated['by_file'][file_name].aggregated['by_line'][line_num].aggregated['by_term'][match_term] +=1



    def output_func(self, print_header=False, print_footer=False, print_line=False, filename=None, dirname=None, matchobject=None):

        if print_header:
            self.print_header()
            print_header = False
        if print_line:
            self.print_line()
            print_line = False
        if print_footer:
            self.print_footer()
            print_footer = False

    def print_header(self, filename, fileobj_term_dict):

        print('\nPath/File: {}\n'.format(filename))

    def print_line(self, line, matchterm, start, end):
        print('\tLine [{}], Matched [{}] at position ({}, {})\n'.format(line, matchterm, start, end))

    def print_footer(self, file_object):
        term_keys = file_object['by_term'].keys()
        total_lines_searched = file_object['total_lines_searched']
        total_matches = file_object.total_matches
        print('\tTotal Lines Searched: {}\n\tTotal Matches: {}\n\tTotal Matches By Term:'.format(total_lines_searched, total_matches))
        for k,v in file_object['by_term'].items():
            print('\t\t\t\t', k, ':', v)
        print('\n')

    def print_program_summary(self, aggregated_obj):
        total_matches = aggregated_obj['total_matches']
        total_lines_searched = aggregated_obj['total_lines_searched']
        total_files_searched = aggregated_obj['total_files_searched']
        term_keys = aggregated_obj['by_term'].keys()

        print('\nProgram Summary:\n')
        print('\tTotal Program Matches: {}'.format(total_matches))
        print('\tTotal Lines Searched: {}'.format(total_lines_searched))
        print('\tTotal Files Searched: {}'.format(total_files_searched))
        print('\tTotal Program Matches By Term:\n')
        for k,v in aggregated_obj['by_term'].items():
            print('\t\t\t\t\t', k, ':', v)

    def aggregated_output(self):

            print('-'*70)
            print('-'*70)
            print('-'*70)
            print('------------RESULTS BELOW-----------------------------')
            print(self)
            print('-'*70)
            print(self.total_results)
            print('-'*70)
            print(self.total_results.aggregated)
            print('-'*70)
            print('------------BY_TERM DICT--------------')
            print(self.total_results.aggregated['by_term'])
            print('-'*70)
            print('total files searched (PROGRAM):', self.total_results.aggregated['total_files_searched'])
            print('-'*70)
            print('total directories searched (PROGRAM):', self.total_results.aggregated['total_dirs_searched'])
            print('-'*70)
            print('total matches (PROGRAM):', self.total_results.aggregated['total_matches'])
            print('-'*70)
            print('total lines searched (PROGRAM):', self.total_results.aggregated['total_lines_searched'])
            print('-'*70)

            for k, v in self.total_results.aggregated['by_dir'].items():
                print('------------BY_DIR DICT-----------')
                print('DIRECTORY',k,'\nVALUE:', v)
                print('-'*70)
                print(v.aggregated)
                print('-'*70)
                for i,j in v.aggregated['by_file'].items():
                    print('-----------BY_FILE DICT-------------------')
                    print('FILE:',i,'\nVALUE:',j)
                    print('-'*70)
                    print(j.aggregated)
                    print('-'*70)
            print('-'*70)

    def regex_fileinput_loop(self):
        with fileinput.input(files=self.valid_files) as fobj:
            fname = 'fname'
            fname_full = 'fname_full'
            dirname = 'dirname'
            print_footer = False
            print_header = False
            print_line = False
            previous_file_obj = {}

            for line_index, line in enumerate(fobj, start=1):
                if fobj.isfirstline():
                    pos_matches_list = []
                    neg_matches_list = []
                    new_file = True
                    print_header = True

                if new_file and print_footer:
                    self.print_footer(previous_file_obj)
                    print_footer = False

                fname_full = fobj.filename()
                fname = os.path.basename(fname_full)
                dirname = os.path.dirname(fname_full) + '/'

                if new_file:
                    if not dirname in self.total_results.aggregated['dirs_searched']:
                        self.total_results.aggregated['dirs_searched'].append(dirname)
                        self.total_results.aggregated['total_dirs_searched'] += 1
                        self.create_aggregate_object(_dir=True, _file=True, file_name=fname, dir_name=dirname)

                    self.create_aggregate_object(_file=True, file_name=fname, dir_name=dirname)
                    self.total_results.aggregated['files_searched'].append(fname_full)
                    self.total_results.aggregated['total_files_searched'] += 1
                    self.total_results.aggregated['by_dir'][dirname].aggregated['files_searched'].append(fname)
                    self.total_results.aggregated['by_dir'][dirname].aggregated['total_files_searched'] += 1

                self.total_results.aggregated['total_lines_searched'] += 1
                self.total_results.aggregated['by_dir'][dirname].aggregated['total_lines_searched'] += 1
                self.total_results.aggregated['by_dir'][dirname].aggregated['by_file'][fname].aggregated['total_lines_searched'] += 1

                matches = self.match_term.finditer(line)
                for match_index, match in enumerate(matches, start=1):
                    if match_index == 1:
                        self.total_results.aggregated['by_dir'][dirname].aggregated['by_file'][fname].aggregated['by_line'][fobj.filelineno()] = [(match_index, match)]
                    else:
                        self.total_results.aggregated['by_dir'][dirname].aggregated['by_file'][fname].aggregated['by_line'][fobj.filelineno()].append((match_index, match))
                    if self.ignore_case:
                        match_term = match.group(0).lower()
                    else:
                        match_term = match.group(0)
                    self.increase_aggregated_match_results(match_term, dir_name=dirname, file_name=fname)


                    if print_header:
                        fobj_file_dict = self.total_results.aggregated['by_dir'][dirname].aggregated['by_file'][fname].aggregated['by_term']
                        self.print_header(fname_full, fobj_file_dict)
                        print_header = False

                    self.print_line(fobj.filelineno(), match.group(0), match.start(), match.end())
                    print_footer = True
                    previous_file_obj = self.total_results.aggregated['by_dir'][dirname].aggregated['by_file'][fname].aggregated

                new_file = False

            if self.total_results.aggregated.total_matches > 0:
                self.print_footer(previous_file_obj)
                self.print_program_summary(self.total_results.aggregated)
            else:
                self.print_program_summary(self.total_results.aggregated)


#-------------------------------------------------------------------------------

def run_program():
    data_object = Program_Data(args)

    data_object.ignore_case_update_terms()

    data_object.recursive_switch()

    data_object.regex_formulation()

    if data_object.obfuscation:
        data_object.obfuscation_function()
    else:
        data_object.create_aggregate_object()
        data_object.regex_fileinput_loop()
