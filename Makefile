all:
		rm -rf bin
		mkdir bin
		cp src/lexer.py bin/lexer.py
		cp src/parser.py bin/parser.py
		cp src/create_graph.py bin/create_graph.py
		cp src/model.py bin/model.py
		cp src/symbol_table.py bin/symbol_table.py
		cp src/tac.py bin/tac.py
		chmod +x bin/lexer.py bin/parser.py bin/create_graph.py bin/model.py bin/symbol_table.py bin/tac.py

clean:
		rm -rf bin
		mkdir bin
		rm -rf *.csv
		rm -rf graph.*
		rm -rf src/__pycache__
