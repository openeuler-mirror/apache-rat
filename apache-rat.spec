Name:                apache-rat
Version:             0.12
Release:             1
Summary:             Apache Release Audit Tool (RAT)
License:             ASL 2.0
URL:                 http://creadur.apache.org/rat/
Source0:             http://www.apache.org/dist/creadur/apache-rat-0.12/apache-rat-0.12-src.tar.bz2
BuildArch:           noarch
Patch1:              0001-Port-to-current-doxia-sitetools.patch
BuildRequires:       maven-local mvn(commons-cli:commons-cli)
BuildRequires:       mvn(commons-collections:commons-collections) mvn(commons-io:commons-io)
BuildRequires:       mvn(commons-lang:commons-lang) mvn(junit:junit) mvn(org.apache.ant:ant)
BuildRequires:       mvn(org.apache.ant:ant-antunit) mvn(org.apache.ant:ant-testutil)
BuildRequires:       mvn(org.apache:apache:pom:) mvn(org.apache.commons:commons-compress)
BuildRequires:       mvn(org.apache.maven.doxia:doxia-core)
BuildRequires:       mvn(org.apache.maven.doxia:doxia-decoration-model)
BuildRequires:       mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:       mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:       mvn(org.apache.maven:maven-artifact:2.2.1)
BuildRequires:       mvn(org.apache.maven:maven-artifact-manager)
BuildRequires:       mvn(org.apache.maven:maven-model:2.2.1) mvn(org.apache.maven:maven-plugin-api)
BuildRequires:       mvn(org.apache.maven:maven-project) mvn(org.apache.maven:maven-settings:2.2.1)
BuildRequires:       mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:       mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:       mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:       mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:       mvn(org.apache.maven.shared:maven-plugin-testing-harness)
BuildRequires:       mvn(org.codehaus.plexus:plexus-utils) mvn(org.hamcrest:hamcrest-library)
BuildRequires:       mvn(org.mockito:mockito-all) mvn(org.mockito:mockito-core)
%description
Release Audit Tool (RAT) is a tool to improve accuracy and efficiency when
checking releases. It is heuristic in nature: making guesses about possible
problems. It will produce false positives and cannot find every possible
issue with a release. It's reports require interpretation.
RAT was developed in response to a need felt in the Apache Incubator to be
able to review releases for the most common faults less labor intensively.
It is therefore highly tuned to the Apache style of releases.
This package just contains meta-data, you will want either apache-rat-tasks,
or apache-rat-plugin.

%package api
Summary:             API module for %{name}
%description api
Shared beans and services.

%package core
Summary:             Core functionality for %{name}
Requires:            javapackages-tools
%description core
The core functionality of RAT, shared by the Ant tasks, and the Maven plugin.
It also includes a wrapper script "apache-rat" that should be the equivalent
to running upstream's "java -jar apache-rat.jar".

%package plugin
Summary:             Maven plugin for %{name}
%description plugin
Maven plugin for running RAT, the Release Audit Tool.

%package tasks
Summary:             Ant tasks for %{name}
%description tasks
Ant tasks for running RAT.

%package javadoc
Summary:             Javadocs for %{name}
%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%pom_disable_module apache-rat
%pom_remove_plugin -r :maven-antrun-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin -r :maven-invoker-plugin
%pom_xpath_remove pom:extensions
rm apache-rat-plugin/src/test/java/org/apache/rat/mp/RatCheckMojoTest.java

%build
%mvn_build -s

%install
%mvn_install
%jpackage_script org.apache.rat.Report "" "" %{name}/%{name}-core:commons-cli:commons-io:commons-collections:commons-compress:commons-lang:junit apache-rat true
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
echo "apache-rat/rat-core apache-rat/rat-tasks" > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/%{name}

%files -f .mfiles-%{name}-project
%doc LICENSE NOTICE

%files api -f .mfiles-%{name}-api
%doc README.txt RELEASE-NOTES.txt
%doc LICENSE NOTICE

%files core -f .mfiles-%{name}-core
%{_bindir}/%{name}

%files plugin -f .mfiles-%{name}-plugin

%files tasks -f .mfiles-%{name}-tasks
%{_sysconfdir}/ant.d/%{name}
%doc ant-task-examples.xml

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Thu Aug 13 2020 chengzihan <chengzihan2@huawei.com> - 0.12-1
- Package init
