Name: libwvstreams
Version: 4.6
Release: 6%{?dist}
Summary: WvStreams is a network programming library written in C++
Source: http://wvstreams.googlecode.com/files/wvstreams-%{version}.tar.gz
#fixed multilib issue (bug #192717)
Patch1: wvstreams-4.2.2-multilib.patch
#install-xplc target was missing
Patch2: wvstreams-4.5-noxplctarget.patch
#Use .so instead of .a
Patch3: wvstreams-4.6-dbus.patch
#sys/stat.h is missing some files in rawhide build
Patch4: wvstreams-4.6.1-statinclude.patch
#const X509V3_EXT_METHOD * -> X509V3_EXT_METHOD * conversion not allowed
#by latest gcc
Patch5: wvstreams-4.6.1-gcc.patch
URL: http://alumnit.ca/wiki/index.php?page=WvStreams
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: openssl-devel, pkgconfig, zlib-devel, readline-devel, dbus-devel
License: LGPLv2+

%description
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development.

%package devel
Summary: Development files for WvStreams
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development.  This package contains the files
needed for developing applications which use WvStreams.

%prep
%setup -q -n wvstreams-%{version}
%patch1 -p1 -b .multilib
%patch2 -p1 -b .xplctarget
%patch3 -p1 -b .dbus
%patch4 -p1 -b .statinclude
%patch5 -p1 -b .gcc

%build
#  --without-PACKAGE       do not use PACKAGE (same as --with-PACKAGE=no)
#  --with-dbus             DBUS
#  --with-openssl          OpenSSL >= 0.9.7 (required)
#  --with-pam              PAM
#  --with-tcl              Tcl
#  --with-qt               Qt
#  --with-zlib             zlib (required)
touch configure
%configure --with-dbus=yes --with-pam --with-openssl --without-tcl --with-qt=no --disable-static

