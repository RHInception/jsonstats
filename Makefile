RPMSPECDIR := .
RPMSPEC := $(RPMSPECDIR)/jsonstats.spec
clean:
	@find . -type f -regex ".*\.py[co]$$" -delete
	@find . -type f \( -name "*~" -or -name "#*" \) -delete
	@rm -fR build dist rpm-build MANIFEST

pep8:
	@echo "#############################################"
	@echo "# Running PEP8 Compliance Tests"
	@echo "#############################################"
# --ignore=E501,E221,W291,W391,E302,E251,E203,W293,E231,E303,E201,E225,E261
	pep8 --exclude="wsgiref/" --ignore=E501 -r JsonStats/ bin/ setup.py

pyflakes:
	@echo "#############################################"
	@echo "# Running Pyflakes Sanity Tests"
	@echo "# Note: most import errors may be ignored"
	@echo "#############################################"
	-pyflakes JsonStats/
	pyflakes bin/

sdist: clean
	python setup.py sdist -t MANIFEST.in

rpmcommon: sdist
	@mkdir -p rpm-build
	@cp dist/*.gz rpm-build/

srpm5: rpmcommon
	rpmbuild-md5 --define "_topdir %(pwd)/rpm-build" \
	--define 'dist .el5' \
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
