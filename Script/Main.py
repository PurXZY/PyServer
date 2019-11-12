from net.TcpServer import TcpServer
import coloredlogs


def main():
	coloredlogs.install(
		level='DEBUG',
		fmt="%(asctime)s:%(msecs)03d %(hostname)s [%(name)s:%(lineno)d] %(levelname)s - %(message)s"
	)
	config = {
		"host": "0.0.0.0",
		"port": 8888,
	}
	server = TcpServer(config)
	server.start()
	server.run()


if __name__ == "__main__":
	main()
