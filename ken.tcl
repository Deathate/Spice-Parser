proc print {text} {
    lakerMsgForm -name M -text $text
}
lakerSelectAll
lakerDeleteObj
lakerSchSelectGridItem -all
lakerSchTopology
lakerPasteObj -point (0,0) -justify CenterCenter -keepInstName 1
set cvId [lakerGetWndCellViewId]
set instlist [dbTraverse -cv $cvId -instonly 1 -attachBox 1]
set out [open output.txt w]
foreach inst $instlist {
    set instid [lindex $inst 0]
    set instbox [lindex $inst 1]
    set x1 [lindex $instbox 0 0]
    set yl [lindex $instbox 0 1]
    set x2 [lindex $instbox 1 0]
    set y2 [lindex $instbox 1 1]
    print 1
}
close $out