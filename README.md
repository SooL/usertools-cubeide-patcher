# Cube IDE project patcher
Project patcher for CubeIDE project

## HOWTO :

First, create a project in STM32CubeIDE using `New STM32 Project`, **select the right STM32 target**, use the options :

 - Targeted Language : C++
 - Targeted Binary Type : Executable
 - Targeted Project Type : **Empty**
 
And hit "Finish".

Get yourself a SooL release with a manifest and put it in any directory, let say `/path/to/sool`.
You should have the `core` folder at `/path/to/sool/core` and a `manifest.xml` file.

Then launch the Project patcher tool.
Provide your project root folder (it should contains a `.cproject` file) and specify a relative root folder for sool in your project.
In example use `drivers/sool`. This folder should not exist and will contain the SooL's `core` folder.

Select the sool root directory (`/path/to/sool`), a list of chip defines should appear.
Select your SooL chip define, matching your chip. You can also write it directly in the "Chip" field.

Then `Put some SooL into my project` !

Finally hit F5 or `File > Refresh` while selecting your project in STM32CubeIDE and all new files should appear in CubeIDE.