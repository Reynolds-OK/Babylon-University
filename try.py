from pathlib import Path

if Path('temlates/login.html').is_file():
    print('yes')

else:
    print('no')