import pypboy
import settings
import socket

class Module(pypboy.SubModule):

	label = "MISC"



	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)

		self.topmenu = pypboy.ui.TopMenu()
		self.add(self.topmenu)
		self.topmenu.label = "DATA"
		self.topmenu.title = settings.MODULE_TEXT

		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			try:
				s.connect(('8.8.8.8', 80))
				ip = s.getsockname()[0]
			except Exception:
				ip = '127.0.0.1'
			finally:
				s.close()
		except Exception:
			ip = '127.0.0.1'
   
		settings.FOOTER_TIME[2] = ip
		self.footer = pypboy.ui.Footer(settings.FOOTER_TIME)
		self.footer.rect[0] = settings.footer_x
		self.footer.rect[1] = settings.footer_y
		self.add(self.footer)
