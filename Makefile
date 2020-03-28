.PHONY windows-alias
windows-alias:
	@echo Setting alias py -> python3
	@Set-Alias -Name python3 -Value py 

.PHONY install-deps
install-deps:
	@echo Installing dependencies
	@py 
