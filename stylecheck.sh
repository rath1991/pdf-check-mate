#!/bin/bash
while getopts "f:" opt; do
  case $opt in
    f)
      file_path=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

# Check if the file path is provided

if [ -z "$file_path" ]; then
  echo "Please provide a file path using the -f option."
  exit 1
fi

# Command 1
if pycodestyle "$file_path"; then
 echo "PYCODESTYLE PASS"
else
 echo "PYCODESTYLE FAIL" 
fi
# Command 2
if pydocstyle "$file_path"; then
 echo "PYDOCSTYLE PASS"
else
 echo "PYDOCSTYLE FAIL" 
fi

# Command 3
if darglint "$file_path"; then
 echo "DARGLINT PASS"
else
 echo "DARGLINT FAIL" 
fi

#command 4
if black --line-length 79  "$file_path"; then
 echo "BLACK PASS"
else
 echo "BLACK FAIL" 
fi

#command 5
if pylint "$file_path"; then
 echo "PYLINT PASS"
else
 echo "PYLINT FAIL" 
fi

#command 6
if isort "$file_path"; then
 echo "ISORT PASS"
else
 echo "ISORT FAIL" 
fi

