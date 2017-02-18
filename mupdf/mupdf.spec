%global debug_package %{nil}

Name:           mupdf
Version:        1.10a
Release:        1%{?dist}
Summary:        A lightweight PDF viewer and toolkit
Group:          Applications/Publishing
License:        GPLv3
URL:            http://mupdf.com/
Source0:        http://mupdf.com/download/%{name}-%{version}-source.tar.gz
Source1:        %{name}.desktop
Patch0:         %{name}-openjpeg_static.patch
Patch1:         %{name}-disable_thirdparty.patch
BuildRequires:  gcc make binutils desktop-file-utils coreutils
BuildRequires:  openjpeg2-devel jbig2dec-devel desktop-file-utils
BuildRequires:  libjpeg-devel freetype-devel libXext-devel curl-devel

%description
MuPDF is a lightweight PDF viewer and toolkit written in portable C.
The renderer in MuPDF is tailored for high quality anti-aliased
graphics.  MuPDF renders text with metrics and spacing accurate to
within fractions of a pixel for the highest fidelity in reproducing
the look of a printed page on screen.
MuPDF has a small footprint.  A binary that includes the standard
Roman fonts is only one megabyte.  A build with full CJK support
(including an Asian font) is approximately five megabytes.
MuPDF has support for all non-interactive PDF 1.7 features, and the
toolkit provides a simple API for accessing the internal structures of
the PDF document.  Example code for navigating interactive links and
bookmarks, encrypting PDF files, extracting fonts, images, and
searchable text, and rendering pages to image files is provided.


%package devel
Summary:        Development files for %{name}
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}
Provides:         %{name}-static = %{version}-%{release}

%description devel
The mupdf-devel package contains header files for developing
applications that use mupdf and static libraries

%prep
%setup -q -n %{name}-%{version}-source
%patch0 -p1
%patch1 -p1
rm -rf thirdparty

%build
export CFLAGS="%{optflags} -fPIC -DJBIG_NO_MEMENTO"
make  %{?_smp_mflags} verbose=1 

%install
make DESTDIR=%{buildroot} install prefix=%{_prefix} libdir=%{_libdir}
## handle docs on our own
rm -rf %{buildroot}/%{_docdir}
rm -f %{buildroot}/%{_libdir}/libmupdfthird.a
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}
## fix strange permissons
chmod 0644 %{buildroot}%{_libdir}/*.a
find %{buildroot}/%{_mandir} -type f -exec chmod 0644 {} \;
find %{buildroot}/%{_includedir} -type f -exec chmod 0644 {} \;
cd %{buildroot}/%{_bindir} && ln -s %{name}-x11 %{name}

%post
update-desktop-database &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :

%files
%defattr(-,root,root,-)
%license COPYING
%doc README CHANGES docs/*
%{_bindir}/*
%{_datadir}/applications/mupdf.desktop
%{_mandir}/man1/*.1.gz



%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/lib%{name}.a

%changelog
* Sat Feb 18 2017 Marco Aurélio Graciotto Silva <magsilva@gmail.com> 1.10a-1
- New package built with tito. 

* Fri Feb 17 2017 Marco Aurélio Graciotto Silva <magsilva@gmail.com> - 1.10a-1
- New release 1.10a

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 28 2015 Pavel Zhukov <landgraf@fedoraproject.org> -1.8-1
- New release (#1280518)

* Sat Nov 28 2015 Pavel Zhukov <landgraf@fedoraproject.org> -1.7a-4
- Disable memento

* Wed Nov 18 2015 Petr Šabata <contyk@redhat.com> - 1.7a-3
- Package the license text with the %%license macro
- Don't use the %%version macro in filenames, it's not helpful
- Added extra handling for the docs; %%_docdir is no longer autopackaged,
  plus we want to install the license text elsewhere

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 01 2015  Pavel Zhukov <landgraf@fedoraproject.org> - 1.7a-1
- New release 1.7a (#1219482)
* Wed May 06 2015  Pavel Zhukov <landgraf@fedoraproject.org> - 1.7-1
- New release 1.7 (#1210318)
- Fix segfault in obj_close routine (#1202137, #1215752)

* Wed May 06 2015 Pavel Zhukov <landgraf@fedoraproject.org> - 1.5-6
- Fix executable name in desktop file

* Sat Oct 11 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 1.5-5
- Add missed curl-devel

* Fri Jul 04 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 1.5-3
- Add fPIC flag (#1109589)
- Add curl-devel to BR (#1114566)

* Sun Jun 15 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 1.5-2
- Add fix for new openjpeg2

* Sun Jun 15 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 1.5-1
- New release 1.5 (#1108710)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May  6 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 1.4-1
- New release 1.4 (#1087287)

* Fri Jan 24 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 1.1-5
- Fix stack overflow (#1056699)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 1.1-2
- rebuild due to "jpeg8-ABI" feature drop

* Wed Jan 09 2013 Pavel Zhukov <landgraf@fedoraproject.org> - 1.1-1
- New release

* Sun May 20 2012  Pavel Zhukov <landgraf@fedoraproject.org> - 1.0-1
- New release

* Wed Mar 14 2012  Pavel Zhukov <landgraf@fedoraproject.org> - 0.9-2
- Fix buffer overflow (#752388)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
