# selenium-expandtesting_UI

UI and API testing in [expandtesting](https://practice.expandtesting.com/notes/app/) note app. This project contains basic examples on how to use Selenium for UI tests writen in Python. Good practices such as hooks, custom commands and tags, among others, are used. All the necessary support documentation to develop this project is placed here. Although custom commands are used, the assertion code to each test is kept in it so we can work independently in each test. It creates one .json file for each test so we can share data between different commands in the test. The .json file is excluded after each test execution. 

# Pre-requirements:

| Requirement                     | Version        | Note                                                            |
| :------------------------------ |:---------------| :-------------------------------------------------------------- |
| Python                          | 3.12.5         | -                                                               |
| Visual Studio Code              | 1.89.1         | -                                                               |
| Python extension                | 2024.14.1      | -                                                               | 
| Selenium                        | 4.25.0         | -                                                               |
| Pytest                          | 8.3.3          | -                                                               |
| Copy CSS Selector               | 1.3.4          | -                                                               |
| Faker                           | 30.0.0         | -                                                               |
| selenium-wire                   | 5.1.0          | -                                                               |
| pytest-html                     | 4.1.1          | -                                                               |
          

# Installation:

- See [python page](https://www.python.org/downloads/) and download the latest Python stable version. Start the installation and check the checkboxes below: 
  - :white_check_mark: Use admin privileges when installing py.exe 
  - :white_check_mark: Add python.exe to PATH
and keep all the other preferenced options as they are.
- See [Visual Studio Code page](https://code.visualstudio.com/) and install the latest VSC stable version. Keep all the prefereced options as they are until you reach the possibility to check the checkboxes below: 
  - :white_check_mark: Add "Open with code" action to Windows Explorer file context menu. 
  - :white_check_mark: Add "Open with code" action to Windows Explorer directory context menu.
Check then both to add both options in context menu.
- Look for Python in the extensions marketplace and install the one from Microsoft.
- Open windows propmpt as admin and execute ```pip install selenium``` to install Selenium.
- Open windows propmpt as admin and execute ```pip install pytest``` to install Pytest.
- Open windows propmpt as admin and execute ```pip install Faker``` to install Faker library.
- See [Copy CSS Selector page](https://chromewebstore.google.com/detail/copy-css-selector/bmgbagkoginmbbgjapcacehjdojdnnhf?hl=pt-BR&utm_source=ext_sidebar) and install it. 
- Open windows propmpt as admin and execute ```pip install selenium-wire``` to install Faker library.
- Open windows propmpt as admin and execute ```pip install pytest-html``` to install pytest-html plugin.

# Tests:

- Execute ```pytest ./tests -v --html=./reports/report.html``` to run tests and generate a report inside reports folder.

# Support:

- [expandtesting API documentation page](https://practice.expandtesting.com/notes/api/api-docs/)
- [expandtesting API demonstration page](https://www.youtube.com/watch?v=bQYvS6EEBZc)
- [How to obtain a CSS Selector](https://help.probely.com/en/articles/8480719-how-to-obtain-a-css-selector)
- [Using faker with selenium and python](https://stackoverflow.com/a/27650137/10519428)
- [Faker 30.0.0 documentation](https://faker.readthedocs.io/en/stable/)
- [Working with windows and tabs](https://www.selenium.dev/documentation/webdriver/interactions/windows/)
- [Keeping browser open](https://www.selenium.dev/documentation/webdriver/browsers/chrome/#keeping-browser-open)
- [Selenium: WebDriverException:Chrome failed to start: crashed as google-chrome is no longer running so ChromeDriver is assuming that Chrome has crashed](https://stackoverflow.com/a/53073789/10519428)

# Tips:

- UI and API tests to send password reset link to user's email and API tests to verify a password reset token and reset a user's password must be tested manually as they rely on e-mail verification.  
