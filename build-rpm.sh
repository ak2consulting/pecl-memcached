#!/bin/sh

FILES="config9.m4 \
	config.m4 \
	config.w32 \
	CREDITS \
	example.php \
	memcache.c \
	memcache_consistent_hash.c \
	memcache.dsp \
	memcache.php \
	memcache_queue.c \
	memcache_queue.h \
	memcache_session.c \
	memcache_standard_hash.c \
	php_memcache.h \
	README \
	build-rpm.sh \
	xml2changelog \
	package.xml \
	memcache-zynga.spec"


specfile=memcache-zynga.spec
package=memcache-zynga

version=`sed -n 's/^Version:[ ]*//p' $specfile`
package_name="$package-$version"

topdir=`pwd`/_rpmbuild

rm -rf $topdir 2>/dev/null

mkdir -p $topdir/{SRPMS,RPMS,BUILD,SOURCES,SPECS}
mkdir -p $topdir/$package_name

cp -a $FILES $topdir/$package_name && \
cp package.xml $topdir && \
cp xml2changelog $topdir/SOURCES && \
cp $specfile $topdir/SPECS && \
echo "Creating source tgz..." && \
tar czvf $topdir/SOURCES/$package_name.tgz -C $topdir package.xml $package_name && \
echo "Building rpm ..." && \
rpmbuild --define="_topdir $topdir" -ba $specfile && \
cp $topdir/SRPMS/*.rpm . && \
cp $topdir/RPMS/*/*.rpm . && \
rm -rf $topdir 
