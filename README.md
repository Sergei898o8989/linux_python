# linux_python

# Log Analyzer

This script analyzes log files with the given format:

109.169.248.247 - - [12/Dec/2015:18:25:11 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-" "Mozilla/5.0 (Windows NT
6.0; rv:34.0) Gecko/20100101 Firefox/34.0" 7269

The script collects the following statistics:

- Top 3 IP addresses from which requests were made
- Top 3 longest requests (by duration)
- Request count for each HTTP method
- Total number of requests

The script can analyze a single log file or all log files in a directory. The results are saved to a JSON file and
printed to the terminal.

## Requirements

- Python 3

## Usage

1. Save the script to a file, e.g., `log_analyzer.py`.
2. Open a terminal or command prompt and navigate to the directory where the script is saved.
3. Run the script using the following command:

`python log_analyzer.py input_path`
Replace input_path with the path to the log file or directory containing log files. The script will process all
.log files in the directory if a directory is provided.

The script will save the results to a JSON file with the same name as the input file, but with a _result.json extension.
The results will also be printed to the terminal.

## Example

`python log_analyzer.py /path/to/your/logfile.log`
This will analyze the logfile.log, print the results to the terminal,
and save them to a file named logfile_result.json in the same directory.

