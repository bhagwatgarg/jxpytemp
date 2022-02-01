all:
		rm -rf bin
		mkdir bin
		cp src/lexer.py bin/lexer.py
		chmod +x bin/lexer.py

clean:
		rm -rf bin
