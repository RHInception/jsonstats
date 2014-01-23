########################################################

# Makefile for jsonstats
#
# useful targets:
#   make sdist ---------------- produce a tarball
#   make rpm  ----------------- produce RPMs
#   make docs ----------------- rebuild the manpages (results are checked in)
#   make pyflakes, make pep8 -- source code checks
#   make test ----------------- run all unit tests (export LOG=true for /tmp/ logging)

########################################################

# > VARIABLE = value
#
# Normal setting of a variable - values within it are recursively
# expanded when the variable is USED, not when it's declared.
#
# > VARIABLE := value
#
# Setting of a variable with simple expansion of the values inside -
# values within it are expanded at DECLARATION time.

########################################################


MANPAGES := docs/man/man1/jsonstatsd.1
ifneq ($(shell which a2x 2>/dev/null),)
# This doesn't evaluate until it's called. The -D argument is the
# directory of the target file ($@), kinda like `dirname`.
ASCII2MAN = a2x -D $(dir $@) -d manpage -f manpage $<
ASCII2HTMLMAN = a2x -D docs/html/man/ -d manpage -f xhtml
else
ASCII2MAN = @echo "ERROR: AsciiDoc 'a2x' command is not installed but is required to build $(MANPAGES)" && exit 1
endif

# VERSION file provides one place to update the software version.
VERSION := $(shell cat VERSION)

# To force a rebuild of the docs run 'touch VERSION && make docs'
docs: $(MANPAGES)

# Regenerate %.1.asciidoc if %.1.asciidoc.in has been modified more
# recently than %.1.asciidoc.
%.1.asciidoc: %.1.asciidoc.in VERSION
	sed "s/%VERSION%/$(VERSION)/" $< > $@

# Regenerate %.1 if %.1.asciidoc or VERSION has been modified more
# recently than %.1. (Implicitly runs the %.1.asciidoc recipe)
%.1: %.1.asciidoc
	$(ASCII2MAN)

# Regenerate %.5.asciidoc if %.5.asciidoc.in has been modified more
# recently than %.5.asciidoc.
%.5.asciidoc: %.5.asciidoc.in VERSION
	sed "s/%VERSION%/$(VERSION)/" $< > $@

# Regenerate %.5 if %.5.asciidoc or VERSION has been modified more
# recently than %.5. (Implicitly runs the %.5.asciidoc recipe)
%.5: %.5.asciidoc
	$(ASCII2MAN)


RPMSPECDIR := .
RPMSPEC := $(RPMSPECDIR)/jsonstats.spec

tag:
	git tag -s -m $(TAG) jsonstats-$(TAG)

tests: unittests pep8 pyflakes
	:

unittests:
	@echo "#############################################"
	@echo "# Running Unit Tests"
	@echo "#############################################"
	nosetests -v

clean:
	@find . -type f -regex ".*\.py[co]$$" -delete
	@find . -type f \( -name "*~" -or -name "#*" \) -delete
	@rm -fR build dist rpm-build MANIFEST

pep8:
	@echo "#############################################"
	@echo "# Running PEP8 Compliance Tests"
	@echo "#############################################"
	pep8 --ignore=E501,E121,E124 JsonStats/ bin/jsonstatsd setup.py

pyflakes:
	@echo "#############################################"
	@echo "# Running Pyflakes Sanity Tests"
	@echo "# Note: most import errors may be ignored"
	@echo "#############################################"
	-pyflakes JsonStats/
	pyflakes bin/

install: clean
	python ./setup.py install

sdist: clean
	python setup.py sdist -t MANIFEST.in

rpmcommon: sdist
	@mkdir -p rpm-build
	@cp dist/*.gz rpm-build/

srpm5: rpmcommon
	rpmbuild --define "_topdir %(pwd)/rpm-build" \
	--define 'dist .el5' \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir $(RPMSPECDIR)" \
	--define "_sourcedir %{_topdir}" \
	--define "_source_filedigest_algorithm 1" \
	--define "_binary_filedigest_algorithm 1" \
	--define "_binary_payload w9.gzdio" \
	--define "_source_payload w9.gzdio" \
	--define "_default_patch_fuzz 2" \
	-bs $(RPMSPEC)
	@echo "#############################################"
	@echo "JsonStats SRPM is built:"
	@find rpm-build -maxdepth 2 -name 'jsonstats*src.rpm' | awk '{print "    " $$1}'
	@echo "#############################################"

srpm: rpmcommon
	rpmbuild --define "_topdir %(pwd)/rpm-build" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir $(RPMSPECDIR)" \
	--define "_sourcedir %{_topdir}" \
	-bs $(RPMSPEC)
	@echo "#############################################"
	@echo "JsonStats SRPM is built:"
	@find rpm-build -maxdepth 2 -name 'jsonstats*src.rpm' | awk '{print "    " $$1}'
	@echo "#############################################"

rpm: rpmcommon
	rpmbuild --define "_topdir %(pwd)/rpm-build" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir $(RPMSPECDIR)" \
	--define "_sourcedir %{_topdir}" \
	-ba $(RPMSPEC)
	@echo "#############################################"
	@echo "JsonStats RPMs are built:"
	@find rpm-build -maxdepth 2 -name 'jsonstats*.rpm' | awk '{print "    " $$1}'
	@echo "#############################################"
