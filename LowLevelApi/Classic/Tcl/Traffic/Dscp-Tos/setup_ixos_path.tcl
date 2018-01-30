#set IXOS_BUILD          $env(IXOS_BUILD)

set IXOS_BUILD "5.10.351.353"
if {$::tcl_platform(platform) == "windows"} {
    package require registry 1
    set ::_IXOS_INSTALL_ROOT [registry get "HKEY_LOCAL_MACHINE\\Software\\Ixia Communications\\IxOS\\$IXOS_BUILD\\InstallInfo" HOMEDIR]
    set ::_IXOS_PKG_DIR $::_IXOS_INSTALL_ROOT
    lappend ::auto_path $::_IXOS_PKG_DIR
    source "$::_IXOS_PKG_DIR\\TclScripts\\bin\\IxiaWish.tcl"
}