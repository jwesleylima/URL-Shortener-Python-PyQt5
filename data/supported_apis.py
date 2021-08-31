from pyshorteners import Shortener


s = Shortener()

'''Written by JWesleyLima on 08/31/2021
Access my GitHub profile: https://github.com/jwesleylima'''

# This is the list of supported APIs. You can easily add more APIs. Change it if you know what you are doing.

SUPPORTED_APIS = {
	'Is.gd': {
		'result-example': 'http://is.gd/example',
		'limited-api': False,
		'api-limits-msg': 'Shorten any URL',
		'command': s.isgd.short,
		'command-expand': s.isgd.expand
	},
	'Da.gd': {
		'result-example': 'http://da.gd/example',
		'limited-api': False,
		'api-limits-msg': 'Shorten any URL',
		'command': s.dagd.short,
		'command-expand': s.dagd.expand
	},
	'Git.io': {
		'result-example': 'https://git.io/example',
		'limited-api': True,
		'api-limits-msg': 'GitHub.com and related URLs only',
		'command': s.gitio.short,
		'command-expand': s.gitio.expand
	},
	'Clck.ru': {
		'result-example': 'http://clck.ru/example',
		'limited-api': False,
		'api-limits-msg': 'Shorten any URL',
		'command': s.clckru.short,
		'command-expand': s.clckru.expand
	},
	'Chilp.it': {
		'result-example': 'http://chilp.it/example',
		'limited-api': False,
		'api-limits-msg': 'Shorten any URL',
		'command': s.chilpit.short,
		'command-expand': s.chilpit.expand
	},
	'Osdb.link': {
		'result-example': 'http://osdb.link/example',
		'limited-api': True,
		'api-limits-msg': '<font color="#111">Shorten any URL - </font>Contains ads',
		'command': s.osdb.short,
		'command-expand': s.osdb.expand
	},
	'Qps.ru': {
		'result-example': 'http://qps.ru/example',
		'limited-api': False,
		'api-limits-msg': 'Shorten any URL',
		'command': s.qpsru.short,
		'command-expand': s.qpsru.expand
	},
	'TinyURL.com': {
		'result-example': 'http://tinyurl.com/example',
		'limited-api': False,
		'api-limits-msg': 'Shorten any URL',
		'command': s.tinyurl.short,
		'command-expand': s.tinyurl.expand
	},
}
