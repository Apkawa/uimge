[Setup]
AppName=guimge
AppVerName=guimge 0.1.2-0
AppPublisher=apkawa
AppPublisherURL=http://github.com/Apkawa/uimge/
DefaultDirName={pf}\guimge
DefaultGroupName=guimge
DisableProgramGroupPage=true
OutputBaseFilename=setup
Compression=lzma
SolidCompression=true
AllowUNCPath=false
VersionInfoVersion=1.0
VersionInfoCompany=Apkawa Inc
VersionInfoDescription=guimge - gui muiltiuploaders image to different imagehostings


[Dirs]
Name: {app}; Flags: uninsalwaysuninstall

[Files]
Source: dist\*; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: {group}\guimge; Filename: {app}\guimge.exe; WorkingDir: {app}
Name: {group}\Uinstall; Filename: {app}\unins000.exe; WorkingDir: {app}

[Run]
Filename: {app}\guimge.exe; Description: {cm:LaunchProgram,guimge}; Flags: nowait postinstall skipifsilent
