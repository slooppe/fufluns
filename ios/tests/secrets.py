DESCRIPTION = "MISSING"

SECRETS_SIGNATURES = {
	"RSA Private Key":     "-----BEGIN RSA PRIVATE KEY-----",
	"OPENSSH Private Key": "-----BEGIN OPENSSH PRIVATE KEY-----",
	"DSA Private Key":     "-----BEGIN DSA PRIVATE KEY-----",
	"EC Private Key":      "-----BEGIN EC PRIVATE KEY-----",
	"PGP Private Key":     "-----BEGIN PGP PRIVATE KEY BLOCK-----",
	"AWS Key":             "AKIA",
}

class ContextSecrets(object):
	def __init__(self, ipa, utils):
		super(ContextSecrets, self).__init__()
		self.ipa   = ipa
		self.utils = utils
		self.found = {}

	def add(self, key, value):
		if key not in self.found:
			self.found[key] = []
		if value not in self.found[key]:
			self.found[key].append(value)

	def size(self, key):
		return len(self.found)

	def add_tests(self):
		for key in self.found:
			self.utils.test(self.ipa, False, "Found {} ({} hit[s])".format(key, self.size(key)), DESCRIPTION, 8)
		if len(self.found) < 1:
			self.ipa.logger.info("[OK] No secrets signatures found")


def find_secrets(string, ctx):
	string = string.strip()
	if "%s" not in string:
		return None
	for key in SECRETS_SIGNATURES:
		prefix = SECRETS_SIGNATURES[key]
		if prefix in string:
			ctx.add(key, string)
	return None

def run_tests(ipa, r2, u, r2h):
	ctx = ContextSecrets(ipa, u)
	r2h.iterate_strings(r2, find_secrets, ctx)
	ctx.add_tests()

def name_test():
	return "Detection of secrets signatures"