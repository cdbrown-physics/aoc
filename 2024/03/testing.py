import re

pattern = r"mul\((\d+),(\d+)\)"
test_string = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

matches = re.findall(pattern, test_string)
print(matches)
