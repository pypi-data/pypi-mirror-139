# Flatbed-Scanner
### Version : 0.0.1

--------------------------------------------------------------------------------------------------- 

   ### Module for Python. This Module will enable a user to use any flatbed scanner using python.

--------------------------------------------------------------------------------------------------- 


### Copyright (c) 2022 Hardik Shah.


--------------------------------------------------------------------------------------------------- 
### Author : Hardik Shah.
### GitHub : https://github.com/Hardik-26
### License : GNU General Public License v3.0

--------------------------------------------------------------------------------------------------- 
### Brief Description :
With this module you will be able to use your flatbed scanner using python.<br>
This module uses PowerShell script to execute the scan command.<br>
you can say that this module works as an API for Powershell which can comunicate with the scanner using WIA (Windows Image Acquisition).<br>


--------------------------------------------------------------------------------------------------- 
### INSTRUCTIONS-
Make sure your flatbed scanner is pluged in and ready to scan <br>
well thats it.

---------------------------------------------------------------------------------------------------
## HOW TO USE-

`import scanny` <br>

### Scan A image- 
``` 
>>> scanny.StartScan("Path"( where you want your image file to be saved) , "ImageName" ) 
Eg- scanny.StartScan('C:\\Users\\Admin\\Desktop','TestIamge')
```

### Calibrate the scanner-
(Optional, only for backward compatibility purposes)-
```
>>> scanny.Calibrate()
```

### Get Scanner Bed Size-
```
>>> scanny.size()
```

### MISC-
```
>>> scanny._calibration
>>> scanny._pixel_len
```
---------------------------------------------------------------------------------------------------
### Other Information-
> Currently this python package only works for Windows 8 & Above. <br>
> Linux and MAC-OS compatibility comming soon in next version: 0.0.2. <br>

---------------------------------------------------------------------------------------------------

# Thank you. ☺