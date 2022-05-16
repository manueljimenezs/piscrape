env:
	python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt
	@echo "Run source venv/bin/activate on your actual shell to run the script"
deps:
	pip3 install -r requirements.txt
install_service:
	sudo cp systemd/piscrape.service /etc/systemd/user/
	sudo cp systemd/piscrape.timer /etc/systemd/user/
	sudo systemctl daemon-reload
	sudo systemctl restart piscrape.timer
	sudo systemctl status piscrape.timer
