
install:
	echo "install..."
	virtualenv venv; \
	. venv/bin/activate ;\
	pip install -r ts_cli/requirements.txt 

create-custom-product:
	. venv/bin/activate ;\
	python ts_cli/cli.py create-custom-product --payload samples/custom_product_tasking.json --input-file samples/custom_product_bundle.zip