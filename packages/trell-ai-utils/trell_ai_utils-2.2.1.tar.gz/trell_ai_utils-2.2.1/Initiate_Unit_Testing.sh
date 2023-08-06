echo
echo ---------------UNIT TESTING INITIATED-----------------
echo 

# Removing python cache files for Unit_Testing directory
`rm -r Unit_Testing/__pycache__ 2>/dev/null`

# Iterating throuth all unit test scripts and executing them
for script in `ls Unit_Testing/*.py`
do
    echo "******Testing $script********"
    echo `python -m unittest $script`
    echo
done
