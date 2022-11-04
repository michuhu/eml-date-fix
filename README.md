# eml-date-fix
Convert dates in `.eml` files to a given format.

This script takes all `.eml` files from `eml_folder` (input), changes the dates to one standard format: 

`%d/%m/%Y %H:%M:%S %z`, e.g. `11/12/1994 01:32:14 +0100`

(or any given format you change it to in the code) 

and places them in `/fixed` folder. 

It was originally written to fix and standardize messages from polish science-fiction and fantasy usenet groups. You can read more about it here [pl.sf-f](https://github.com/michuhu/pl.sf-f/blob/main/README.md)

## TO DO
* parametrize date format