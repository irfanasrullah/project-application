name: C/I testing with coverage

on: [push, pull_request]

jobs:
  build
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v1
      with:
        python-version: 3.7.3

    - name: Install dependencies
      run: |
        python3 -m pip install --upgrade pip
        pip3 install -r requirements.txt
    - name: Test with pytest
      run: |
        cd ProjectApplication
        coverage erase
        coverage run manage.py test
        coverage xml
    - name: UPload coverage to Codecov
      uses: codecov/codecov-action@v1
      with:
        token: ${{ secrets.CODECOV_TOKEN }}
        flags: unittests
        name: codecov-project
        fail_ci_if_error: false
