from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.Qt import Qt
from validators import url as is_valid_url
from data.supported_apis import SUPPORTED_APIS
from webbrowser import open_new_tab


'''Written by JWesleyLima on 08/31/2021
Access my GitHub profile: https://github.com/jwesleylima'''

# global objects
line_edit_url = None
combo_box_api = None
label_api_details = None
button_shorten_url = None


def pre_enter():
	'''Executes some presets from the main window.'''
	global combo_box_api, label_api_details, line_edit_url, button_shorten_url

	# get widgets
	combo_box_api = main_window.comboBoxAPI
	label_api_details = main_window.information
	line_edit_url = main_window.lineEditCompleteURL
	button_shorten_url = main_window.buttonShortenURL

	# LineEditCompleteURL
	line_edit_url.setFocus(True)
	line_edit_url.textChanged.connect(check_typed_url)

	# buttonShortenURL
	button_shorten_url.setEnabled(False)
	button_shorten_url.clicked.connect(shorten_url)
	
	# ComboBoxAPI
	combo_box_api.addItems(SUPPORTED_APIS.keys())
	combo_box_api.currentIndexChanged.connect(update_api)

	# Menu actions
	main_window.actionAbout.triggered.connect(about_program)
	main_window.actionQuit.triggered.connect(app.quit)
	main_window.actionExpand.triggered.connect(run_url_expander)
	main_window.actionCredits.triggered.connect(show_credits)

	# Some pre-calls
	update_api()


def successful_dialog_pre_enter():
	'''Executes some presets from the sucess dialog.'''
	successful_dialog.commandOpenInBrowser.clicked.connect(successful_dialog_open_in_browser)
	successful_dialog.buttonCopyURL.clicked.connect(successful_dialog_copy_url)


def successful_dialog_open_in_browser():
	'''Opens the API response URL in a new tab in the default browser.'''
	shortened_url = successful_dialog.shortenedURL.text()
	open_new_tab(shortened_url)
	successful_dialog.close()


def successful_dialog_copy_url():
	'''Copies the API response URL to the clipboard.'''
	shortened_url = successful_dialog.shortenedURL.text()
	app.clipboard().setText(shortened_url)
	successful_dialog.close()


def show_sucessful_dialog(title: str, msg: str, url: str):
	'''Sets up and displays a success dialog

	Parameters
	----------
	title: (str) Title of the window that will be displayed
	msg: (str) Message that will be displayed
	url: (str) API response URL

	Returns
	-------
	None'''
	successful_dialog.setWindowTitle(title)
	successful_dialog.info.setText(msg)
	successful_dialog.shortenedURL.setText(url)
	successful_dialog.exec_()


def failure_dialog_pre_enter():
	'''Executes some presets from the failure dialog.'''
	failure_dialog.buttonOk.clicked.connect(failure_dialog.close)


def show_failure_dialog(msg: str, title='Something seems to have gone wrong'):
	'''Sets up and displays a failure dialog.

	Parameters
	----------
	msg: (str) Message that will be displayed
	title: (str) Title of the error that will be displayed
		It has a generic message by default

	Returns
	-------
	None'''
	failure_dialog.labelTitle.setText(title)
	failure_dialog.labelMessage.setText(msg)
	failure_dialog.exec_()


def update_api():
	'''Gets the data from the newly selected API and updates the UI.'''
	selected_api = combo_box_api.currentText()
	selected_api_data = SUPPORTED_APIS[selected_api]
	# get some cosmetic information
	api_limits_msg_color = 'red' if selected_api_data['limited-api'] else '#111'
	result_example_color = '#686868'

	# Update the warning message about API limits
	label_api_details.setText(f'<font color="{api_limits_msg_color}">\
		{selected_api_data["api-limits-msg"]}</font> \
		<font color="#333">| Final result example: </font> <font color="{result_example_color}">\
		     {selected_api_data["result-example"]}</font>')


def shorten_url():
	'''Shortens the URL entered by the user.

	According to the result, it shows a success or failure dialog.'''
	selected_api = combo_box_api.currentText()
	shorten = SUPPORTED_APIS[selected_api]['command']
	complete_url = line_edit_url.text().strip()
	shortened_url = ''

	try:
		shortened_url = shorten(complete_url)
	except:
		show_failure_dialog('Could not shorten URL. Try checking the spelling and validity of the URL. Also check if the URL you entered meets the API limitations below the API choice field.')
	else:
		show_sucessful_dialog('Successfully Shortened', 'Your shortened URL is',
			shortened_url)


def run_url_expander():
	'''Runs the URL expander window.'''
	exec(open('url_expander.py').read(), {'app': app, 
		'show_sucessful_dialog': show_sucessful_dialog, 'show_failure_dialog': show_failure_dialog})


def check_typed_url():
	'''It does some checks against the URL entered by the user.'''
	button_shorten_url.setEnabled(bool(is_valid_url(line_edit_url.text())))


def show_credits():
	'''It shows a dialog with the program credits.'''
	QMessageBox.information(main_window, 'Credits',
		'''DEVELOPER
https://github.com/jwesleylima

IMAGES FROM
https://www.freepik.com
https://www.flaticon.com/authors/prosymbols
https://icons8.com''')


def about_program():
	'''Shows an information dialog about the program.'''
	QMessageBox.information(main_window, 'About URL Shortener',
		'''The URL Shortener helps you access pages with a long URL. You even have the option to choose the API you want to use for shortening, which will directly affect the new URL.

You can also use the expander after shortening a URL.

This project was developed by Jose Wesley De Lima Silva. You can learn more by visiting the project page on github:

https://github.com/jwesleylima/URL-Shortener-Python-PyQt5''')


if __name__ == '__main__':
	from sys import argv, exit
	app = QApplication(argv)
	
	# load UI
	main_window = loadUi('ui/main.ui')
	successful_dialog = loadUi('ui/successful_dialog.ui')
	failure_dialog = loadUi('ui/failure_dialog.ui')

	# set icons
	main_window.setWindowIcon(QIcon('images/icon.png'))
	successful_dialog.setWindowIcon(QIcon('images/icon.png'))
	failure_dialog.setWindowIcon(QIcon('images/icon.png'))
	
	# pre enter
	pre_enter()
	successful_dialog_pre_enter()
	failure_dialog_pre_enter()
	
	# exec
	main_window.show()
	exit(app.exec_())
