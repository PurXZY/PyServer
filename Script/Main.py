from TcpServer import TcpServer


def main():
	config = {
		"host": "127.0.0.1",
		"port": 12233,
	}
	server = TcpServer(config)
	server.start()
	server.run()


if __name__ == "__main__":
	main()
