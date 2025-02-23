# -----------------------------------
#		GCP
# -----------------------------------

REGION = europe-west1

PYTHON_VERSION=3.8.12




gcloud ai-platform jobs submit training ${JOB_NAME} \
    --job-dir gs://${BUCKET_NAME}/${BUCKET_TRAINING_FOLDER}  \
    --package-path ${PACKAGE_NAME} \
    --module-name ${PACKAGE_NAME}.${FILENAME} \
    --python-version=${PYTHON_VERSION} \
    --runtime-version=${RUNTIME_VERSION} \
    --region ${REGION} \
    --stream-logs






# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* projectwind/*.py

black:
	@black scripts/* projectwind/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr projectwind-*.dist-info
	@rm -fr projectwind.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

run_api:
	uvicorn api.api:app --reload