#upstream is working with .a lib, so hardcoding path to libdbus-1.so to prevent build failures, parallel build fails
make LIBS_DBUS=/%{_lib}/libdbus-1.so COPTS="$RPM_OPT_FLAGS -fPIC -fno-strict-aliasing" CXXOPTS="$RPM_OPT_FLAGS -fPIC -fpermissive -fno-strict-aliasing" VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
chmod 755 $RPM_BUILD_ROOT%{_libdir}/*.so.*
rm -fr $RPM_BUILD_ROOT/usr/bin

pushd $RPM_BUILD_ROOT
rm -f \
   ./etc/uniconf.conf \
   .%{_bindir}/uni \
   .%{_libdir}/pkgconfig/libwvqt.pc \
   .%{_sbindir}/uniconfd \
   .%{_mandir}/man8/uni.8* \
   .%{_mandir}/man8/uniconfd.8* \
   .%{_var}/lib/uniconf/uniconfd.ini
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/wvstreams
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/valgrind/*.supp
%{_libdir}/pkgconfig/*.pc

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Thu Jan 28 2010 Ondrej Vasik <ovasik@redhat.com> - 4.6-6
- build correctly with newer glibc-headers and newer gcc
  (#558912)
- add comments, fix few merge review issues

* Thu Dec 03 2009 Dennis Gregorovic <dgregor@redhat.com> - 4.6-5.2
- Rebuilt for RHEL 6

* Mon Nov 23 2009 Dennis Gregorovic <dgregor@redhat.com> - 4.6-5.1
- Rebuilt for RHEL 6

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 4.6-5
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 27 2009 Ondrej Vasik <ovasik@redhat.com> - 4.6-3
- another fix for build with dbus(#479144)

* Sat Jun 27 2009 Ondrej Vasik <ovasik@redhat.com> - 4.6-2
- add build requires for dbus-devel, build with libdbus-1.so
  (#479144)
- fix multilib issue with wvautoconf.h(#508418)

* Thu Jun 11 2009 Ondrej Vasik <ovasik@redhat.com> - 4.6-1
- new upstream release with dynamically linked dbus(#479144)

* Fri Feb 27 2009 Ondrej Vasik <ovasik@redhat.com> - 4.5.1-5
- fix rebuild failure with gcc 4.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 4.5.1-3
- rebuild with new openssl

* Fri Jan 09 2009 Ondrej Vasik <ovasik@redhat.com> - 4.5.1-2
- do not remove libwvdbus.pc (#479144)

* Thu Jan 08 2009 Ondrej Vasik <ovasik@redhat.com> - 4.5.1-1
- new upstream release 4.5.1 , removed applied patches
- activate --with-dbus(#479144)

* Fri Nov 22 2008 Ondrej Vasik <ovasik@redhat.com> - 4.5-1
- new upstream release
- fixed issue with missing install-xplc target and std::sort
  missing gcc-4.3 error
- updated optional configure options list in spec file

* Fri Aug 28 2008 Ondrej Vasik <ovasik@redhat.com> - 4.4.1-5
- patch fuzz clean up

* Tue Feb 12 2008 Ondrej Vasik <ovasik@redhat.com> - 4.4.1-4
- gcc43 rebuild, climits instead limits.h usage

* Wed Dec 05 2007 Ondrej Vasik <ovasik@redhat.com> - 4.4.1-3
- rebuilt because of new OpenSSL

* Wed Nov 28 2007 Ondrej Vasik <ovasik@redhat.com> - 4.4.1-2
- no use of obsolete sa_restorer(#402531- by Oliver Falk)

* Mon Oct 22 2007 Ondrej Vasik <ovasik@redhat.com> - 4.4.1-1
- version 4.4.1

* Fri Aug 17 2007 Harald Hoyer <harald@rawhide.home> - 4.4-1
- version 4.4
- changed license tag to LGPLv2+

* Thu Jun 28 2007 Harald Hoyer <harald@redhat.com> - 4.3-2
- added static libs, esp. xplc-cxx

* Thu Jun 28 2007 Harald Hoyer <harald@redhat.com> - 4.3-1
- version 4.3

* Wed Apr 18 2007 Harald Hoyer <harald@redhat.com> - 4.2.2-4
- specfile review

* Wed Jan 24 2007 Harald Hoyer <harald@redhat.com> - 4.2.2-3
- fixed code for new g++ version

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.2.2-2.1
- rebuild

* Fri Jun 02 2006 Harald Hoyer <harald@redhat.com> 4.2.2-2
- more corrections to multilib patch (bug #192717)

* Wed May 24 2006 Harald Hoyer <harald@redhat.com> 4.2.2-1
- version 4.2.2
- fixed multilib issue (bug #192717)

* Fri Mar 10 2006 Bill Nottingham <notting@redhat.com> - 4.2.1-2
- rebuild for ppc TLS issue (#184446)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.2.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.2.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 19 2005 Harald Hoyer <harald@redhat.com> 4.2.1-1
- version 4.2.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> 3.75.0-6
- rebuilt against new openssl
- the gcc4 patch shouldn't be used anymore

* Mon Mar 14 2005 Harald Hoyer <harald@redhat.com> 3.75.0-5
- gcc4 patch added

* Wed Mar  2 2005 Jindrich Novy <jnovy@redhat.com> 3.75.0-4
- rebuilt

* Wed Feb 09 2005 Harald Hoyer <harald@redhat.com>
- rebuilt

* Wed Jun 28 2004 Harald Hoyer <harald@redhat.com> 3.75.0-2
- added libwvstreams-3.75.0-stringbuf.patch (114996)

* Mon Jun 21 2004 Harald Hoyer <harald@redhat.com> 3.75.0-1
- version 3.75.0

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Oct 10 2003 Nalin Dahyabhai <nalin@redhat.com> 3.70-12
- link libwvstreams shared libs against libcrypt, upon which they depend

* Mon Sep  8 2003 Nalin Dahyabhai <nalin@redhat.com> 3.70-11
- rebuild

* Mon Sep  8 2003 Nalin Dahyabhai <nalin@redhat.com> 3.70-10
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 3.70-7
- rebuild

* Fri Jan  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- correct an const/not-const type mismatch that breaks compilation with newer
  OpenSSL
- add flags from pkgconfig so that OpenSSL is always found

* Tue Sep 10 2002 Mike A. Harris <mharris@redhat.com> 3.70-6
- use FHS macros for multilib systems

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Tim Powers <timp@redhat.com>
- rebuild using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Nalin Dahyabhai <nalin@redhat.com> 3.70-1
- patch to build with gcc 3.x
- build with -fPIC

* Wed Apr 10 2002 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.70

* Wed Mar 27 2002 Nalin Dahyabhai <nalin@redhat.com> 3.69-1
- pull in from upstream tarball

* Wed Feb 27 2002 Nalin Dahyabhai <nalin@redhat.com>
- merge the main and -devel packages into one .spec file
- use globbing to shorten the file lists
- don't define name, version, and release as macros (RPM does this by default)
- use the License: tag instead of Copyright: (equivalent at the package level,
  but License: reflects the intent of the tag better)
- use a URL to point to the source of the source tarball
- add BuildRequires: openssl-devel (libwvcrypto uses libcrypto)
- move the buildroot to be under %%{_tmppath}, so that it can be moved by
  altering RPM's configuration

* Tue Jan 29 2002 Patrick Patterson <ppatters@nit.ca>
- Initial Release of WvStreams
