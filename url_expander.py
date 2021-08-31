from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from validators import url as is_valid_url
from tldextract import extract as get_domain_name_from_url
from data.supported_apis import SUPPORTED_APIS


# [!] This file should not be executed manually

'''Written by JWesleyLima on 08/31/2021
Access my GitHub profile: https://github.com/jwesleylima'''

# global objects
line_edit_url = None
combo_box_api = None
info = None
button_expand_url = None


def pre_enter():
	'''Executes some window presets.'''
	global combo_box_api, info, line_edit_url, button_expand_url

	# get widgets
	combo_box_api = main_window.comboBoxAPI
	info = main_window.information
	line_edit_url = main_window.lineEditShortenedURL
	button_expand_url = main_window.buttonExpandURL

	# LineEditCompleteURL
	line_edit_url.setFocus(True)
	line_edit_url.textChanged.connect(check_typed_url)

	# buttonShortenURL
	button_expand_url.setEnabled(False)
	button_expand_url.clicked.connect(expand_url)
	
	# ComboBoxAPI
	combo_box_api.addItems(list(SUPPORTED_APIS.keys()) + ['Unknown API'])
	combo_box_api.setCurrentText('Unknown API')

	# Some calls
	show_supported_apis()


def show_supported_apis():
	'''Shows the user which APIs are supported.'''
	MAX_NUMBER_OF_APIS_ON_DISPLAY = 7
	final_text = 'Support only '
	apis = list(SUPPORTED_APIS.keys())
	
	if len(apis) > MAX_NUMBER_OF_APIS_ON_DISPLAY:
		del apis[MAX_NUMBER_OF_APIS_ON_DISPLAY:]
		apis.append('more')

	for i, api in enumerate(apis):
		i += 1
		final_text += f'<font style="font-weight: bold;">{api}</font>'
		if i < len(apis) - 1: final_text += ', '
		elif i == len(apis) - 1: final_text += ' and '
	# Update on UI
	info.setText(final_text)


def check_typed_url():
	'''It does some checks against the URL entered by the user.'''
	valid_url = bool(is_valid_url(line_edit_url.text()))
	if valid_url and find_api_using_typed_url() != False:
		button_expand_url.setEnabled(valid_url)
		return
	button_expand_url.setEnabled(False)
	combo_box_api.setCurrentText('Unknown API')


def find_api_using_typed_url():
	'''Detects and displays the API used in the entered URL.

	Returns
	-------
	False - When the API used is unknown'''
	domain_name = ''
	try:
		ext = get_domain_name_from_url(line_edit_url.text())
		domain_name = f'{ext.domain}.{ext.suffix}'
	except: return False

	supported_apis = [x.lower() for x in list(SUPPORTED_APIS.keys())]
	if domain_name.lower() not in supported_apis: return False
	else: combo_box_api.setCurrentIndex(supported_apis.index(domain_name))


def expand_url():
	'''Expands the URL entered by the user.

	According to the result, it shows a success or failure dialog.'''
	selected_api = combo_box_api.currentText()
	selected_api_data = SUPPORTED_APIS[selected_api]
	shortened_url = line_edit_url.text().strip()
	complete_url = ''

	try:
		complete_url = selected_api_data['command-expand'](shortened_url)
	except Exception as e:
		show_failure_dialog('Unable to expand the URL. Please check the spelling of the URL and its validity. The API may be out of access at the moment, please try again with another API.')
	else:
		show_sucessful_dialog('Successfully Expanded', 'Your complete URL is',
			complete_url)


# load UI
main_window = loadUi('ui/url_expander.ui')
main_window.setWindowIcon(QIcon('images/icon.png'))
# pre enter
pre_enter()
# exec
main_window.exec_()
