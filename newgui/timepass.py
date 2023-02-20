import re
mobile = input("Enter mobile number")
mobile_pattern = re.compile(r'(\d{10})')
name_pattern = re.compile(r'\d{1,2}')
match = mobile_pattern.search(mobile)
if match and len(mobile) == 10:
    print(match.group(0))
else:
    print("error")
    