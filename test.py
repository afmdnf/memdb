import os
from db import *

def run_test(test_input, test_output):
    test_input = test_input.strip()
    commands = test_input.split("\n")
    
    expected_results = test_output.strip().split("\n")
    actual_results = list()

    db = MemDB()

    for cmd in commands:
        if "UNSET" in cmd:
            _, k = cmd.split(" ")
            db.remove(k)
        elif "SET" in cmd:
            _, k, v = cmd.split(" ")
            db.set(k, v)
        elif "GET" in cmd:
            _, k = cmd.split(" ")
            r = db.get(k)
            if r:
                actual_results.append(r)
            else:
                actual_results.append("NULL")
        elif "BEGIN" in cmd:
            db.begin()
        elif "ROLLBACK" in cmd:
            r = db.rollback()
            if r is not None:
                actual_results.append(r)
        elif "COMMIT" in cmd:
            r = db.commit()
            if r is not None:
                actual_results.append(r)
        else:
            raise ValueError("Error: unrecognized command {}".format(cmd))

    actual_results = [str(x) for x in actual_results]

    if expected_results == actual_results:
        print("Test passed")
        return True
    else:
        print("Test failed")
        print("Expected: {}".format(expected_results))
        print("Actual: {}".format(actual_results))
        return False


if __name__ == "__main__":
    
    TEST_DIR = "tests/"
    test_inputs = sorted([x for x in os.listdir(TEST_DIR) if "input" in x])

    total_test_cnt = len(test_inputs)
    failed_test_cnt = 0

    print("------------")

    for i, t in enumerate(test_inputs):
        print("Running test {}: {}".format(i+1, t))

        input_file = open(TEST_DIR + t, "r").read()

        output_correct = t.replace("input", "output")
        output_file = open(TEST_DIR + output_correct, "r").read()
        
        if not run_test(input_file, output_file):
            failed_test_cnt += 1
        
        print("------------")

    success_test_cnt = total_test_cnt - failed_test_cnt
    print("Ran {} Tests: {} passed; {} failed".format(total_test_cnt, success_test_cnt, failed_test_cnt)) 
