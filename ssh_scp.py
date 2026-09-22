import subprocess
import os

class Ssh:

	def __init__(self, user, host, password=None) -> None:
		self.__user = user
		self.__password = password
		self.__host = host

	def __ssh(self, cmd) -> list:
		"""
		Execute une commande à travers la session ssh sans password.

		:param cmd: commande a lancer
		:type cmd: str
		:return: le resultat de la commande ainsi que le code d'erreur
		:rtype: list
		"""

		script_dir = os.path.dirname(__file__)
		try :
			output = subprocess.run(["bash", f"{script_dir}/ssh/ssh.sh", self.__user, self.__host, cmd], capture_output=True, text=True, timeout=15)
		except subprocess.TimeoutExpired:
			return "", 1
		return output.stdout.strip(), output.returncode
	
	def __ssh_pass(self, cmd) -> list:
		"""
		Execute une commande à travers la session ssh avec password.

		:param cmd: commande a lancer
		:type cmd: str
		:return: le resultat de la commande ainsi que le code d'erreur
		:rtype: list
		"""

		script_dir = os.path.dirname(__file__)
		try :
			output = subprocess.run(["bash", f"{script_dir}/ssh/ssh_pass.sh", self.__user, self.__host, self.__password, cmd], capture_output=True, text=True, timeout=15)
		except subprocess.TimeoutExpired:
			return "", 1
		return output.stdout.strip(), output.returncode
	
	def execute_cmd(self, cmd) -> list:
		"""
		Execute une commande à travers la session ssh.
		Le password est optionnel.

		:param cmd: commande a lancer
		:type cmd: str
		:return: le resultat de la commande ainsi que le code d'erreur
		:rtype: list
		"""

		if self.__password is None:
			return self.__ssh(cmd)
		return self.__ssh_pass(cmd)
		
	def execute_cmd_reboot(self, cmd) -> list:
		"""
		Execute une commande à travers la session ssh pour rebooter un équipement.
		Le password est optionnel. Les tests sont ignorés, le reboot risquant de les déclencher.

		:param cmd: commande a lancer
		:type cmd: str
		:return: le resultat de la commande ainsi que le code d'erreur
		:rtype: list
		"""

		try:
			return self.execute_cmd(cmd)
		except:
			return ("Reboot command sent", 0)

class Scp:
	def __init__(self, user, host, password=None) -> None:
		self.__user = user
		self.__password = password
		self.__host = host

	def __upload(self, src_file, dst_file) -> list:
		script_dir = os.path.dirname(__file__)

		if self.password:
			try :
				output = subprocess.run(["bash", f"{script_dir}/scp/scp_pass_upload.sh", self.__host, src_file, dst_file, self.__user, self.__password], capture_output=True, text=True, timeout=15)
			except subprocess.TimeoutExpired:
				return "", 1
			return output.stdout.strip(), output.returncode

		try :
			output = subprocess.run(["bash", f"{script_dir}/scp/scp_upload.sh", self.__host, src_file, dst_file, self.__user], capture_output=True, text=True, timeout=15)
		except subprocess.TimeoutExpired:
			return "", 1
		return output.stdout.strip(), output.returncode

	def __download(self, src_file, dst_file) -> list:
		script_dir = os.path.dirname(__file__)

		if self.password:
			try :
				output = subprocess.run(["bash", f"{script_dir}/scp/scp_pass_download.sh", self.__host, src_file, dst_file, self.__user, self.__password], capture_output=True, text=True, timeout=15)
			except subprocess.TimeoutExpired:
				return "", 1
			return output.stdout.strip(), output.returncode

		try :
			output = subprocess.run(["bash", f"{script_dir}/scp/scp_download.sh", self.__host, src_file, dst_file, self.__user], capture_output=True, text=True, timeout=15)
		except subprocess.TimeoutExpired:
			return "", 1
		return output.stdout.strip(), output.returncode

	def scp(self, up_dl, src_file, dst_file) -> list:
		if up_dl not in ('upload', 'download'):
			raise ValueError(f"src_file doit être 'upload' ou 'download', reçu : '{src_file}'")

		if up_dl == 'upload':
			return self.__upload(src_file=src_file, dst_file=dst_file)

		return self.__download(src_file=src_file,dst_file=dst_file)

		
		
