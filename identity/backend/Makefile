test: | test-unit test-usecase test-functional

test-functional:
	PYTHONPATH=./src/:../lib/chamber:../lib/lambler python -m tests.functional.registration.verify

test-unit:
	PYTHONPATH=./src/:../lib/chamber:../lib/lambler pytest src/tests/unit/

test-usecase:
	PYTHONPATH=./src/:../lib/chamber:../lib/lambler pytest src/tests/usecase
