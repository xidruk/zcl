.PHONY: install uninstall clean

install:
	@echo "------------------------------------------"
	@echo "  ZCL Installer"
	@echo "------------------------------------------"
	@echo ""
	@echo "[1/5] Detecting shell configurations..."
	@SHELL_CONFIGS=""; \
	if [ -f "$$HOME/.bashrc" ]; then \
		SHELL_CONFIGS="$$SHELL_CONFIGS $$HOME/.bashrc"; \
		echo "  [SUCCESS] Found: ~/.bashrc"; \
	fi; \
	if [ -f "$$HOME/.zshrc" ]; then \
		SHELL_CONFIGS="$$SHELL_CONFIGS $$HOME/.zshrc"; \
		echo "  [SUCCESS] Found: ~/.zshrc"; \
	fi; \
	if [ -f "$$HOME/.config/fish/config.fish" ]; then \
		SHELL_CONFIGS="$$SHELL_CONFIGS $$HOME/.config/fish/config.fish"; \
		echo "  [SUCCESS] Found: ~/.config/fish/config.fish"; \
	fi; \
	if [ -f "$$HOME/.profile" ]; then \
		SHELL_CONFIGS="$$SHELL_CONFIGS $$HOME/.profile"; \
		echo "  [SUCCESS] Found: ~/.profile"; \
	fi; \
	if [ -z "$$SHELL_CONFIGS" ]; then \
		echo "  [ERROR] No shell config files found!"; \
		echo "  [ERROR] Please create ~/.bashrc or ~/.zshrc first."; \
		exit 1; \
	fi; \
	echo ""; \
	echo "[2/5] Detecting Python interpreter..."; \
	PYTHON_CMD=""; \
	if command -v python3 >/dev/null 2>&1; then \
		PYTHON_CMD="python3"; \
		echo "  [SUCCESS] Found: python3 ($$(python3 --version))"; \
	elif command -v python >/dev/null 2>&1; then \
		PYTHON_CMD="python"; \
		echo "  [SUCCESS] Found: python ($$(python --version))"; \
	elif command -v python2 >/dev/null 2>&1; then \
		PYTHON_CMD="python2"; \
		echo "  [SUCCESS] Found: python2 ($$(python2 --version))"; \
	else \
		echo "  [ERROR] No Python interpreter found!"; \
		echo "  [ERROR] Please install Python 3 first."; \
		exit 1; \
	fi; \
	echo ""; \
	echo "[3/5] Setting up ~/.zcl directory..."; \
	if [ -d "$$HOME/.zcl" ]; then \
		echo "  [WARNING] ~/.zcl already exists, cleaning old content..."; \
		rm -rf "$$HOME/.zcl"; \
	fi; \
	mkdir -p "$$HOME/.zcl"; \
	echo "  [SUCCESS] Created: ~/.zcl/"; \
	echo ""; \
	echo "[4/5] Copying project files..."; \
	cp -r zcl.py zcl_linux_machine_cfps.py zcl_darwin_machine_cfps.py "$$HOME/.zcl/"; \
	if [ -d "cache_dirs" ]; then \
		cp -r cache_dirs "$$HOME/.zcl/"; \
	fi; \
	echo "  [SUCCESS] zcl.py"; \
	echo "  [SUCCESS] zcl_linux_machine_cfps.py"; \
	echo "  [SUCCESS] zcl_darwin_machine_cfps.py"; \
	if [ -d "cache_dirs" ]; then \
		echo "  [SUCCESS] cache_dirs/"; \
	fi; \
	echo ""; \
	echo "[5/5] Adding 'zcl' command to shell configs..."; \
	ZCL_ALIAS="alias zcl='$$PYTHON_CMD ~/.zcl/zcl.py'"; \
	for config in $$SHELL_CONFIGS; do \
		if grep -q "alias zcl=" "$$config" 2>/dev/null; then \
			echo "  [WARNING] zcl alias already exists in $$config, skipping..."; \
		else \
			echo "" >> "$$config"; \
			echo "# ZCL - ZCleaner command" >> "$$config"; \
			echo "$$ZCL_ALIAS" >> "$$config"; \
			echo "  [SUCCESS] Added alias to: $$config"; \
		fi; \
	done; \
	echo ""; \
	echo "[6/6] Reloading shell configurations..."; \
	if [ -f "$$HOME/.bashrc" ]; then \
		bash -c "source $$HOME/.bashrc" 2>/dev/null || true; \
		echo "  [SUCCESS] Reloaded ~/.bashrc"; \
	fi; \
	if [ -f "$$HOME/.zshrc" ]; then \
		zsh -c "source $$HOME/.zshrc" 2>/dev/null || true; \
		echo "  [SUCCESS] Reloaded ~/.zshrc"; \
	fi; \
	echo ""; \
	echo "------------------------------------------"; \
	echo "  Installation complete!"; \
	echo "------------------------------------------"; \
	echo ""; \
	echo "The 'zcl' command is now available."; \
	echo "Just type: zcl"; \
	echo ""

uninstall:
	@echo "------------------------------------------"
	@echo "  ZCL Uninstaller"
	@echo "------------------------------------------"
	@echo ""
	@echo "[1/3] Removing ~/.zcl directory..."
	@if [ -d "$$HOME/.zcl" ]; then \
		rm -rf "$$HOME/.zcl"; \
		echo "  [SUCCESS] Removed: ~/.zcl/"; \
	else \
		echo "  [WARNING] ~/.zcl not found, nothing to remove."; \
	fi
	@echo ""
	@echo "[2/3] Removing 'zcl' alias from shell configs..."
	@for config in "$$HOME/.bashrc" "$$HOME/.zshrc" "$$HOME/.config/fish/config.fish" "$$HOME/.profile"; do \
		if [ -f "$$config" ]; then \
			if grep -q "alias zcl=" "$$config" 2>/dev/null; then \
				sed -i.bak '/# ZCL - ZCleaner command/d' "$$config"; \
				sed -i.bak '/alias zcl=/d' "$$config"; \
				rm -f "$$config.bak"; \
				echo "  [SUCCESS] Removed alias from: $$config"; \
			fi; \
		fi; \
	done
	@echo ""
	@echo "[3/3] Cleaning up..."
	@echo "  [SUCCESS] Done!"
	@echo ""
	@echo "------------------------------------------"
	@echo "  Uninstallation complete!"
	@echo "------------------------------------------"
	@echo ""
	@echo "Restart your terminal or run 'source ~/.bashrc'"
	@echo ""

clean:
	@echo "[INFO] Cleaning temporary files..."
	@rm -rf __pycache__
	@rm -f *.pyc
	@echo "[SUCCESS] Done!"