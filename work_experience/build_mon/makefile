.PHONY: clean init-web
clean:
	@rm -frv data/*
	@rm -frv status/*
	@rm -frv log/*
	@rm -frv monitor
init-web:
	@tar -zxvf monitor_front.tar.gz
	@cp -v web/*.php monitor/
	@cp -rv web/conf/ monitor/
	@cp web/components/bootstrap-3.3.5/js/iframe.js monitor/components/bootstrap-3.3.5/js/
