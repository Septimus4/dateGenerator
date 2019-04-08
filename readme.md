# DateGenerator
Date generator supporting a few output with customizable separator.  
Just a simple code that allow to generate wordlist based on dates.  
Could be used directly in any other python script.  
### Support  
* yyyymmdd
* mmddyyyy
* ddmmyyyy
## Installation 
### Requirements
* python
## Usage
You can simply run it as a script with arguments:
* 1: starting year
* 2: ending year
* 3: display format
    * 0 = yyyymmdd
    * 1 = ddmmyyyy
    * 2 = mmddyyyy
* 3 : optional separator added in between

```bash
python3  date_generator.py {starting year} {ending year} {display format} {separator}
```
You could also remove the main function and use it in your python code as a class.  
The separator in not required, if not passed the script doesn't display any.  
## Example
`$ python3 date_generator.py 1900 1901 1`
01011900  
02011900  
03011900  
04011900  
05011900  
06011900  
...  
26121900  
27121900  
28121900  
29121900  
30121900  
31121900  

`$ python3 date_generator.py 1900 1901 0 "-"`
1900-01-01  
1900-01-02  
1900-01-03  
1900-01-04  
1900-01-05  
1900-01-06  
...  
1900-12-26  
1900-12-27  
1900-12-28  
1900-12-29  
1900-12-30  
1900-12-31  

## License
[GPL-3.0]
