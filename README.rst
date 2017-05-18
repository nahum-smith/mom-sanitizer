# M.O.M. Sanitizer
## Development Version (1.0.0.dev1)

##### Note: Please clone this repository for most recent version. [Requires: Python 3.5+]

## Overview
For those with compliance requirements or who are concerned with minimizing exposure of personally identifiable information, we took it upon ourselves to build something that could (M)odularly assist with (O)bfuscating digital (M)edia. The efficiency of this command line tool is that you can move this application into your production environments and scan files in place, rather relocating any sensitive data. Then ideally remove this application from the environment and report your findings as this is not meant to be an ongoing solution for mitigating out of bounds PII.

### Description
**mom_sanitizer** was created to assist with identifying any PII (Personally Identifiable Information) stored at rest in clear text, particularly when it isn't expected such as in log files. This application can scan your unencrypted data and identify potential PII.

According to Nist Special Publication 800-122, examples of PII include, but are not limited to:
* Names, such as full name, maiden name, mother‘s maiden name, or alias
* Personal identification numbers, such as social security number (SSN), passport number, driver‘s license number, taxpayer identification number, or financial account or credit card number
* Address information, such as street address or email address

We are always trying to improve this utility, so please post your suggestions.

## Installation
**mom_sanitizer** requires Python 3.5 and the only supported platform is Linux32/64bits. Please note any difficulties encountered when using this application.

##### using pip package  
download compressed files from [M.O.M. Sanitizer on PyPi](include link here)  
Unpack and install with:
```bash
$ pip install mom_sanitizer
$ sanitize *args
```  
##### Cloning from Github Repository
1. Clone this Repository
2. Move into the project directory: `$ cd mom_sanitizer`
3. Install distribution with: `$ ./setup.py install`
4. From anywhere on your system run program with: `$ sanitize *args`  

## Usage

### Commands
The following command will provide the list of available command line options:

#### Arguments
###### source_directory:   
The directory that the search traverses down the file tree from [if recursive]    
The single directory the search is performed on [if non-recursive]

###### file_pattern:
Can be either: (1) an exact file or (2) a shell pattern that will match a set of files  
###### recursive [-r]:
If flagged will perform search traversing down the file tree from the source directory
###### search terms:
One or more search terms listed one after another
###### ignore case [-i]:
if flagged will set ignore_case to False.  Standard setting is case insensitive
###### mask (obfuscate) [-m]:
If flagged will replace all matched terms with a sequence of astericks.  
NOTHING OUTPUTTED TO SCREEN  
When flagged all files are searched and automatically obfuscated IN PLACE and saved.  
USE WITH CAUTION


#### Sample Command
```bash
$ sanitize /home/ubuntu/workspace/projects -r '*.txt' debug windows config
```

#### Sample Output
```bash
Path/File: /home/ubuntu/wokspace/projects/logfile1.txt  

          Line [3], Matched [debug] at position (4, 10)
          Line [7], Matched [DEBUG] at position (7, 15)
          Line [37], Matched [windows] at position (3, 9)

          Total Lines Searched: 98
          Total Matches: 3
          Total Matches By Term:

                debug: 2  
                config: 0
                windows: 1  

Path/File: /home/ubuntu/wokspace/projects/logfile2.txt  

          Line [5], Matched [debug] at position (4, 10)
          Line [77], Matched [DEBUG] at position (7, 15)
          Line [103], Matched [windows] at position (3, 9)
          Line [114], Matched [config] at position (5, 11)
          Line [120], Matched [config] at position (1, 6)
          Line [122], Matched [WINDOWS] at position (1, 7)
          Line [140], Matched [DEBUG] at position (3, 9)

          Total Lines Searched: 150
          Total Matches: 7
          Total Matches By Term:

                debug: 3  
                config: 2
                windows: 2  

Program Summary:  

          Total Program Matches: 10
          Total Lines Searched: 248
          Total Files Searched: 2
          Total Program Matches By Term:
                debug: 4
                config: 2
                windows: 3

```
#### Reporting options

As of now output is limited to standard (seen above).   
