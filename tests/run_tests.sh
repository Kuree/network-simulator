TEST_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#/bin/bash -c "$TEST_DIR/../env/bin/active exec /bin/bash -i"
source $TEST_DIR/../env/bin/activate
for f in $(find $TEST_DIR -name 'test*.py'); 
    do 
        echo "Running test $f";
        python $f;
done

#exit
