all:
		rm -rf bin
		mkdir bin
		cp src/lexer.py bin/lexer.py
		cp src/parser.py bin/parser.py
		cp src/create_graph.py bin/create_graph.py
		chmod +x bin/lexer.py bin/parser.py bin/create_graph.py

clean:
		rm -rf bin
		mkdir bin
